# llm_rag/config.py


from pathlib import Path
import os
import dotenv

# .env 파일에서 환경 변수 로드
dotenv.load_dotenv()

# 이 파일(config.py)의 위치를 기준으로 프로젝트 루트를 계산합니다.
# llm_rag -> SWE_PROJECT
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Embedding
EMBEDDING_MODEL = 'jhgan/ko-sbert-nli'

# Vector DB
DB_DIR = PROJECT_ROOT / 'persistent_chroma_db' 

# LLM
LLM_MODEL = "gemini-2.5-flash"

# LLM API KEY
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
