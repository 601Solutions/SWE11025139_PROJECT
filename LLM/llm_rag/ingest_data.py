# ingest_data.py
# (llm_rag 폴더 밖에 위치)

import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb
import time

CSV_FILE_PATH = './animal_medicine_data_full.csv'
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "pet_medicine"
EMBEDDING_MODEL_NAME = 'ko-sbert-v1'
BATCH_SIZE = 100

def main():
    print("데이터 주입(Ingestion) 스크립트를 시작합니다...")
    
    # 1. 데이터 로드
    try:
        df = pd.read_csv(CSV_FILE_PATH)
    except FileNotFoundError:
        print(f"오류: '{CSV_FILE_PATH}' 파일을 찾을 수 없습니다.")
        return

    # 2. 임베딩할 텍스트 결합 (원본 로직과 동일)
    df['combined_info'] = df.apply(
        lambda row: f"제품명: {row['product_name']}\n"
                    f"효능효과: {row['efficacy']}\n"
                    f"용법용량: {row['dosage']}\n"
                    f"주의사항: {row['precautions']}",
        axis=1
    )
    df_cleaned = df.dropna(subset=['combined_info'])
    
    # 3. 임베딩 모델 로드
    print(f"'{EMBEDDING_MODEL_NAME}' 모델을 로드합니다...")
    model = SentenceTransformer(EMBEDDING_MODEL_NAME, device='cuda')

    # 4. ChromaDB 클라이언트 연결
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    # 5. 문서, 메타데이터, ID 준비
    documents = df_cleaned['combined_info'].tolist()
    metadatas = df_cleaned.apply(
        lambda row: {
            'product_name': row['product_name'],
            'efficacy': row['efficacy'],
            'dosage': row['dosage'],
            'precautions': row['precautions']
        }, axis=1
    ).tolist()
    ids = [f"doc_{i}" for i in range(len(documents))]

    # 6. 데이터 일괄 주입 (배치 처리)
    print(f"총 {len(documents)}개의 문서를 ChromaDB에 주입합니다...")
    start_time = time.time()
    
    for i in range(0, len(documents), BATCH_SIZE):
        batch_docs = documents[i:i + BATCH_SIZE]
        batch_metas = metadatas[i:i + BATCH_SIZE]
        batch_ids = ids[i:i + BATCH_SIZE]
        
        # 임베딩 생성
        embeddings = model.encode(batch_docs)
        
        # DB에 추가
        collection.add(
            embeddings=embeddings.tolist(),
            documents=batch_docs,
            metadatas=batch_metas,
            ids=batch_ids
        )
        print(f"  > {i + len(batch_docs)} / {len(documents)} 처리 완료...")
    
    end_time = time.time()
    print(f"\n데이터 주입 완료! (총 {end_time - start_time:.2f}초 소요)")

if __name__ == "__main__":
    main()