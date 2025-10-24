import pandas as pd
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAI

# --- 1단계: 데이터 로딩 및 '지식'으로 변환 ---
try:
    df = pd.read_csv('lifet_products_cleaned.csv')
    print("✅ 정제된 CSV 파일 로딩 성공!")

    # 각 행을 LangChain이 사용하는 Document 객체로 변환
    # page_content에 LLM이 이해할 자연어 문장을 넣는 것이 핵심
    documents = []
    for index, row in df.iterrows():
        content = f"상품명은 '{row['NAME']}'이고, 가격은 {row['PRICE']}원입니다."
        doc = Document(page_content=content)
        documents.append(doc)
    
    print(f"✅ {len(documents)}개의 상품 정보를 Document로 변환 완료!")
    # print("Document 예시:", documents[0]) # 첫 번째 Document 내용 확인

except FileNotFoundError:
    print("❌ 오류: 'lifet_products_cleaned.csv' 파일을 찾을 수 없습니다. 파일 이름을 확인해주세요.")
    exit()


# --- 2단계: 벡터 데이터베이스 구축 ---
# 한국어 문장을 벡터로 변환해주는 모델 로딩 (시간이 조금 걸릴 수 있음)
print("임베딩 모델을 로딩 중입니다...")
model_name = "jhgan/ko-sbert-nli"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
print("✅ 임베딩 모델 로딩 완료!")

# Document들을 벡터화하여 FAISS 데이터베이스에 저장
print("벡터 데이터베이스를 구축 중입니다...")
vectorstore = FAISS.from_documents(documents, embeddings)
print("✅ 벡터 데이터베이스 구축 완료!")


# --- 3단계: 질의응답(QA) 시스템 구현 ---
# OpenAI LLM 모델 로딩 (환경변수에 OPENAI_API_KEY가 설정되어 있어야 함)
try:
    llm = OpenAI(temperature=0) # temperature=0은 답변의 일관성을 높여줌
    print("✅ OpenAI LLM 로딩 성공!")
except Exception as e:
    print(f"❌ OpenAI LLM 로딩 실패: API 키를 확인해주세요. (오류: {e})")
    exit()

# RAG 체인 생성
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
print("✅ QA 시스템 준비 완료!")

# --- 시스템 테스트 ---
question = "아인솝 강아지 비누 가격 알려줘"
print(f"\n💬 질문: {question}")

# 질문에 대한 답변 생성
response = qa_chain.invoke(question)

print(f"🤖 답변: {response['result']}")