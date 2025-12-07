#====================================================
# Author: 601 Solutions
# Title: dog_info.py
# 강아지 정보 조회 화면
#====================================================

import streamlit as st

import sqlite3

DB_PATH = "pet_healthcare.db"

def get_connection():
    """데이터베이스와 루프를 연결"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def create_tables():
    """DB 생성"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
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
    c.execute('''
        CREATE TABLE IF NOT EXISTS change_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dog_id INTEGER NOT NULL,
            field_name TEXT NOT NULL,
            old_value TEXT,
            new_value TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(dog_id) REFERENCES dogs(id)
        )
    ''')
    conn.commit()
    conn.close()


def validate_dog_info(name, breed, age, weight):
    errors = []
    if not name or any(char in "!@#$%^&*()" for char in name):
        errors.append("강아지 이름을 올바르게 입력하세요(특수문자 제외).")

    if not breed:
        errors.append("품종을 입력하세요.")

    try:
        age_int = int(age)
        if age_int <= 0:
            errors.append("나이가 범위를 벗어났습니다.")
        elif age_int > 20:
            errors.append("나이가 범위를 벗어났습니다.")
    except (ValueError, TypeError):
        errors.append("나이는 숫자여야 합니다.")

    try:
        weight_float = float(weight)
        if weight_float <= 0:
            errors.append("잘못된 숫자입니다.")
    except (ValueError, TypeError):
        errors.append("체중은 숫자여야 합니다.")

    # 품종 리스트 검증
    valid_breeds = [
        "골든리트리버",
        "시바견",
        "치와와",
        "비글",
        "믹스견",
        "래브라도 리트리버",
        "저먼 셰퍼드",
        "불독",
        "포메라니안",
        "복서",
        "닥스훈트",
        "요크셔 테리어",
        "시추",
        "파피용",
        "말티즈",
        "달마시안",
        "퍼그",
        "보더 콜리",
        "미니어처 슈나우저",
        "그레이하운드"
    ]

    if breed not in valid_breeds:
        errors.append("유효하지 않은 품종입니다.")

    return errors



def save_dog_info(name, breed, age, weight, health, owner_id):
    """강아지 정보 저장"""
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO dogs(name, breed, age, weight, health, owner_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, breed, age, weight, health, owner_id))
    dog_id = c.lastrowid
    conn.commit()
    conn.close()
    return dog_id


