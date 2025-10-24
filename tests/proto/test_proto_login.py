from streamlit.testing.v1 import AppTest


def test_valid_input_and_save():
    at = AppTest.from_file("proto\\login.py").run()

    # 로그인 입력 및 클릭
    at.text_input[0].input("testuser").run()
    at.text_input[1].input("testpass").run()
    at.button[0].click().run()

    # 로그인 상태 반영 위해 앱 재실행
    at.run(timeout=10)

    # 로그인 후 강아지 정보 입력
    at.text_input[0].input("마루").run()             # 강아지 이름
    at.text_input[1].input("말티즈").run()           # 품종
    at.number_input[0].set_value(3).run()            # 나이
    at.number_input[1].set_value(10.5).run()         # 체중
    at.text_area[0].input("건강함").run()            # 건강 상태

    at.button[0].click().run()

    assert "강아지 정보가 정상적으로 저장되었습니다." in [m.value for m in at.success]


def test_invalid_input_shows_warning():
    at = AppTest.from_file("proto\\login.py").run()

    # 로그인
    at.text_input[0].input("testuser").run()
    at.text_input[1].input("testpass").run()
    at.button[0].click().run()

    # 로그인 상태 반영 위해 앱 재실행
    at.run(timeout=10)

    # 부적합 강아지 이름 입력 (특수문자 포함)
    at.text_input[0].input("펫!").run()
    at.text_input[1].input("포메라니안").run()
    at.number_input[0].set_value(2).run()
    at.number_input[1].set_value(5).run()
    at.text_area[0].input("건강").run()

    at.button[0].click().run()

    warnings = [w.value for w in at.warning]
    assert any("특수문자" in w for w in warnings)
