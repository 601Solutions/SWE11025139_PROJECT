import streamlit as st

# 시작 조건: 로그인 후 진입 (예시, 실제 구현에서는 세션/DB 연동 필요)
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

def login():
    st.session_state.is_logged_in = True

if not st.session_state.is_logged_in:
    st.title("로그인")
    st.text_input("아이디")
    st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        login()
    st.stop()

# 유스케이스 화면 진입
st.title("강아지 헬스케어 AI 시스템")
st.header("내 강아지 등록/수정")

# 기본 흐름: 정보 입력/수정 (폼)
dog_name = st.text_input("강아지 이름")
dog_breed = st.text_input("품종")
dog_age = st.number_input("나이(년)", min_value=0, step=1)
dog_weight = st.number_input("체중(kg)", min_value=0.0, step=0.1)
dog_health = st.text_area("건강 상태")

# 대안 흐름: 필수 정보 누락/부적합값 체크
def validate_form():
    errors = []
    if not dog_name: errors.append("강아지 이름을 입력하세요.")
    if not dog_breed: errors.append("품종을 입력하세요.")
    if dog_age <= 0: errors.append("나이는 0보다 커야 합니다.")
    if dog_weight <= 0: errors.append("체중은 0보다 커야 합니다.")
    if any(char in "!@#$%^&*()" for char in dog_name):
        errors.append("이름에 특수문자를 입력할 수 없습니다.")
    return errors

if st.button("저장"):
    errors = validate_form()
    if errors:
        # 대안 흐름: 누락/부적합 안내
        for e in errors:
            st.warning(e)
    else:
        # 기본 흐름: DB 저장 (여기선 메모리 저장 예시)
        st.session_state.dog_info = {
            "이름": dog_name,
            "품종": dog_breed,
            "나이": dog_age,
            "체중": dog_weight,
            "건강상태": dog_health
        }
        # 종료 조건: 정상 저장 및 확인 메시지
        st.success("강아지 정보가 정상적으로 저장되었습니다.")
        st.write(st.session_state.dog_info)
