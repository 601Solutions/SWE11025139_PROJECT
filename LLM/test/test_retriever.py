#====================================================
# Author: 601 Solutions
# Title: test_retriever.py
# Retriever 테스트
#====================================================

import os
import sys

# Add the LLM directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
llm_dir = os.path.dirname(current_dir)
sys.path.append(llm_dir)

from llm_rag.retriver.retriever import get_rag_retriever

import time

def run_test_case(tc_id, description, query, time_limit_sec, check_func=None):
    print("--------------------------------------------------")

    print(f"\n=== TC {tc_id}: {description} ===")
    retriever = get_rag_retriever()
    if retriever is None:
        print("Retriever 초기화 실패")
        return False

    start = time.time()
    try:
        docs = retriever.invoke(query)
        elapsed = time.time() - start
        if elapsed > time_limit_sec:
            print(f"FAIL: 제한 시간 {time_limit_sec}s 초과 ({elapsed:.2f}s)")
            return False

        if check_func:
            if not check_func(docs):
                print("FAIL: 결과 검증 실패")
                return False

        print(f"PASS ({elapsed:.2f}s)")
        return True

    except Exception as e:
        print(f"ERROR: {e}")
        return False


def check_non_empty(docs):
    return len(docs) > 0


def main():
    tests = [
        ("R3-1", "단순 용법 검색 (Baseline)", "넥스가드 스펙트라 투여 주기가 어떻게 돼?", 30, check_non_empty),
        ("R3-2", "체중 기반 용량 계산 (High Load)", "우리 강아지한테 아포퀠몇 mg 먹여야 해?", 30, check_non_empty),
        ("R3-3", "다중 조건/금기 검색 (Filter)", "임신 중인 3살 리트리버(전혁건)인데,구충제 파나쿠어 먹여도 안전해?", 30, check_non_empty),
        ("R3-4", "긴 증상 텍스트 분석 (Long Context)",
         "3일 전부터 사료 거부, 어제는 노란 토 2회, 오늘은 설사함. 활력은 좀 떨어짐... 이거 무슨 병일까?", 30, check_non_empty),
        ("R3-5", "오타/유의어 처리 속도", "프론트라인대신프로트라인 써도 진드기 죽어?", 30, check_non_empty),
        ("R3-6", "연속 질문 (캐싱 효율)", "그럼20kg는 얼마나 먹여?", 30, check_non_empty),
    ]

    for tc_id, desc, query, limit, check in tests:
        run_test_case(tc_id, desc, query, limit, check)


if __name__ == "__main__":
    main()
