# llm_rag/llm/llm_loader.py

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import config

_llm_instance = None

def get_llm():
    """
    LangChain과 호환되는 Google Gemini LLM 인스턴스 반환
    Self-Query Retriever에서 사용
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=0.3,
        )
    return _llm_instance
