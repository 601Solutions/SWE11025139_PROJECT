# llm_rag/embeddings/embedder.py

from sentence_transformers import SentenceTransformer
from .. import config

_embedding_model = None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(
            config.EMBEDDING_MODEL_NAME,
            device=config.EMBEDDING_DEVICE
        )
        print(f"Embedding model '{config.EMBEDDING_MODEL_NAME}' loaded.")
    return _embedding_model