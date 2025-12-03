#====================================================
# Author: 601 Solutions
# Title: retriever.py
# Multi-Collection Retriever 로드 및 관리
#====================================================

import os
import sys
from langchain_community.vectorstores import Chroma 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.retrievers import MergerRetriever
from langchain_classic.chains.query_constructor.base import AttributeInfo
from langchain_classic.retrievers.self_query.base import SelfQueryRetriever
from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from typing import List

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from llm.llm_loader import get_llm 

class SimpleMergerRetriever(BaseRetriever):
    retrievers: List[BaseRetriever]

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None
    ) -> List[Document]:
        all_docs = []
        for retriever in self.retrievers:
            docs = retriever.invoke(query)
            all_docs.extend(docs)
        # 중복 제거 (내용 기준)
        seen = set()
        unique_docs = []
        for doc in all_docs:
            if doc.page_content not in seen:
                seen.add(doc.page_content)
                unique_docs.append(doc)
        return unique_docs

_retriever = None

def get_rag_retriever():
    global _retriever
    if _retriever is not None:
        return _retriever

    print("🔄 임베딩 모델 로딩 중...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    if not os.path.exists(config.DB_DIR):
        print(f"❌ 오류: '{config.DB_DIR}' 폴더가 없습니다.")
        return None

    llm = get_llm() 

    # 1. 의약품용 Retriever
    med_vectorstore = Chroma(
        persist_directory=str(config.DB_DIR), 
        collection_name="medicine_data", 
        embedding_function=embeddings
    )
    med_metadata = [
        AttributeInfo(name="product_name", description="의약품 제품명", type="string"),
        AttributeInfo(name="company", description="제조사 이름", type="string"),
    ]
    med_retriever = SelfQueryRetriever.from_llm(
        llm, med_vectorstore, "동물용 의약품 정보", med_metadata, verbose=True
    )

    # 2. 상품용 Retriever
    prod_vectorstore = Chroma(
        persist_directory=str(config.DB_DIR), 
        collection_name="product_data", 
        embedding_function=embeddings
    )
    prod_metadata = [
        AttributeInfo(name="product_name", description="건강기능식품 상품명", type="string"),
        AttributeInfo(name="price", description="상품 가격 (원)", type="integer"),
        AttributeInfo(name="rating", description="평점 (0~5점)", type="float"),
    ]
    prod_retriever = SelfQueryRetriever.from_llm(
        llm, prod_vectorstore, "반려동물 건강기능식품 정보", prod_metadata, verbose=True
    )

    # 3. 통합 (커스텀 클래스 사용)
    print("🔗 의약품 및 상품 DB 통합 중...")
    # 여기서 우리가 만든 SimpleMergerRetriever를 사용합니다.
    _retriever = SimpleMergerRetriever(retrievers=[med_retriever, prod_retriever])
    
    print("✅ 통합 Retriever 준비 완료")
    return _retriever