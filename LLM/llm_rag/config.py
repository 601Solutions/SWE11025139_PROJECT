#====================================================
# Author: 601 Solutions
# Title: config.py
# 핵심 변수 설정 정의
#====================================================

"""
프로젝트 전반에서 사용되는 핵심 설정 변수를 정의

- 프로젝트 루트 경로
- .env 파일 로드
- 임베딩 및 LLM 모델 이름
- Vector DB 경로
- API 키
"""

from pathlib import Path
import os
import dotenv

dotenv.load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EMBEDDING_MODEL = "jhgan/ko-sbert-nli"
DB_DIR = PROJECT_ROOT / 'persistent_chroma_db' 
LLM_MODEL = "gemini-2.5-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
