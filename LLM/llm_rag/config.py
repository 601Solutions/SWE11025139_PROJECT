# llm_rag/config.py

# Embedding
EMBEDDING_MODEL_NAME = 'ko-sbert-v1'
EMBEDDING_DEVICE = 'cuda'

# Vector DB
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "pet_medicine"

# LLM
GOOGLE_API_KEY = 'my-api-key'
LLM_MODEL_ID = "gemini-2.5-flash"