#====================================================
# Author: 601 Solutions
# Title: retriever.py
# Multi-Collection Retriever 로드 및 관리
#====================================================

import os
import sys
from langchain_chroma import Chroma # 최신 패키지 사용
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.retrievers import MergerRetriever
from langchain_classic.chains.query_constructor.base import AttributeInfo
from langchain_classic.retrievers.self_query.base import SelfQueryRetriever

# 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from llm.llm_loader import get_llm 

_retriever = None

def get_rag_retriever():
    """
    두 개의 컬렉션(의약품, 상품)을 통합 검색하는 Retriever 반환
    """
    global _retriever
    if _retriever is not None:
        return _retriever

    print("🔄 임베딩 모델 로딩 중...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    if not os.path.exists(config.DB_DIR):
        print(f"❌ 오류: '{config.DB_DIR}' 폴더가 없습니다.")
        return None

    llm = get_llm() 

    # -------------------------------------------------------
    # 1. 의약품용 Retriever 생성 (medicine_data)
    # -------------------------------------------------------
    med_vectorstore = Chroma(
        persist_directory=str(config.DB_DIR), 
        collection_name="medicine_data", # ingest_data.py와 일치해야 함
        embedding_function=embeddings
    )
    
    med_metadata = [
        AttributeInfo(name="product_name", description="의약품 제품명", type="string"),
        AttributeInfo(name="company", description="제조사 이름", type="string"),
    ]
    
    med_retriever = SelfQueryRetriever.from_llm(
        llm,
        med_vectorstore,
        "동물용 의약품 정보 (효능, 용법, 주의사항)",
        med_metadata,
        verbose=True
    )

    # -------------------------------------------------------
    # 2. 상품용 Retriever 생성 (product_data)
    # -------------------------------------------------------
    prod_vectorstore = Chroma(
        persist_directory=str(config.DB_DIR), 
        collection_name="product_data", # ingest_data.py와 일치해야 함
        embedding_function=embeddings
    )
    
    prod_metadata = [
        AttributeInfo(name="product_name", description="건강기능식품 상품명", type="string"),
        AttributeInfo(name="price", description="상품 가격 (원)", type="integer"),
        AttributeInfo(name="rating", description="평점 (0~5점)", type="float"),
    ]
    
    prod_retriever = SelfQueryRetriever.from_llm(
        llm,
        prod_vectorstore,
        "반려동물 건강기능식품 상품 정보",
        prod_metadata,
        verbose=True
    )

    # -------------------------------------------------------
    # 3. 두 Retriever 통합 (MergerRetriever)
    # -------------------------------------------------------
    # 사용자의 질문이 들어오면 두 DB를 동시에 뒤져서 결과를 합칩니다.
    print("🔗 의약품 및 상품 DB 통합 중...")
    _retriever = MergerRetriever(retrievers=[med_retriever, prod_retriever])
    
    print("✅ 통합 Retriever 준비 완료 (의약품 + 상품)")
    return _retriever
