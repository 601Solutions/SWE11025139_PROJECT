# llm_rag/retriever/retriever.py

from ..embeddings.embedder import get_embedding_model
from ..embeddings.vectorstore_chroma import get_vector_collection

def retrieve_context(query_text: str, k: int = 5):
    model = get_embedding_model()
    collection = get_vector_collection()
    
    if collection is None:
        return "Error: Vector DB Collection not found.", []

    # 1. 질문 임베딩
    query_embedding = model.encode(query_text)
    
    # 2. ChromaDB 쿼리
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=k
    )
    
    # 3. LLM에 전달할 컨텍스트 생성 (원본 로직과 동일)
    context_str = ""
    retrieved_metadatas = results['metadatas'][0]
    
    sources = [] # 근거 자료 추적
    
    for i, meta in enumerate(retrieved_metadatas):
        product_name = meta.get('product_name', 'N/A')
        efficacy = meta.get('efficacy', 'N/A')
        dosage = meta.get('dosage', 'N/A')
        
        context_str += f"문서 {i+1}:\n"
        context_str += f"  - 제품명: {product_name}\n"
        context_str += f"  - 효능효과: {efficacy}\n"
        context_str += f"  - 용법용량: {dosage}\n\n"
        
        sources.append(meta) # 메타데이터 전체를 소스로 추가
        
    return context_str, sources