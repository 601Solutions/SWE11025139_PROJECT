## feature/LLM

- **Branch for LLM/RAG implementation and data preprocessing**

## 📂 프로젝트 구조

```plaintext
feature/LLM/
├── README.md            # 이 브랜치 전용 설명 (개발 목적, 실행 방법 등)
│
├── data/                  # 💾 데이터 관련
│   ├── raw/               # 원본 데이터 (ex. CSV, JSON, XLSX)
│   ├── processed/         # 전처리된 데이터
│   ├── crawled/           # 웹 크롤링 결과
│   └── schema/            # DB 스키마 정의(SQL, ERD 등)
│
├── database/              # 🧩 DB 구축 코드
│   ├── create_tables.sql  # 테이블 생성 스크립트
│   ├── insert_data.py     # 데이터 삽입용 스크립트
│   └── db_connection.py   # DB 연결 관리 코드
│
├── llm_rag/               # 🧠 LLM + RAG 시스템
│   ├── __init__.py        # (패키지 인식용)
│   ├── embeddings/        # 임베딩 관련 코드
│   │   ├── __init__.py
│   │   ├── embedder.py        # SentenceTransformer 등 임베딩 생성
│   │   └── vectorstore_chroma.py # ChromaDB 관련 코드
│   │
│   ├── retriever/         # 문서 검색/검색 파이프라인
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   └── similarity_search.py
│   │
│   ├── llm/               # LLM 관련 코드
│   │   ├── __init__.py
│   │   ├── llm_response.py    # 모델 응답 생성 로직
│   │   └── prompt_templates.py # 프롬프트 템플릿
│   │
│   ├── rag_pipeline.py    # 전체 RAG 파이프라인 구성
│   └── config.py          # 모델/DB 설정값 모음
│
├── utils/                 # ⚙️ 공용 유틸리티
│   ├── __init__.py
│   ├── preprocess.py      # 데이터 전처리 공통 함수
│   ├── logger.py          # 로그 관리
│   └── helpers.py         # 기타 보조 함수
│
├── tests/                 # 🧪 테스트 코드
│   ├── __init__.py
│   ├── test_rag.py
│   └── test_database.py
│
└── app/                   # 🚀 (선택) RAG 질의응답 시스템 실행 부분
    ├── __init__.py
    ├── main.py            # Streamlit / Flask 등 실행 엔트리포인트
    └── api_routes.py      # API endpoint 관리