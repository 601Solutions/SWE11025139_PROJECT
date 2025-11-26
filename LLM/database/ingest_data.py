#====================================================
# Author: 601 Solutions
# Title: ingest_data.py
# 데이터 처리 및 저장 - 컬렉션 분리 및 안정성 강화 버전
#====================================================

import pandas as pd
import os
import chromadb
from langchain_core.documents import Document
from langchain_chroma import Chroma # 패키지명 확인
from langchain_huggingface import HuggingFaceEmbeddings # 최신 패키지 사용 권장

# ---------------------------------------------------
# 1. 경로 및 설정 정의
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SUPPLEMENT_CSV = os.path.normpath(os.path.join(BASE_DIR, '../data/processed/lifet_products_cleaned.csv'))
MEDICINE_CSV = os.path.normpath(os.path.join(BASE_DIR, '../data/raw/animal_medicine_dataset_full.csv'))
DB_DIR = os.path.normpath(os.path.join(BASE_DIR, '../persistent_chroma_db'))
EMBEDDING_MODEL = 'jhgan/ko-sbert-nli'

# ---------------------------------------------------
# 2. 데이터 로드 함수들
# ---------------------------------------------------
def load_supplements(filepath):
    """건강기능식품 데이터 로드 -> Document 변환"""
    if not os.path.exists(filepath):
        print(f"⚠️ 오류: '{filepath}' 파일이 없습니다.")
        return []
        
    try:
        # 인코딩 문제 방지 (utf-8-sig 권장)
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filepath, encoding='cp949') # 차선책
        
    df = df.fillna('')
    documents = []
    
    for _, row in df.iterrows():
        # 검색에 필요한 핵심 정보만 텍스트로 구성
        content = f"상품명: {row['NAME']}, 가격: {row['PRICE']}원, 평점: {row['RATING_AVG']}점"
        
        doc = Document(
            page_content=content, 
            metadata={
                'product_name': str(row['NAME']),
                'source_type': 'product', # 구분자 변경
                'price': int(row['PRICE']) if row['PRICE'] else 0, # 숫자형으로 변환 (필터링용)
                'rating': float(row['RATING_AVG']) if row['RATING_AVG'] else 0.0,
                'product_code': str(row['PRODUCT_CODE'])
            }
        )
        documents.append(doc)
        
    print(f"✅ 건강기능식품 {len(documents)}개 로드 완료.")
    return documents

def load_medicines(filepath):
    """동물용의약품 데이터 로드 -> Document 변환"""
    if not os.path.exists(filepath):
        print(f"⚠️ 오류: '{filepath}' 파일이 없습니다.")
        return []

    try:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
    except:
        df = pd.read_csv(filepath, encoding='cp949')

    # 필요한 컬럼만 추출
    cols = ['product_name', 'efficacy', 'dosage', 'precautions', 'item_seq', 'company_name']
    # 없는 컬럼이 있을 경우 방어 로직
    existing_cols = [c for c in cols if c in df.columns]
    df = df[existing_cols].fillna('')
    
    documents = []
    for _, row in df.iterrows():
        content = (
            f"제품명: {row.get('product_name', '')}\n"
            f"효능효과: {row.get('efficacy', '')}\n"
            f"용법용량: {row.get('dosage', '')}\n"
            f"주의사항: {row.get('precautions', '')}"
        )
        
        doc = Document(
            page_content=content, 
            metadata={
                'product_name': str(row.get('product_name', '')),
                'source_type': 'medicine',
                'company': str(row.get('company_name', '')),
                'item_seq': str(row.get('item_seq', ''))
            }
        )
        documents.append(doc)
        
    print(f"✅ 의약품 {len(documents)}개 로드 완료.")
    return documents

# ---------------------------------------------------
# 3. 메인 실행 로직 (핵심 수정 부분)
# ---------------------------------------------------
def main():
    # A. 데이터 로드
    product_docs = load_supplements(SUPPLEMENT_CSV)
    medicine_docs = load_medicines(MEDICINE_CSV)

    if not product_docs and not medicine_docs:
        print("❌ 저장할 데이터가 없습니다.")
        return

    # B. 임베딩 모델 로드
    print(f"\n🔄 임베딩 모델({EMBEDDING_MODEL}) 로딩 중...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # C. ChromaDB 클라이언트 설정 (오류 방지용)
    # Windows 환경에서 안전하게 동작하도록 설정 강제 주입
    client_settings = chromadb.config.Settings(
        is_persistent=True,
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )

    print(f"📂 '{DB_DIR}'에 저장 시작...")

    # D. 컬렉션 1: 상품 데이터 저장
    if product_docs:
        print(f"   -> [1/2] 상품 데이터 저장 중 ({len(product_docs)}개)...")
        Chroma.from_documents(
            documents=product_docs,
            embedding=embeddings,
            collection_name="product_data", # 별도 컬렉션
            persist_directory=DB_DIR,
            client_settings=client_settings
        )

    # E. 컬렉션 2: 의약품 데이터 저장
    if medicine_docs:
        print(f"   -> [2/2] 의약품 데이터 저장 중 ({len(medicine_docs)}개)...")
        Chroma.from_documents(
            documents=medicine_docs,
            embedding=embeddings,
            collection_name="medicine_data", # 별도 컬렉션
            persist_directory=DB_DIR,
            client_settings=client_settings
        )
    
    print("\n✨ 모든 데이터 저장이 완료되었습니다!")
    print("이제 서버를 실행하세요.")

if __name__ == "__main__":
    main()
