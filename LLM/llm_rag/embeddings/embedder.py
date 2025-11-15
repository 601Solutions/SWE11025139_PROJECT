#====================================================
# Author: 601 Solutions
# Title: embedder.py
# SentenceTransformer 임베딩 모델 로드 및 관리
#====================================================


from sentence_transformers import SentenceTransformer
from .. import config

_embedding_model = None

def get_embedding_model():
    """
    설정된 임베딩 모델 로드하여 반환

    Returns:
        SentenceTransformer: 로드된 임베딩 모델 객체
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            config.EMBEDDING_MODEL_NAME,
            device=config.EMBEDDING_DEVICE
        )
        print(f"Embedding model '{config.EMBEDDING_MODEL_NAME}' loaded.")
    return _embedding_model
