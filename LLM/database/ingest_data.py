#====================================================
# Author: 601 Solutions
# Title: ingest_data.py
# 데이터 처리 및 저장
#====================================================

import pandas as pd
import os
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


SUPPLEMENT_CSV = 'data/processed/lifet_products_cleaned.csv'
MEDICINE_CSV = 'data/raw/animal_medicine_data_sample.csv'
EMBEDDING_MODEL = 'jhgan/ko-sbert-nli'
DB_DIR = 'persistent_chroma_db' # DB가 저장


def load_and_process_supplements(filepath):
    """
    CSV 파일에서 건강기능식품 데이터를 로드하여 LangChain Document 객체 리스트로 변환.

    Args:
        filepath (str): 로드할 건강기능식품 CSV 파일 경로.

    Returns:
        list[Document]: 변환된 Document 객체의 리스트.
    """
    #건강기능식품 처리
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"오류: '{filepath}' 파일을 찾을 수 없습니다.")
        return []
        
    df = df.fillna('') # 결측치 처리
    documents = []
    for index, row in df.iterrows():
        content = f"상품명: {row['NAME']}, 가격: {row['PRICE']}원, 리뷰 수: {row['REVIEW_COUNT']}개, 평점: {row['RATING_AVG']}점."
        doc = Document(
            page_content=content, 
            metadata={
                'product_name': str(row['NAME']), # 검색을 위해 필드명 통일
                'source_type': '건강기능식품',
                'product_code': str(row['PRODUCT_CODE'])
            }
        )
        documents.append(doc)
    print(f"건강기능식품 {len(documents)}개 로드 완료.")
    return documents

def load_and_process_medicines(filepath):
    """
    CSV 파일에서 동물용의약품 데이터를 로드하여 LangChain Document 객체 리스트로 변환.

    Args:
        filepath (str): 로드할 동물용의약품 CSV 파일 경로.

    Returns:
        list[Document]: 변환된 Document 객체의 리스트.
    """
    #의약품 처리
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"오류: '{filepath}' 파일을 찾을 수 없습니다.")
        return []

    cols_to_fill = ['product_name', 'efficacy', 'dosage', 'precautions', 'item_seq']
    df = df[cols_to_fill].fillna('') # 결측치 처리
    
    documents = []
    for index, row in df.iterrows():
        content = (
            f"제품명: {row['product_name']}\n"
            f"효능효과: {row['efficacy']}\n"
            f"용법용량: {row['dosage']}\n"
            f"주의사항: {row['precautions']}"
        )
        doc = Document(
            page_content=content, 
            metadata={
                'product_name': str(row['product_name']), # ⬅️ 검색을 위해 필드명 통일
                'source_type': '동물용의약품',
                'item_seq': str(row['item_seq'])
            }
        )
        documents.append(doc)
    print(f"의약품 {len(documents)}개 로드 완료.")
    return documents

def main():
    """
    데이터 로드, 임베딩, Chroma 벡터 DB 생성 및 저장을 위한 메인 파이프라인을 실행.

    Args:
        None

    Returns:
        None (콘솔에 진행 상황 및 결과를 출력.)
    """
    # 1. 두 CSV 파일에서 모든 Document 로드
    all_documents = []
    all_documents.extend(load_and_process_supplements(SUPPLEMENT_CSV))
    all_documents.extend(load_and_process_medicines(MEDICINE_CSV))

    if not all_documents:
        print("처리할 문서가 없습니다. CSV 파일 경로를 확인하세요.")
        return

    # 2. 임베딩 모델 로드
    print(f"\n임베딩 모델({EMBEDDING_MODEL}) 로딩 중...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    print("임베딩 모델 로딩 완료!")

    # 3. Chroma.from_documents로 DB 생성 및 저장
    print(f"'{DB_DIR}' 폴더에 벡터 DB를 생성 및 저장합니다...")
    vectorstore = Chroma.from_documents(
        all_documents, 
        embeddings, 
        persist_directory=DB_DIR  # ⬅️ 이 폴더에 영구 저장
    )
    
    print(f"\n총 {len(all_documents)}개의 문서가 '{DB_DIR}'에 성공적으로 저장되었습니다.")
    print("이제 RAG 시스템을 사용할 수 있습니다.")

if __name__ == "__main__":
    main()
