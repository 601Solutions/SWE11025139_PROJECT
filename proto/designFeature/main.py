import streamlit as st
from dog_info import show_dog_info_page
from chatbot import show_chatbot_page
import sqlite3
from passlib.hash import bcrypt

DB_PATH = "pet_healthcare.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def user_exists(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username=?", (username,))
    res = c.fetchone() is not None
    conn.close()
    return res

def safe_hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password should not be empty")
    pw_bytes = password.encode("utf-8")[:72]  # utf-8 인코딩 후 72바이트 제한
    return bcrypt.hash(pw_bytes)

def safe_verify_password(password: str, hashed: str) -> bool:
    if not password:
        return False
    pw_bytes = password.encode("utf-8")[:72]
    return bcrypt.verify(pw_bytes, hashed)

def add_user(username: str, password: str):
    conn = get_connection()
    c = conn.cursor()
    hashed = safe_hash_password(password)
    c.execute("INSERT INTO users (username, hashed_password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()

def verify_user(username: str, password: str) -> bool:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return False
    return safe_verify_password(password, row[0])



def login_ui():
    st.header("로그인")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type='password')
    if st.button("로그인"):
        if verify_user(username, password):
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.success(f"{username}님, 로그인 성공!")
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")

def signup_ui():
    st.header("회원가입")
    username = st.text_input("아이디", key="su_id")
    password = st.text_input("비밀번호", type='password', key="su_pw")
    password_confirm = st.text_input("비밀번호 확인", type='password', key="su_pw2")
    if st.button("회원가입"):
        if len(username) < 3:
            st.error("아이디는 3자 이상이어야 합니다.")
            return
        if password != password_confirm:
            st.error("비밀번호가 일치하지 않습니다.")
            return
        if user_exists(username):
            st.error("이미 존재하는 아이디입니다.")
            return
        add_user(username, password)
        st.success("회원가입 완료! 로그인해주세요.")

def logout():
    st.session_state.is_logged_in = False
    st.session_state.username = ""

def main():
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.username = ""

    if st.session_state.is_logged_in:
        menu = st.sidebar.radio("메뉴 선택", ["강아지 건강정보", "챗봇 상담", "로그아웃"])
        if menu == "강아지 건강정보":
            show_dog_info_page()
        elif menu == "챗봇 상담":
            show_chatbot_page()
        elif menu == "로그아웃":
            logout()
            st.success("로그아웃 되었습니다.")
    else:
        menu = st.sidebar.radio("메뉴 선택", ["로그인", "회원가입"])
        if menu == "로그인":
            login_ui()
        else:
            signup_ui()

if __name__=="__main__":
    main()