def update_dog_info(dog_id, name, breed, age, weight, health):
    """강아지 정보 수정"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute("SELECT name, breed, age, weight, health FROM dogs WHERE id=?", (dog_id,))
    old_data = c.fetchone()
    
    if old_data:
        old_name, old_breed, old_age, old_weight, old_health = old_data
        if old_name != name:
            c.execute(
                "INSERT INTO change_history(dog_id, field_name, old_value, new_value) VALUES (?,?,?,?)",
                (dog_id, "Name", old_name, name)
            )
        if old_breed != breed:
            c.execute("INSERT INTO change_history(dog_id, field_name, old_value, new_value) VALUES (?,?,?,?)",
                     (dog_id, "Breed", old_breed, breed))
        if old_age != age:
            c.execute("INSERT INTO change_history(dog_id, field_name, old_value, new_value) VALUES (?,?,?,?)",
                     (dog_id, "Age", str(old_age), str(age)))
        if old_weight != weight:
            c.execute("INSERT INTO change_history(dog_id, field_name, old_value, new_value) VALUES (?,?,?,?)",
                     (dog_id, "Weight", str(old_weight), str(weight)))
        if old_health != health:
            c.execute("INSERT INTO change_history(dog_id, field_name, old_value, new_value) VALUES (?,?,?,?)",
                     (dog_id, "Status", old_health or "", health or ""))
    
    c.execute("UPDATE dogs SET name=?, breed=?, age=?, weight=?, health=? WHERE id=?",
             (name, breed, age, weight, health, dog_id))
    conn.commit()
    conn.close()


def get_user_id(username):
    """세션에서 유저 정보 획득"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def get_dog_info(owner_id):
    """유저 정보에서 반려견 정보 획득"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, breed, age, weight, health FROM dogs WHERE owner_id=? ORDER BY id DESC LIMIT 1", (owner_id,))
    result = c.fetchone()
    conn.close()
    return result


def get_change_history(dog_id):
    """강아지 정보 수정 이력 조회"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT field_name, old_value, new_value, changed_at 
        FROM change_history 
        WHERE dog_id=? 
        ORDER BY changed_at DESC
    """, (dog_id,))
    results = c.fetchall()
    conn.close()
    return results


# UI Section
def show_dog_info_page():
    st.set_page_config(page_title="내 손 안의 반려견 지킴이", page_icon="🐾")
    st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: #1e3a8a;
        margin: 0 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid #e3e8ef;
    }
    </style>
    """, unsafe_allow_html=True)

    if "username" not in st.session_state or not st.session_state.username:
        st.warning("로그인 후 이용해 주세요.")
        return

    user_id = get_user_id(st.session_state.username)
    if user_id is None:
        st.error("유저를 찾을 수 없습니다. 다시 로그인 해주세요.")
        return

    dog_info = get_dog_info(user_id)
    
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False if dog_info else True

    # === 편집 모드 ===
    if st.session_state.edit_mode:
        with st.container(border=True):  # border=True로 카드 효과

            default_name = dog_info[1] if dog_info else "My Dog"
            default_breed = dog_info[2] if dog_info else ""
            default_age = dog_info[3] if dog_info else 0
            default_weight = dog_info[4] if dog_info else 0.0
            default_health = dog_info[5] if dog_info else ""

            st.text_input("강아지 이름", value=default_name, key="input_name")
            st.text_input("견종", value=default_breed, key="input_breed")
            st.number_input("나이", min_value=0, value=int(default_age), key="input_age")
            st.number_input("체중", min_value=0.0, step=0.1, value=float(default_weight), key="input_weight")
            st.text_input("상태", value=default_health, key="input_status")

            col1, col2, col3 = st.columns([6, 1, 1])
            with col3:
                done = st.button("완료", type="primary", use_container_width=True)

            if done:
                name = st.session_state.input_name
                breed = st.session_state.input_breed
                age = st.session_state.input_age
                weight = st.session_state.input_weight
                status = st.session_state.input_status
                
                errors = validate_dog_info(name, breed, age, weight)
                if errors:
                    for err in errors:
                        st.error(err)
                else:
                    if dog_info:
                        update_dog_info(dog_info[0], name, breed, age, weight, status)
                        st.success("강아지 정보가 수정되었습니다.")
                    else:
                        save_dog_info(name, breed, age, weight, status, user_id)
                        st.success("강아지 정보가 저장되었습니다.")
                    st.session_state.edit_mode = False
                    st.rerun()

    # === 조회 모드 ===
    else:
        with st.container(border=True):
            st.markdown('<p class="card-title">✦ 우리 강아지</p>', unsafe_allow_html=True)
            
            if dog_info:
                st.markdown(f"**이름:** {dog_info[1]}")
                st.markdown(f"**견종:** {dog_info[2]}")
                st.markdown(f"**나이:** {dog_info[3]}")
                st.markdown(f"**체중:** {dog_info[4]:.1f}")
                st.markdown(f"**상태:** {dog_info[5] or '-'}")

            col1, col2, col3 = st.columns([6, 1, 1])
            with col3:
                if st.button("EDIT", type="secondary", use_container_width=True):
                    st.session_state.edit_mode = True
                    st.rerun()

    # === Change History ===
    with st.container(border=True):
        st.markdown('<p class="card-title">✦ 변경 이력</p>', unsafe_allow_html=True)
        
        if dog_info:
            history = get_change_history(dog_info[0])
            if history:
                history_data = []
                for h in history:
                    field_name = h[0]
                    old_value = h[1]
                    new_value = h[2]
                    
                    # Weight 필드만 소수점 1자리 포맷
                    if field_name == "Weight":
                        try:
                            old_value = f"{float(old_value):.1f}"
                        except:
                            pass
                        try:
                            new_value = f"{float(new_value):.1f}"
                        except:
                            pass
                    
                    history_data.append({
                        "항목": field_name, 
                        "이전값": old_value, 
                        "변경값": new_value, 
                        "변경일시": h[3][:19]
                    })
                
                st.dataframe(history_data, use_container_width=True, hide_index=True)
            else:
                st.info("변경 이력이 없습니다.")
        else:
            st.info("등록된 강아지 정보가 없습니다.")


# Main Section
create_tables() ## 오류 방지
