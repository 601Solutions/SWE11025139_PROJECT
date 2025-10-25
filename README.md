## feature/LLM

- **Branch for LLM/RAG implementation and data preprocessing**

## 📂 프로젝트 구조

```plaintext
feature/LLM/
├── README.md            
│
├── data/                  # 데이터 관련
│   ├── raw/               # 원본 데이터 
│   ├── processed/         # 전처리된 데이터
│   ├── crawled/           # 웹 크롤링 결과
│   └── schema/            # DB 스키마 정의
│
├── database/              # DB 구축 코드
│   ├── create_tables.sql  # 테이블 생성 스크립트
│   ├── ingest_data.py     # DB 벡터 생성 스크립트
│   └── db_connection.py   # DB 연결 관리 코드
│
├── llm_rag/               # LLM + RAG 시스템
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
│   │   ├── llm_loader.py    # LLM 로드 모듈
│   │   ├── prompt_templates.py # 프롬프트 템플릿
│   │   └── llm_response.py    # 모델 응답 생성 로직
│   │
│   ├── rag_pipeline.py    # 전체 RAG 파이프라인 구성
│   └── config.py          # 모델/DB 설정값 모음
│
├── utils/                 # 공용 유틸리티
│   ├── __init__.py
│   ├── preprocess.py      # 데이터 전처리 공통 함수
│   ├── logger.py          # 로그 관리
│   └── helpers.py         # 기타 보조 함수
│
├── tests/                 #  테스트 코드
│   ├── __init__.py
│   ├── test_rag.py
│   └── test_database.py
│
├── .gitignore             # Git 추적 제외 파일
│
├── persistent_chroma_db/  # 생성된 벡터 DB (Git 추적 제외)
│
├── requirements.txt       # 필요 라이브러리
│
└── app/                   # RAG 질의응답 시스템 실행 부분
    ├── __init__.py
    ├── main.py            # RAG 시스템 실행 엔트리포인트
    └── api_routes.py      # API endpoint 관리

```

설치 방법
-------

1. Python 가상환경 생성 및 활성화

    conda create -n swe_project python=3.10
    conda activate swe_project

2. 필요 라이브러리 설치

    pip install -r requirements.txt

3. Google Gemini API Key 설정

    - Windows
        $env:GOOGLE_API_KEY = "your_api_key_here"
    
    - Linux/MacOS
        export GOOGLE_API_KEY="your_api_key_here"


시스템 실행 방법
------------

**이 시스템은 2단계로 실행됩니다.**

1. 벡터 DB 생성(최초 1회)
- 루트 폴더에서 database/ingest_data.py를 실행하여 persistent_chroma_db 생성

        python database/ingest_data.py

2. RAG 질의응답 시스템 실행
- DB 생성 완료 이후, app/main.py를 실행하여 RAG 시스템 시작

    python app/main.py

*실행 후, 터미널에서 바로 질문을 입력하여 사용할 수 있습니다.*



