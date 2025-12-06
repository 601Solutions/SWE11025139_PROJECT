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
        return

    # 1. 일반적인 검색 예시
    print("\n=== 일반 검색 예시 ===")
    query = "강아지 관절 건강에 좋은 제품 알려주세요"
    docs = retriever.get_relevant_documents(query)
    for i, doc in enumerate(docs, 1):
        print(f"\n검색결과 {i}:")
        print(f"내용: {doc.page_content[:200]}...")
        print(f"제품명: {doc.metadata.get('product_name', 'N/A')}")
        print(f"출처: {doc.metadata.get('source_type', 'N/A')}")

    # 2. 특정 제품 검색 예시
    print("\n=== 특정 제품 검색 예시 ===")
    specific_query = "더 릴렉스라는 제품에 대해 알려주세요"
    specific_docs = retriever.get_relevant_documents(specific_query)
    for i, doc in enumerate(specific_docs, 1):
        print(f"\n검색결과 {i}:")
        print(f"제품명: {doc.metadata.get('product_name', 'N/A')}")
        print(f"내용: {doc.page_content[:200]}...")

    # 3. 건강기능식품만 검색 예시
    print("\n=== 건강기능식품 검색 예시 ===")
    supplement_query = "반려동물용 건강기능식품 중에서 면역력 강화에 좋은 제품 추천"
    supplement_docs = retriever.get_relevant_documents(supplement_query)
    for i, doc in enumerate(supplement_docs, 1):
        print(f"\n검색결과 {i}:")
        print(f"제품명: {doc.metadata.get('product_name', 'N/A')}")
        print(f"출처: {doc.metadata.get('source_type', 'N/A')}")
        print(f"내용: {doc.page_content[:200]}...")

if __name__ == "__main__":
    main()
