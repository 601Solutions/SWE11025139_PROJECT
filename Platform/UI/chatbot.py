#====================================================
# Author: 601 Solutions
# Title: chatbot.py
# 챗봇 대화 화면 
#====================================================

import streamlit as st

import requests
import sqlite3


## HTTP API 호출 주소 및 포트
_URL = "http://127.0.0.1:8000" #localhost


def get_user_id(username):
    """사용자 ID 가져오기"""
    conn = sqlite3.connect("pet_healthcare.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def get_message(input_message: str, owner_id: int = None) -> dict:
    """
    API를 통해 메시지 전송 및 응답 받기
    
    Args:
        input_message: 사용자 질문
        owner_id: 사용자 ID (강아지 정보 조회용)
    
    Returns:
        dict: {'message': str, 'dog_name': str or None}
    """
    try:
        response = requests.post(
            _URL + "/conversation",
            json={
                "message": input_message,
                "owner_id": owner_id  # 강아지 정보를 위한 owner_id 전달
            },
            timeout=300  # 타임아웃 설정
        )
        
        # 통신 예외처리
        if response.status_code == 200:
            data = response.json()
            print(f"API 응답: {data}")  # Debug
            return {
                'message': data.get('message', '응답을 받지 못했습니다.'),
                'dog_name': data.get('dog_name'),
                'retrieved_docs': data.get('retrieved_docs', 0)
            }
        else:
            print(f"API 오류: {response.status_code}")
            return {
                'message': f"메시지를 불러올 수 없습니다. (오류 코드: {response.status_code})",
                'dog_name': None
            }
    
    except requests.exceptions.Timeout:
        print("API 타임아웃")
        return {
            'message': "응답 시간이 초과되었습니다. 다시 시도해 주세요.",
            'dog_name': None
        }
    except requests.exceptions.ConnectionError:
        print("API 연결 실패")
        return {
            'message': "서버에 연결할 수 없습니다. API 서버가 실행 중인지 확인해주세요.",
            'dog_name': None
        }
    except Exception as e:
        print(f"예외 발생: {e}")
        return {
            'message': f"에러가 발생하였습니다: {str(e)}",
            'dog_name': None
        }


# UI Section
def show_chatbot_page():
    """
    챗봇 페이지 UI
    """
    st.set_page_config(page_title="내 손 안의 반려견 지킴이", page_icon="🐾")
    
    # 사용자 ID 가져오기
    user_id = get_user_id(st.session_state.username)
    
    # 세션 상태 변수 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = "start"
    
    
    # 이전 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            # 강아지 정보 알림 표시
            if message["role"] == "assistant" and message.get("dog_name"):
                st.info(f"{message['dog_name']}의 정보를 바탕으로 답변드립니다.")
            
            st.markdown(message["content"])
            
            # 이미지가 있으면 표시
            if message.get("image"):
                st.image(message["image"], width=200)
    
    # 사용자 입력 처리
    if prompt := st.chat_input("강아지 건강에 대해 궁금한 것을 물어보세요"):
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("답변 생성 중..."):
                # owner_id를 전달하여 강아지 정보 포함
                response_data = get_message(prompt, owner_id=user_id)
                
                # 강아지 이름이 있으면 알림 표시
                if response_data.get('dog_name'):
                    st.info(f"{response_data['dog_name']}의 정보를 바탕으로 답변드립니다.")
                
                # 응답 메시지 표시
                st.markdown(response_data['message'])
                
                # 메시지 히스토리에 추가
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response_data['message'],
                    "dog_name": response_data.get('dog_name')
                })
    

#Main Section    
if __name__ == "__main__":
    # 테스트용
    if "username" not in st.session_state:
        st.session_state.username = "test_user"
    
    show_chatbot_page()
