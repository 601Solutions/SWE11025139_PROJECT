# app_text_input.py
import streamlit as st
from chat_scenarios_keyword import conversation

def show_chatbot_page():
    st.set_page_config(page_title="멍멍닥터 챗봇", page_icon="🐾")

    # 세션 상태 변수 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = "start"

    st.title("🐾 멍멍닥터: 강아지 건강 어드바이스 Demo")
    st.markdown("---")

    # 메시지 출력 함수
    def show_message(role, content, image=None):
        with st.chat_message(role):
            st.markdown(content)
            if image is not None:
                st.image(image, width=200)

    # 대화 기록 출력
    for message in st.session_state.messages:
        show_message(message["role"], message["content"], message.get("image"))

    # 단계별 메시지 출력(중복 방지)
    def add_bot_message(step_data):
        bot_message_content = step_data["message"]
        image = step_data.get("image")
        # 마지막 메시지와 다를 때만 추가
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != bot_message_content:
            show_message("assistant", bot_message_content, image)
            data = {"role": "assistant", "content": bot_message_content}
            if image:
                data["image"] = image
            st.session_state.messages.append(data)

    step_data = conversation[st.session_state.current_step]
    add_bot_message(step_data)

    # 사용자 입력 처리 함수
    def process_user_input(user_input):
        options = conversation[st.session_state.current_step].get("options", {})
        next_step = None
        # 옵션이 있는 단계라면 해당 키워드 매칭
        for key, keywords in options.items():
            if any(keyword in user_input for keyword in keywords):
                next_step = key
                break
        # 매칭되는 옵션이 있을 때
        if next_step:
            st.session_state.current_step = next_step
        else:
            # 옵션이 없거나, 옵션에 포함되지 않은 입력일 때
            if options:
                error_msg = "죄송해요, 잘 이해하지 못했어요. '영양제', '피부'처럼 키워드로 다시 말씀해주시겠어요?"
            else:
                error_msg = "감사합니다. 추가 궁금하신 점이 있으면 언제든 말씀해주세요!"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

    # 사용자 입력폼
    if prompt := st.chat_input("여기에 메시지를 입력하세요."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        show_message("user", prompt)
        process_user_input(prompt.lower())
        st.rerun()