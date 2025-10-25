# llm_rag/config.py


from pathlib import Path

# 이 파일(config.py)의 위치를 기준으로 프로젝트 루트를 계산합니다.
# llm_rag -> SWE_PROJECT
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Embedding
EMBEDDING_MODEL = 'jhgan/ko-sbert-nli'

# Vector DB
DB_DIR = PROJECT_ROOT / 'persistent_chroma_db' 

# LLM
LLM_MODEL = "gemini-2.5-flash"
