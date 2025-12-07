#====================================================
# Author: 601 Solutions
# Title: vectorstore_chroma.py
# ChromaDB 벡터 저장소 클라이언트 및 컬렉션 관리
#====================================================


import chromadb
from .. import config

_client = None
_collection = None

def get_vector_collection():
    """
    설정된 ChromaDB 컬렉션 로드하여 반환

    Returns:
        chromadb.Collection | None:
        성공 시 ChromaDB 객체
        실패 시 None
    """
    global _client, _collection
    if _collection is None:
        if _client is None:
            _client = chromadb.PersistentClient(path=config.CHROMA_DB_PATH)
        
        try:
            _collection = _client.get_collection(name=config.COLLECTION_NAME)
            print(f"Vector collection '{config.COLLECTION_NAME}' loaded.")
        except Exception as e:
            print(f"컬렉션 로드 실패: {e}")
            print(f"'{config.COLLECTION_NAME}' 컬렉션을 찾을 수 없습니다.")
            print("먼저 'ingest_data.py' 스크립트를 실행하여 데이터를 주입하세요.")
            return None
            
    return _collection
