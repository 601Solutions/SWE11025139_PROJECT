#====================================================
# Author: 601 Solutions
# Title: test_llm.py
# LLM 테스트
#====================================================

import os
import sys
import traceback
# Add the LLM directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
llm_dir = os.path.dirname(current_dir)
sys.path.append(llm_dir)

from llm_rag.retriever.retriever import get_rag_retriever
from llm_rag.llm.llm_response import generate_response
from llm_rag import config


def test_rag_pipeline():
    """
    RAG 파이프라인 전체 테스트
    1. Retriever로 관련 문서 검색
    2. LLM으로 답변 생성
    """
    print("=" * 60)
    print("RAG 시스템 테스트 시작")
    print("=" * 60)
    
    # 1. Retriever 초기화
    print("\nStep 1: Retriever 초기화 중...")
    retriever = get_rag_retriever()
    
    if retriever is None:
        print("Retriever 초기화 실패!")
        print("먼저 'database/ingest_data.py'를 실행하여 DB를 생성하세요.")
        return
    
    # 2. 테스트 질문들
    test_questions = [
        "강아지 관절 건강에 좋은 제품이 뭐가 있나요?",
        "더 릴렉스라는 제품에 대해 알려주세요",
        "피부가 가려운 강아지에게 줄 수 있는 의약품은?",
        "노령견에게 좋은 영양제 추천해주세요",
    ]
    
    # 3. 각 질문에 대해 RAG 실행
    for idx, question in enumerate(test_questions, 1):
        print("\n" + "=" * 60)
        print(f"질문 {idx}: {question}")
        print("=" * 60)
        
        # 3-1. 관련 문서 검색
        print("\n관련 문서 검색 중...")
        try:
            retrieved_docs = retriever.invoke(question)
            
            print(f"{len(retrieved_docs)}개의 관련 문서를 찾았습니다.\n")
            
            # 검색된 문서 출력
            for i, doc in enumerate(retrieved_docs[:3], 1):  # 상위 3개만
                print(f"문서 {i}:")
                print(f"   내용: {doc.page_content[:200]}...")
                if doc.metadata:
                    print(f"   메타데이터: {doc.metadata}")
                print()
            
            # 3-2. Context 생성
            context = "\n\n".join([doc.page_content for doc in retrieved_docs[:5]])
            
            # 3-3. LLM 응답 생성
            print("LLM 응답 생성 중...")
            response = generate_response(context, question)
            
            print("\nAI 답변:")
            print("-" * 60)
            print(response)
            print("-" * 60)
            
        except Exception as e:
            print(f"오류 발생: {e}")
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("RAG 시스템 테스트 완료!")
    print("=" * 60)


def test_retriever_only():
    """
    Retriever만 단독 테스트
    """
    print("=" * 60)
    print("Retriever 단독 테스트")
    print("=" * 60)
    
    retriever = get_rag_retriever()
    
    if retriever is None:
        print("Retriever 초기화 실패!")
        return
    
    # 테스트 질문
    question = "강아지 관절 건강에 좋은 제품이 뭐가 있나요?"
    print(f"\n질문: {question}\n")
    
    try:
        # 문서 검색
        docs = retriever.invoke(question)
        
        print(f"{len(docs)}개의 문서를 찾았습니다.\n")
        
        for i, doc in enumerate(docs, 1):
            print(f"문서 {i}:")
            print(f"   내용: {doc.page_content[:300]}...")
            print(f"   메타데이터: {doc.metadata}")
            print()
            
    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc()


def test_llm_only():
    """
    LLM만 단독 테스트 (RAG 없이)
    """
    print("=" * 60)
    print("LLM 단독 테스트")
    print("=" * 60)
    
    question = "강아지 건강 관리에 대해 알려주세요"
    context = "반려동물의 건강을 위해서는 정기적인 운동, 균형잡힌 식사, 정기 건강검진이 중요합니다."
    
    print(f"\n질문: {question}")
    print(f"Context: {context}\n")
    
    try:
        response = generate_response(context, question)
        print("AI 답변:")
        print("-" * 60)
        print(response)
        print("-" * 60)
    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc()


def interactive_mode():
    """
    대화형 모드 - 사용자가 직접 질문 입력
    """
    print("=" * 60)
    print("RAG 대화형 모드")
    print("종료하려면 'quit' 또는 'exit' 입력")
    print("=" * 60)
    
    retriever = get_rag_retriever()
    
    if retriever is None:
        print("Retriever 초기화 실패!")
        return
    
    print("\n준비 완료! 질문을 입력하세요.\n")
    
    while True:
        try:
            question = input("질문: ").strip()
            
            if question.lower() in ['quit', 'exit', '종료', 'q']:
                print("\n프로그램을 종료합니다.")
                break
            
            if not question:
                continue
            
            print("\n검색 중...")
            docs = retriever.invoke(question)
            context = "\n\n".join([doc.page_content for doc in docs[:5]])
            
            print("답변 생성 중...\n")
            response = generate_response(context, question)
            
            print("AI 답변:")
            print("-" * 60)
            print(response)
            print("-" * 60)
            print()
            
        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}")


if __name__ == "__main__":
    print("\n펫 헬스케어 AI 챗봇 - RAG 시스템 테스트\n")
    print("테스트 모드를 선택하세요:")
    print("1. 전체 RAG 파이프라인 테스트")
    print("2. Retriever만 테스트")
    print("3. LLM만 테스트")
    print("4. 대화형 모드 (직접 질문)")
    
    choice = input("\n선택 (1-4): ").strip()
    
    if choice == "1":
        test_rag_pipeline()
    elif choice == "2":
        test_retriever_only()
    elif choice == "3":
        test_llm_only()
    elif choice == "4":
        interactive_mode()
    else:
        print("잘못된 선택입니다. 1-4 중 선택하세요.")
