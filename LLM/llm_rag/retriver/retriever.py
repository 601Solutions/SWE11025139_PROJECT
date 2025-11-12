# llm_rag/retriever/retriever.py
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains.query_constructor.base import AttributeInfo
from langchain_classic.retrievers.self_query.base import SelfQueryRetriever
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config
from llm.llmj_loader import get_llm 

_retriever = None

def get_rag_retriever():
    
    # ChromaDB와 SelfQueryRetriever 로드

    global _retriever
    if _retriever is not None:
        return _retriever

    # 1. 임베딩 모델 로드
    print("🔍 임베딩 모델 로딩 중...")
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    # 2. DB 불러오기
    print(f"📂 '{config.DB_DIR}'에서 벡터 DB 로딩 중...")
    if not os.path.exists(config.DB_DIR):
        print(f"❌ 오류: '{config.DB_DIR}' 폴더를 찾을 수 없습니다.")
        print("먼저 'database/ingest_data.py'를 실행하여 DB를 생성하세요.")
        return None

    vectorstore = Chroma(
        persist_directory=str(config.DB_DIR), 
        embedding_function=embeddings
    )

    # 3. Self-Query Retriever 설정 (정확한 제품명 검색용)
    metadata_field_info = [
        AttributeInfo(
            name="product_name",
            description="건강기능식품 또는 의약품의 제품명. (예: '더 릴렉스')",
            type="string",
        ),
        AttributeInfo(
            name="source_type",
            description="정보의 출처 ('건강기능식품' 또는 '동물용의약품')",
            type="string", 
        ),
    ]
    document_content_description = "반려동물 건강기능식품 또는 의약품의 상세 정보 (효능, 용법, 주의사항 등)"

    llm = get_llm() # Self-query를 위해 LLM 로드
    
    _retriever = SelfQueryRetriever.from_llm(
        llm,
        vectorstore,
        document_content_description,
        metadata_field_info,
        verbose=True 
    )
    
    print("✅ Self-Query Retriever (질문 모듈) 준비 완료.")
    return _retriever