import pytest
import os
import tempfile
import UI.dog_info as dog_info

# 테스트용 임시 DB 경로 설정 및 초기화
@pytest.fixture(scope="module")
def setup_test_db():
    fd, tmpfile = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    old_path = dog_info.DB_PATH
    dog_info.DB_PATH = tmpfile
    dog_info.create_tables()
    yield
    dog_info.DB_PATH = old_path
    os.remove(tmpfile)

# 정상 등록 테스트 (R1-1)
@pytest.mark.usefixtures("setup_test_db")
def test_save_dog_info_success():
    dogid = dog_info.save_dog_info("코코", "골든리트리버", 3, 25.5, "양호", 1)
    print("Log:", dogid)
    assert dogid is not None
    dogdata = dog_info.get_dog_info(1)
    print("Log:", dogdata)
    assert dogdata is not None
    assert dogdata[2] == "골든리트리버"  # breed 필드 위치 확인 필요
    assert dogdata[3] == 3
    assert abs(dogdata[4] - 25.5) < 0.001
    assert dogdata[5] == "양호"

# 필수 항목 누락 에러 테스트 (R1-2)
def test_validate_missing_breed():
    errors = dog_info.validate_dog_info("코코", "", 3, 25.5)
    print("Log:", errors)
    assert any("품종" in e for e in errors)

# 나이 데이터 타입 에러 (R1-3)
def test_validate_age_type_error():
    errors = dog_info.validate_dog_info("코코", "시바", "세 살", 10.0)  # 나이 문자형 입력 (비정상)
    print("Log:", errors)
    assert any("숫자" in e for e in errors)

# 체중 소수점 처리 (R1-4)
@pytest.mark.usefixtures("setup_test_db")
def test_weight_decimal():
    errors = dog_info.validate_dog_info("코코", "치와와", 2, 2.55)
    print("Log:", errors)
    assert errors == []
    dogid = dog_info.save_dog_info("코코", "치와와", 2, 2.55, "보통", 1)
    dogdata = dog_info.get_dog_info(1)
    print("Log:", dogdata)
    assert abs(dogdata[4] - 2.55) < 0.001

# 체중 음수 입력 에러 (R1-5)
def test_validate_negative_weight():
    errors = dog_info.validate_dog_info("코코", "비글", 5, -5.0)
    print("Log:", errors)
    assert any("잘못된" in e for e in errors)

# 긴 텍스트 건강 상태 저장 (R1-6)
@pytest.mark.usefixtures("setup_test_db")
def test_long_health_text():
    long_text = "건강 상태 매우 좋음 " * 50  # 500자 이상 텍스트
    dogid = dog_info.save_dog_info("코코", "믹스", 4, 12.0, long_text, 1)
    dogdata = dog_info.get_dog_info(1)
    print("Log:", dogdata)
    assert dogdata[5] == long_text

# 범위 외 데이터 및 비정상 단위 입력 테스트 (R1-7)
def test_validate_out_of_range_and_format():
    # 품종이 허용되지 않은 값인 경우
    errors = dog_info.validate_dog_info("쿠쿠", "전혁건", 3, 25.5)
    print("Log:", errors)
    assert any("품종" in e or "유효하지 않음" in e for e in errors)

    # 나이 범위 초과 (24 > 20)
    errors = dog_info.validate_dog_info("코코", "믹스견", 24, 20.0)
    print("Log:", errors)
    assert any("범위" in e or "유효하지 않음" in e for e in errors)

    # 체중 단위 이상 입력("70.0mg" -> 비정상 문자열 형태)
    errors = dog_info.validate_dog_info("코코", "믹스견", 4, "70.0mg")
    print("Log:", errors)
    assert any("숫자" in e or "잘못된" in e for e in errors)

if __name__ == "__main__":
    pytest.main()
