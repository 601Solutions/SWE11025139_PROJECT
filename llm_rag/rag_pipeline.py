# llm_rag/rag_pipeline.py

from .retriever.retriever import retrieve_context
from .llm.llm_response import generate_response

def ask(question: str):
    """
    사용자 질문에 대해 RAG 파이프라인을 실행합니다.
    (Retrieve -> Generate)
    """
    print(f"🔄 질문 처리 중: \"{question}\"")
    
    # 1. Retrieve: 관련 문서 및 컨텍스트 검색
    print("🔍 문서를 검색합니다...")
    context_str, sources = retrieve_context(question, k=5)
    
    if "Error:" in context_str:
        print(f"오류: {context_str}")
        return
    
    print("✅ 문서 검색 완료.")
    
    # 2. Generate: LLM에 답변 요청
    print("🤖 답변을 생성합니다...")
    answer = generate_response(context_str, question)
    print("✅ 답변 생성 완료.")
    
    return answer, context_str # 원본 스크립트처럼 답변과 컨텍스트 반환

# --- 이 파일을 직접 실행할 때 테스트 (원본 스크립트의 main 부분) ---
if __name__ == "__main__":
    test_question = "강아지 피부가 건조한데 오메가3 영양제 추천해줘"
    
    final_answer, context = ask(test_question)
    
    print("\n" + "="*50)
    print(f"질문: {test_question}")
    print(f"\n답변:\n{final_answer}")
    print(f"\n[참고한 자료]\n{context}")
    print("="*50)