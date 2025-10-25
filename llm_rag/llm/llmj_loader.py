# llm_rag/llm/llm_loader.py
from langchain_google_genai import ChatGoogleGenerativeAI
from .. import config

_llm_model = None

def get_llm():

    global _llm_model
    if _llm_model is None:
        print("myPets LLM 로딩 중...")
        _llm_model = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            temperature=0.1,
            convert_system_message_to_human=True
        )
    return _llm_model