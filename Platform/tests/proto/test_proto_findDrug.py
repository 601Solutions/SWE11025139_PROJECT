import pytest
import requests

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from proto.findDrug import search_medicine, parse_detail_page, BASE_URL, SEARCH_URL

# 테스트에 사용할 모의 HTML 데이터
@pytest.fixture
def mock_search_html():
    """search_medicine 함수 테스트를 위한 검색 결과 페이지의 모의 HTML을 반환합니다."""
    return """
    <html>
        <body>
            <table>
                <thead>
                    <tr>
                        <th>번호</th>
                        <th>제품명</th>
                        <th>업체명</th>
                        <th>주성분</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td><a href="/medicine/detail/12345">옵티실드정</a></td>
                        <td>(주)테스트제약</td>
                        <td>테스트성분A</td>
                    </tr>
                </tbody>
            </table>
        </body>
    </html>
    """

@pytest.fixture
def mock_detail_html():
    """parse_detail_page 함수 테스트를 위한 상세 정보 페이지의 모의 HTML을 반환합니다."""
    return """
    <html>
        <body>
            <div class="drug_info_mid">
                <div class="info_sec">
                    <h3>원료약품 및 분량</h3>
                    <p>1정 중 유효성분: 테스트성분A (100mg)</p>
                </div>
                <div class="info_sec">
                    <h3>첨가제</h3>
                    <p>첨가제: 테스트첨가제B</p>
                </div>
                <div class="info_sec">
                    <h3>효능효과</h3>
                    <p>눈의 피로, 시력 개선</p>
                </div>
                <div class="info_sec">
                    <h3>사용상의 주의사항</h3>
                    <p>다음 환자에게는 투여하지 말 것.</p>
                </div>
            </div>
        </body>
    </html>
    """

def test_search_medicine_success(requests_mock, mock_search_html):
    """의약품 검색 성공 케이스를 테스트합니다."""
    keyword = "옵티실드"
    # SEARCH_URL에 대한 GET 요청을 모의 HTML로 대체
    requests_mock.get(f"{SEARCH_URL}?itemName={keyword}", text=mock_search_html)

    results = search_medicine(keyword)

    # 결과 검증
    assert len(results) == 1
    assert results[0]['제품명'] == '옵티실드정'
    assert results[0]['업체명'] == '(주)테스트제약'
    assert results[0]['주성분'] == '테스트성분A'
    assert results[0]['detail_url'] == f"{BASE_URL}/medicine/detail/12345"

def test_search_medicine_no_results(requests_mock):
    """검색 결과가 없을 경우를 테스트합니다."""
    keyword = "없는약"
    # 검색 결과가 없는 경우의 HTML (tbody가 비어있음)
    empty_html = "<table><tbody></tbody></table>"
    requests_mock.get(f"{SEARCH_URL}?itemName={keyword}", text=empty_html)

    results = search_medicine(keyword)

    # 결과가 빈 리스트인지 검증
    assert len(results) == 0

def test_search_medicine_http_error(requests_mock):
    """서버 에러 발생 시 (HTTP 500) 예외 처리를 테스트합니다."""
    keyword = "에러테스트"
    requests_mock.get(f"{SEARCH_URL}?itemName={keyword}", status_code=500)

    # requests.HTTPError가 발생하는지 검증
    with pytest.raises(requests.exceptions.HTTPError):
        search_medicine(keyword)

def test_parse_detail_page_success(requests_mock, mock_detail_html):
    """상세 페이지 파싱 성공 케이스를 테스트합니다."""
    detail_url = f"{BASE_URL}/medicine/detail/12345"
    requests_mock.get(detail_url, text=mock_detail_html)

    data = parse_detail_page(detail_url)

    # 파싱된 데이터 검증
    assert '원료약품 및 분량 1정 중 유효성분: 테스트성분A (100mg)' in data['raw_materials']
    assert data['additives'] == '첨가제 첨가제: 테스트첨가제B'
    assert data['efficacy'] == '효능효과 눈의 피로, 시력 개선'
    assert data['warnings_and_side_effects'] == '사용상의 주의사항 다음 환자에게는 투여하지 말 것.'

def test_parse_detail_page_container_not_found(requests_mock):
    """상세 페이지에 주요 정보 컨테이너가 없을 경우를 테스트합니다."""
    detail_url = f"{BASE_URL}/medicine/detail/empty"
    # 'drug_info_mid' 클래스가 없는 HTML
    empty_html = "<html><body><div>내용 없음</div></body></html>"
    requests_mock.get(detail_url, text=empty_html)

    data = parse_detail_page(detail_url)

    # 빈 딕셔너리를 반환하는지 검증
    assert data == {}
