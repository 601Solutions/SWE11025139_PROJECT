import streamlit as st
from chat_scenarios_keyword import conversation

# Utils (FastAPI)
import requests, json

## http API 호출 주소 및 포트(포트는 변경 가능)
_URL = "http://127.0.0.1:8000"

def get_message(input_message: str) -> str:

    # 요청 호출 및 답변 불러오기
    try:
        response = requests.post(
            _URL + "/conversation",
            json={
                "message": input_message,
            }
        )
        
        # 통신 예외처리
        if response.status_code == 200:
            data = response.json()
            print(data) # Debug
            return data['message']

        else:
            return "메시지를 불러올 수 없습니다."

    except:
        return "에러가 발생하였습니다. 다시 시도해 주세요."



def show_chatbot_page():

    # 웹 정보 설정 및 UI
    st.set_page_config(page_title="내 손 안의 반려견 지킴이", page_icon="🐾")


    # 세션 상태 변수 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = "start"

    # 메시지 출력 함수
    def show_message(role, content, image=None):
        with st.chat_message(role):
            st.markdown(content)
            if image is not None:
                st.image(image, width=200)

    # 사용자 입력 처리 (사용자 메시지 입력 -> 답장 반환)
    def prossece_message(user_input: str) -> str:
        st.session_state.messages.append({"role": "user", "content": prompt})
        _message = get_message(user_input)
        st.session_state.messages.append({"role": "assistant", "content": _message})

    # 사용자 입력폼
    if prompt := st.chat_input("여기에 메시지를 입력하세요."):
        show_message("user", prompt)
        prossece_message(prompt.lower())
        
        st.rerun()

    # 대화 기록 출력
    for message in st.session_state.messages:
        print(message)
        show_message(message["role"], message["content"], message.get("image"))


if __name__ == "__main__":
    show_chatbot_page()