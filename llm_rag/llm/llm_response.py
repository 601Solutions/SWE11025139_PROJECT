# llm_rag/llm/llm_response.py

from google.generativeai import genai
from .. import config
from .prompt_templates import RAG_PROMPT_TEMPLATE

_llm_client = None

def get_llm_client():

    global _llm_client
    if _llm_client is None:
        _llm_client = genai(api_key=config.GOOGLE_API_KEY)
    return _llm_client

def generate_response(context: str, question: str) -> str:

    client = get_llm_client()
    
    prompt = RAG_PROMPT_TEMPLATE.format(context=context, question=question)
    
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL_ID,
            messages=[
                {"role": "system", "content": "당신은 전문 수의사입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM API 호출 오류: {e}")
        return "답변을 생성하는 중 오류가 발생했습니다."