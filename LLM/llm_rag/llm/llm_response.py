#====================================================
# Author: 601 Solutions
# Title: llm_response.py
# llm 응답 생성 코드
#====================================================


import google.generativeai as genai
import os
import sys
import config
from .prompt_templates import RAG_PROMPT_TEMPLATE


sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
_llm_client = None

def get_llm_client():
    global _llm_client
    if _llm_client is None:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        _llm_client = genai.GenerativeModel(config.LLM_MODEL)
    return _llm_client


def generate_response(context: str, question: str, dog_profile: str = "") -> str:
    """
    Google Gemini API를 사용한 응답 생성
    
    Args:
        context: 검색된 문서 컨텍스트
        question: 사용자 질문
        dog_profile: 강아지 프로필 정보 (선택)
    """
    client = get_llm_client()
    
    # 프롬프트 생성
    prompt = RAG_PROMPT_TEMPLATE.format(
        dog_profile=dog_profile if dog_profile else "반려견 정보가 등록되지 않았습니다.",
        context=context,
        question=question
    )
    
    try:
        response = client.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
            )
        )
        return response.text
    except Exception as e:
        print(f"LLM API 호출 오류: {e}")
        return "답변을 생성하는 중 오류가 발생했습니다."