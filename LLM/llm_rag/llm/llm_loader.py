#====================================================
# Author: 601 Solutions
# Title: llm_loader.py
# llm을 langchain과 호환되도록 변환 후 load하는 코드
#====================================================

"""
Gemini LLM 모델 인스턴스를 관리

'get_llm' 함수를 통해 ChatGoogleGenerativeAI 객체를 API 키와 설정을 한 번만 로드
"""

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import sys
import config

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

_llm_instance = None

def get_llm():
    """
    Google Gemini API를 사용한 응답 생성
    """
    
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatGoogleGenerativeAI(
            model=config.LLM_MODEL,
            google_api_key=config.GOOGLE_API_KEY,
            temperature=0.3,
        )
    return _llm_instance
