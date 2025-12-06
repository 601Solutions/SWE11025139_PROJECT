#====================================================
# Author: 601 Solutions
# Title: main_ui.py
# 웹 앱 메인화면 
#====================================================

import sqlite3

import streamlit as st

from streamlit_option_menu import option_menu
from dog_info import show_dog_info_page
from chatbot import show_chatbot_page

DB_PATH = "pet_healthcare.db"

def get_connection():
    """데이터베이스와 루프를 연결"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def user_exists(username):
    """기존에 동일 유저가 존재하는지 판단"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username=?", (username,))
    res = c.fetchone() is not None
    conn.close()
    return res


def add_user(username: str, password: str):
    """사용자를 DB에 새로 추가"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()


def verify_user(username: str, password: str) -> bool:
    """로그인 검증"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return False
    return password == row[0]


def logout():
    """세션종료"""
    st.session_state.is_logged_in = False
    st.session_state.username = ""


def get_user_id(username):
    """세션에서 유저 정보 획득"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def get_dog_name(owner_id):
    """유저 정보에서 반려견 정보 획득"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM dogs WHERE owner_id=? ORDER BY id DESC LIMIT 1", (owner_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "My Dog"


### UI Section
def login_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
    }
    
    .main {
        background: #f5f5f7;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 애니메이션 정의 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Welcome 텍스트 애니메이션 */
    .welcome-text {
        color: #1d1d1f;
        font-size: 56px;
        font-weight: 600;
        line-height: 1.08;
        letter-spacing: -0.01em;
        margin-bottom: 16px;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    
    .welcome-subtext {
        color: #6e6e73;
        font-size: 21px;
        font-weight: 400;
        line-height: 1.4;
        letter-spacing: 0.01em;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
        opacity: 0;
    }
    
    /* 컬럼 내부 요소 애니메이션 */
    div[data-testid="column"]:nth-child(2) {
        display: flex;
        justify-content: center;
        align-items: center;
        animation: fadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;
        opacity: 0;
    }
    
    /* 입력 필드 */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #d2d2d7;
        padding: 16px 15px;
        font-size: 17px;
        font-weight: 400;
        background: #ffffff;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0071e3;
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
        outline: none;
        transform: scale(1.01);
    }
    
    .stTextInput label {
        font-size: 14px;
        font-weight: 500;
        color: #1d1d1f;
        margin-bottom: 8px;
    }
    
    /* Primary 버튼 */
    .stButton > button[kind="primary"] {
        background: #0071e3;
        color: white;
        border-radius: 12px;
        padding: 16px;
        font-size: 17px;
        font-weight: 500;
        border: none;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #0077ed;
        box-shadow: 0 4px 16px rgba(0, 113, 227, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Secondary 버튼 */
    .stButton > button[kind="secondary"] {
        background: transparent;
        border: none;
        color: #0071e3;
        padding: 0;
        font-size: 15px;
        font-weight: 400;
        box-shadow: none;
        transition: all 0.2s ease;
    }
    
    .stButton > button[kind="secondary"]:hover {
        color: #0077ed;
        text-decoration: underline;
        background: transparent;
    }
    
    /* 카드 컨테이너 애니메이션 */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:has(div.stTextInput) {
        background: rgba(255, 255, 255, 0.72);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-radius: 18px;
        border: 0.5px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 1px 1px rgba(0, 0, 0, 0.04);
        padding: 48px 40px;
        margin: 20px auto;
        max-width: 400px;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:has(div.stTextInput):hover {
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.06);
        transform: translateY(-4px);
    }
    
    /* Footer 스타일 */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 16px 20px;
        background: rgba(245, 245, 247, 0.8);
        backdrop-filter: blur(10px);
        border-top: 0.5px solid rgba(0, 0, 0, 0.08);
        animation: fadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.8s forwards;
        opacity: 0;
        z-index: 1000;
    }
    
    .footer-content {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 24px;
        flex-wrap: wrap;
    }
    
    .footer-text {
        font-size: 12px;
        color: #86868b;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.02em;
    }
    
    .footer-divider {
        color: #d2d2d7;
        font-size: 12px;
    }
    
    .footer-link {
        color: #0071e3;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    .footer-link:hover {
        color: #0077ed;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style="padding: 80px 60px;">
            <h1 class="welcome-text">우리 강아지는<br/>좋은 것만<br/>줘야하니까.</h1>
            <p class="welcome-subtext">AI 기반 반려견 건강 관리 서비스</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            
            username = st.text_input("", key="login_username", placeholder="아이디를 입력하세요")
            password = st.text_input("", type='password', key="login_password", placeholder="비밀번호를 입력하세요")
            
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
            if st.button("Log In", type="primary", use_container_width=True):
                if verify_user(username, password):
                    st.session_state.is_logged_in = True
                    st.session_state.username = username
                    st.success(f"환영합니다, {username}님!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 일치하지 않습니다.")
            
            st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
            if st.button("계정이 없으신가요?", type="secondary", key="signup_link"):
                st.session_state.auth_page = "signup"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <p class="footer-text">Demo Version · v1.0.0</p>
            <span class="footer-divider">|</span>
            <p class="footer-text">Developed by <span style="font-weight: 500;">Team 601 Solutions</span></p>
            <span class="footer-divider">|</span>
            <p class="footer-text">© 2025 Pet Healthcare AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def signup_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
    }
    
    .main {
        background: #f5f5f7;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 애니메이션 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Welcome 텍스트 */
    .welcome-text {
        color: #1d1d1f;
        font-size: 56px;
        font-weight: 600;
        line-height: 1.08;
        letter-spacing: -0.01em;
        margin-bottom: 16px;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        opacity: 0;
    }
    
    .welcome-subtext {
        color: #6e6e73;
        font-size: 21px;
        font-weight: 400;
        line-height: 1.4;
        letter-spacing: 0.01em;
        animation: fadeInUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s forwards;
        opacity: 0;
    }
    
    div[data-testid="column"]:nth-child(2) {
        display: flex;
        justify-content: center;
        align-items: center;
        animation: fadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.4s forwards;
        opacity: 0;
    }
    
    /* 입력 필드 */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1px solid #d2d2d7;
        padding: 16px 18px;
        font-size: 17px;
        font-weight: 400;
        background: #ffffff;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0071e3;
        box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
        outline: none;
        transform: scale(1.01);
    }
    
    .stTextInput label {
        font-size: 14px;
        font-weight: 500;
        color: #1d1d1f;
        margin-bottom: 8px;
    }
    
    /* Primary 버튼 */
    .stButton > button[kind="primary"] {
        background: #0071e3;
        color: white;
        border-radius: 12px;
        padding: 16px;
        font-size: 17px;
        font-weight: 500;
        border: none;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        box-shadow: none;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #0077ed;
        box-shadow: 0 4px 16px rgba(0, 113, 227, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) scale(0.98);
    }
    
    /* Secondary 버튼 */
    .stButton > button[kind="secondary"] {
        background: transparent;
        border: none;
        color: #0071e3;
        padding: 0;
        font-size: 15px;
        font-weight: 400;
        box-shadow: none;
        transition: all 0.2s ease;
    }
    
    .stButton > button[kind="secondary"]:hover {
        color: #0077ed;
        text-decoration: underline;
        background: transparent;
    }
    
    /* 카드 컨테이너 */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:has(div.stTextInput) {
        background: rgba(255, 255, 255, 0.72);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-radius: 18px;
        border: 0.5px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 1px 1px rgba(0, 0, 0, 0.04);
        padding: 48px 40px;
        margin: 20px auto;
        max-width: 400px;
        transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:has(div.stTextInput):hover {
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12), 0 2px 4px rgba(0, 0, 0, 0.06);
        transform: translateY(-4px);
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 16px 20px;
        background: rgba(245, 245, 247, 0.8);
        backdrop-filter: blur(10px);
        border-top: 0.5px solid rgba(0, 0, 0, 0.08);
        animation: fadeIn 1s cubic-bezier(0.16, 1, 0.3, 1) 0.8s forwards;
        opacity: 0;
        z-index: 1000;
    }
    
    .footer-content {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 24px;
        flex-wrap: wrap;
    }
    
    .footer-text {
        font-size: 12px;
        color: #86868b;
        font-weight: 400;
        margin: 0;
        letter-spacing: 0.02em;
    }
    
    .footer-divider {
        color: #d2d2d7;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style="padding: 80px 60px;">
            <h1 class="welcome-text">함께 시작할<br/>준비가<br/>되셨나요?</h1>
            <p class="welcome-subtext">간단한 정보 입력으로 우리 강아지의 건강 관리를 시작하세요</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        with st.container():
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            
            username = st.text_input("아이디", key="su_id", placeholder="3자 이상 입력하세요")
            password = st.text_input("비밀번호", type='password', key="su_pw", placeholder="비밀번호를 입력하세요")
            password_confirm = st.text_input("비밀번호 확인", type='password', key="su_pw2", placeholder="비밀번호를 다시 입력하세요")
            
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            
            if st.button("가입하기", type="primary", use_container_width=True):
                if len(username) < 3:
                    st.error("아이디는 3자 이상이어야 합니다.")
                elif password != password_confirm:
                    st.error("비밀번호가 일치하지 않습니다.")
                elif user_exists(username):
                    st.error("이미 존재하는 아이디입니다.")
                else:
                    add_user(username, password)
                    st.success("가입이 완료되었습니다!")
                    st.session_state.auth_page = "login"
                    st.rerun()
            
            st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
            if st.button("이미 계정이 있으신가요?", type="secondary", key="login_link"):
                st.session_state.auth_page = "login"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <p class="footer-text">Demo Version · v1.0.0</p>
            <span class="footer-divider">|</span>
            <p class="footer-text">Developed by <span style="font-weight: 500;">Team 601 Solutions</span></p>
            <span class="footer-divider">|</span>
            <p class="footer-text">© 2025 Pet Healthcare AI</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def draw_sidebar():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: saturate(180%) blur(20px) !important;
        -webkit-backdrop-filter: saturate(180%) blur(20px) !important;
        border-right: 0.5px solid rgba(0, 0, 0, 0.08);
        box-shadow: none;
        min-width: 300px;
        padding-top: 24px !important;
    }
    
    .dog-name-text {
        font-size: 35px;
        font-weight: 600;
        color: #1d1d1f;
        margin: 0;
        padding: 20px 16px;
        letter-spacing: -0.01em;
    }
    
    hr {
        border: none;
        border-top: 0.5px solid rgba(0, 0, 0, 0.08);
        margin: 16px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        user_id = get_user_id(st.session_state.username)
        dog_name = get_dog_name(user_id) if user_id else "My Dog"
        
        st.markdown(f"""
        <div>
            <p class="dog-name-text">🐾 {dog_name} 견주님 안녕하세요!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        selected = option_menu(
            menu_title=None,
            options=["우리 강아지", "무엇이든 물어보세요", "로그아웃"],
            menu_icon="cast",
            default_index=0,
            key="main_menu",
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#0071e3", "font-size": "20px"},
                "nav-link": {
                    "font-size": "17px",
                    "font-weight": "400",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "14px 16px",
                    "border-radius": "10px",
                    "color": "#1d1d1f"
                },
                "nav-link-selected": {
                    "background-color": "rgba(0, 113, 227, 0.1)",
                    "font-weight": "500",
                    "color": "#0071e3"
                }
            }
        )
        return selected

### Main Loop Section
def main():
    st.set_page_config(page_title="내 손 안의 반려견 지킴이", page_icon="🐾", layout="wide")
    
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.username = ""
    
    if not st.session_state.is_logged_in:
        if "auth_page" not in st.session_state:
            st.session_state.auth_page = "login"
        
        if st.session_state.auth_page == "login":
            login_ui()
        else:
            signup_ui()
        return
    
    selected = draw_sidebar()
    
    if selected == "우리 강아지":
        show_dog_info_page()
    elif selected == "무엇이든 물어보세요":
        show_chatbot_page()
    elif selected == "로그아웃":
        logout()
        st.session_state.auth_page = "login"
        st.success("로그아웃 되었습니다.")
        st.rerun()

if __name__ == "__main__":
    main()
