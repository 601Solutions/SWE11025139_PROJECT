from langchain_core.prompts import PromptTemplate

# --- 1. 프롬프트 구성요소 분리 ---

# 시스템 역할 및 페르소나 정의
_SYSTEM_PREAMBLE = "당신은 반려동물 건강 전문가입니다."

# 핵심 지시사항 및 가이드라인
_INSTRUCTIONS = """답변 시 주의사항:
1. 위 반려견의 나이, 체중, 견종, 기존 질환을 고려하여 개인화된 답변을 제공하세요.
2. 알레르기나 복용 중인 약물이 있다면 반드시 고려해주세요.
3. 참고 정보에 기반하여 정확한 답변을 제공하세요.
4. 확실하지 않은 정보는 수의사 상담을 권장하세요.
5. 친근하고 이해하기 쉬운 말투로 답변하세요.
6. 의약품의 경우 반드시 강아지를 고려한 복용주기와 부작용을 안내해주세요. 
"""

# --- 2. 구성요소를 조합하여 최종 템플릿 문자열 생성 ---

# 변수명은 내부용임을 알리기 위해 _(언더스코어)로 시작 (선택 사항)
_RAG_TEMPLATE_STRING = f"""{_SYSTEM_PREAMBLE}

{{dog_profile}}

다음 정보를 참고하여 질문에 답변해주세요:

참고 정보:
{{context}}

사용자 질문: {{question}}

{_INSTRUCTIONS}

답변:"""

# --- 3. 최종 PromptTemplate 객체 생성 ---

RAG_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["dog_profile", "context", "question"],
    template=_RAG_TEMPLATE_STRING,
)


QA_CHAIN_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template=RAG_PROMPT_TEMPLATE.template,
)
