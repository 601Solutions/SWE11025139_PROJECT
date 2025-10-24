import streamlit as st
import sqlite3
from passlib.hash import bcrypt

DB_PATH = "pet_healthcare.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight REAL NOT NULL,
            health TEXT,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY(owner_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# 사용자 유효성 검사
def validate_dog_info(name, breed, age, weight):
    errors = []
    if not name or any(char in "!@#$%^&*()" for char in name):
        errors.append("강아지 이름을 올바르게 입력하세요(특수문자 제외).")
    if not breed:
        errors.append("품종을 입력하세요.")
    if age <= 0:
        errors.append("나이는 0보다 커야 합니다.")
    if weight <= 0:
        errors.append("체중은 0보다 커야 합니다.")
    return errors

# 강아지 정보 저장 함수
def save_dog_info(name, breed, age, weight, health, owner_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO dogs(name, breed, age, weight, health, owner_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, breed, age, weight, health, owner_id))
    conn.commit()
    conn.close()

# 유저 아이디 조회 함수
def get_user_id(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def show_dog_info_page():
    st.title("강아지 정보 등록")
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("로그인 후 이용해 주세요.")
        return

    name = st.text_input("강아지 이름")
    breed = st.text_input("품종")
    age = st.number_input("나이(년)", min_value=0)
    weight = st.number_input("체중(kg)", min_value=0.0, step=0.1)
    health = st.text_area("기타 건강 상태")

    if st.button("저장"):
        errors = validate_dog_info(name, breed, age, weight)
        if errors:
            for err in errors:
                st.error(err)
            return

        user_id = get_user_id(st.session_state.username)
        if user_id is None:
            st.error("유저를 찾을 수 없습니다. 다시 로그인 해주세요.")
            return

        save_dog_info(name, breed, age, weight, health, user_id)
        st.success("강아지 정보가 저장되었습니다.")

# 테이블 한번 생성 (앱 최초 실행 시)
create_tables()
