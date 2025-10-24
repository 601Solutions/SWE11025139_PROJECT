import pandas as pd
import os
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
# ✅ Gemini 모델을 위한 클래스를 불러옵니다.
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# --- 0. Google AI API 키 설정 ---
# 터미널에서 Google AI API 키를 환경 변수로 설정해야 합니다.
# export GOOGLE_API_KEY="AIza..."

if "GOOGLE_API_KEY" not in os.environ:
    print("❌ 오류: GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
    exit()

# --- 1. 데이터 로딩 및 가공 (이전과 동일) ---
CSV_FILE_PATH = 'lifet_products_final.csv'
try:
    df = pd.read_csv(CSV_FILE_PATH)
    print(f"✅ '{CSV_FILE_PATH}' 파일 로딩 성공! ({len(df)}개 상품)")
except FileNotFoundError:
    print(f"❌ 오류: '{CSV_FILE_PATH}' 파일을 찾을 수 없습니다.")
    exit()

documents = []
for index, row in df.iterrows():
    content = f"상품명은 '{row['NAME']}'이며, 가격은 {row['PRICE']}원입니다. 현재 리뷰 수는 {row['REVIEW_COUNT']}개, 평균 평점은 {row['RATING_AVG']}점입니다."
    doc = Document(page_content=content, metadata={'product_code': row['PRODUCT_CODE']})
    documents.append(doc)
print(f"✅ {len(documents)}개의 상품 정보를 Document 형식으로 변환했습니다.")


# --- 2. 임베딩 모델 및 벡터 DB(ChromaDB) 설정 (이전과 동일) ---
print("\n임베딩 모델을 로딩합니다...")
model_name = "jhgan/ko-sbert-nli" 
embeddings = HuggingFaceEmbeddings(model_name=model_name)
print("✅ 임베딩 모델 로딩 완료!")

db_directory = 'chroma_db'
vectorstore = Chroma.from_documents(
    documents, 
    embeddings, 
    persist_directory=db_directory
)
print(f"✅ 상품 정보를 벡터화하여 ChromaDB에 저장했습니다.")


# --- 3. Gemini LLM 및 RAG 체인 설정 ---
# ✅ Google Gemini 모델을 로딩합니다.
# model="gemini-pro"는 텍스트 생성에 최적화된 모델입니다.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro",
                             temperature=0.1,
                             convert_system_message_to_human=True) # 시스템 메시지를 지원하도록 설정

# RAG 체인 생성 (이전과 동일)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
print("RAG 질의응답 시스템이 준비되었습니다.\n")

# --- 4. 추천 알고리즘 테스트 ---
query = "우리 강아지가 7살인데 슬개골이 안 좋아. 관절에 좋은 영양제 추천해 줘."
print(f"💬 사용자 질문: {query}")

response = qa_chain.invoke(query)

print("\n🤖 AI 추천 답변:")
print(response['result'])