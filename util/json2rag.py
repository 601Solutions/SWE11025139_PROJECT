from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import json

# 1. 문서 적재
records = []
with open("util/animal_medicine.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        # 각 줄을 json으로 파싱해 dict로
        record = json.loads(line.strip())
        records.append(record)
docs = [Document(page_content=str(r), metadata=r) for r in records]

# 2. 텍스트 분할 (너무 짧으면 생략 가능)
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
split_docs = splitter.create_documents([str(doc) for doc in docs])

# 3. 임베딩 모델 준비
embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large-instruct")

# 4. 벡터DB로 저장 (Chroma)
persist_directory = "DB/chroma_medicine_db"  # 저장 폴더명
vectorstore = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory=persist_directory
)
vectorstore.persist()  # 실제 파일로 DB 저장(폴더 생김)

print("RAG 인덱스와 벡터 DB 파일이", persist_directory, "폴더에 생성되었습니다.")
