import sqlite3
import streamlit as st
from streamlit_option_menu import option_menu
from dog_info import show_dog_info_page
from chatbot import show_chatbot_page

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

def add_user(username: str, password: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def verify_user(username: str, password: str) -> bool:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row is None:
        return False
    return password == row[0]

def login_ui():
    # 로그인 화면 전용 CSS
    st.markdown("""
    <style>
    /* 전체 페이지 레이아웃 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 사이드바 숨기기 */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 로그인 컨테이너 */
    .login-container {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 80vh;
        padding: 40px 20px;
    }
    
    /* 로고/이미지 영역 */
    .login-logo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .login-logo-text {
        color: white;
        font-size: 32px;
        font-weight: bold;
        margin: 0;
    }
    
    /* 웰컴 텍스트 */
    .welcome-text {
        color: white;
        font-size: 48px;
        font-weight: bold;
        text-align: left;
        margin-bottom: 20px;
    }
    
    .welcome-subtext {
        color: rgba(0, 0, 0, 0.9);
        font-size: 18px;
        text-align: left;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 12px 16px;
        font-size: 16px;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* 텍스트 버튼 스타일 */
    div[data-testid="stButton"]:has(button[kind="secondary"]) button {
        background: transparent !important;
        border: none !important;
        color: #667eea !important;
        box-shadow: none !important;
        padding: 0 !important;
        font-size: 14px !important;
        font-weight: 400 !important;
    }
    div[data-testid="stButton"]:has(button[kind="secondary"]) button:hover {
        color: #764ba2 !important;
        text-decoration: underline !important;
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 2컬럼 레이아웃 (왼쪽: 웰컴, 오른쪽: 로그인 카드)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 60px 40px;">
            <h1 class="welcome-text">우리 강아지는 좋은 것만 </br>줘야하니까.</h1>
            <p class="welcome-subtext">AI 기반 반려견 건강 관리 서비스</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 로그인 카드
        with st.container():
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            
            
            # 입력 필드
            username = st.text_input("User Name", key="login_username", placeholder="아이디를 입력하세요")
            password = st.text_input("Password", type='password', key="login_password", placeholder="비밀번호를 입력하세요")
            
            # 로그인 버튼
            if st.button("Log In", type="primary", use_container_width=True):
                if verify_user(username, password):
                    st.session_state.is_logged_in = True
                    st.session_state.username = username
                    st.success(f"{username}님, 로그인 성공!")
                    st.rerun()
                else:
                    st.error("아이디 또는 비밀번호가 틀렸습니다.")
            
            # 회원가입 링크 버튼
            if st.button("계정이 없으신가요?", type="secondary", use_container_width=False, key="signup_link_btn"):
                st.session_state.auth_page = "signup"
                st.rerun()
        
            st.markdown('</div>', unsafe_allow_html=True)


def signup_ui():
    # 회원가입 화면
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    [data-testid="stSidebar"] {
        display: none;
    }
    .login-logo {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
    }
    .login-logo-text {
        color: white;
        font-size: 32px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # 이미지 파일이 있는지 확인하고 표시
    import os
    if os.path.exists("logo.png"):
        st.image("logo.png", width=340)
    else:
        st.markdown('<p style="font-size: 48px; margin: 0;">🐾</p>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    username = st.text_input("아이디", key="su_id", placeholder="3자 이상 입력하세요")
    password = st.text_input("비밀번호", type='password', key="su_pw", placeholder="비밀번호를 입력하세요")
    password_confirm = st.text_input("비밀번호 확인", type='password', key="su_pw2", placeholder="비밀번호를 다시 입력하세요")
    
    if st.button("회원가입", type="primary", use_container_width=True):
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    st.session_state.is_logged_in = False
    st.session_state.username = ""

def get_user_id(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_dog_name(owner_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM dogs WHERE owner_id=? ORDER BY id DESC LIMIT 1", (owner_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else "My Dog"

# ===== 여기가 사이드바 스타일 + 구조 =====
def draw_sidebar():
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: #fcfdfe !important;
        border-radius: 14px 0 0 14px;
        box-shadow: 2px 0 22px rgba(30,82,212,0.08);
        min-width: 263px;
        padding-top: 18px !important;
    }
    [data-testid="stSidebar"] h2 {
        color: #255de3; font-family: 'Montserrat', sans-serif; margin-bottom: 12px;
    }
    .option-menu .nav-link {
        border-radius: 7px !important;
        margin-bottom: 5px;
    }
    .option-menu .nav-link.active {
        background-color: #e2edfa !important;
        color: #2257a5 !important;
        font-weight: bold;
    }
    hr {border: 0.5px solid #dde2e7; margin: 14px 0;}
                
    .dog-name-text {
        font-size: 32px;
        font-weight: 600;
        color: #1e3a8a;
        margin: 0;
        padding: 12px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # 강아지 이름 표시
        user_id = get_user_id(st.session_state.username)
        dog_name = get_dog_name(user_id) if user_id else "My Dog"
        
        st.markdown(f"""
        <div class="dog-name-box">
            <p class="dog-name-text">🐾 {dog_name} 견주님 반가워요!</p>
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
                "container": {"padding": "0!important", "background-color": "#fcfdfe"},
                "icon": {"color": "#255de3", "font-size": "22px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
                "nav-link-selected": {"background-color": "#e2edfa", "font-weight": "bold", "color": "#173e95"}
            }
        )
        return selected

def main():
    st.set_page_config(page_title="내 손 안의 반려견 지킴이", page_icon="🐾")
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
        st.session_state.username = ""
    
    # 로그인 전: 사이드바 없이 중앙 로그인 화면
    if not st.session_state.is_logged_in:
        # 탭 대신 페이지 전환 버튼
        if "auth_page" not in st.session_state:
            st.session_state.auth_page = "login"
        
        if st.session_state.auth_page == "login":
            login_ui()
        else:
            signup_ui()
            if st.button("로그인 하러가기", type="secondary"):
                st.session_state.auth_page = "login"
                st.rerun()
        return
    
    # 로그인 후: 기존 사이드바 + 메인 콘텐츠
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
