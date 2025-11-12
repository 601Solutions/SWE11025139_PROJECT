#====================================================
# Author: 601 Solutions
# Title: rag_pipeline.py
# llm을 langchain과 호환되도록 변환 후 load하는 코드
#====================================================


from langchain.chains import RetrievalQA
from .llm.llm_loader import get_llm
from .retriever.retriever import get_rag_retriever
from .llm.prompt_templates import QA_CHAIN_PROMPT

_rag_chain = None

def get_rag_chain():
   
    global _rag_chain
    if _rag_chain is not None:
        return _rag_chain
        
    print("🔄 RAG 파이프라인 구성 중...")
    llm = get_llm()
    retriever = get_rag_retriever()
    
    if llm is None or retriever is None:
        print("❌ 오류: LLM 또는 Retriever 초기화 실패.")
        return None
        
    _rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    print("✅ RAG 질의응답 시스템이 준비되었습니다.\n")
    return _rag_chain
