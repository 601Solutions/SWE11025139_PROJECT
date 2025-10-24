import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://medi.qia.go.kr"
SEARCH_URL = f"{BASE_URL}/searchMedicine"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def search_medicine(keyword):
    """
    의약품명으로 검색 후 결과 테이블에서 상세페이지 URL과 기본정보 리스트 반환
    """
    params = {
        "itemName": keyword
    }
    res = requests.get(SEARCH_URL, headers=HEADERS, params=params)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # 테이블 찾기 (첨부 HTML 기준)
    table = soup.find("table")
    results = []
    if table:
        headers = [th.text.strip() for th in table.find_all("th")]

        for tr in table.find_all("tr")[1:]:
          td_list = tr.find_all("td")
          if not td_list:
              continue

          row_data = {headers[i]: td_list[i].text.strip() for i in range(len(td_list))}

          # 제품명 컬럼에서 상세페이지 링크 추출
          product_td = td_list[1]  # 제품명 컬럼 위치 반드시 확인!
          a_tag = product_td.find("a")
          if a_tag and a_tag.get("href"):
              detail_url = BASE_URL + a_tag.get("href")
          else:
              detail_url = None
          row_data["detail_url"] = detail_url

          results.append(row_data)

    return results

def parse_detail_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    container = soup.find('div', class_='drug_info_mid')
    if not container:
        return {}

    # 전체 info_sec 요소를 분류해서 담기
    raw_materials = []
    additives = None
    efficacy = None
    warnings_and_side_effects = None

    info_sections = container.find_all('div', class_='info_sec')
    for section in info_sections:
        text = section.get_text(separator=' ', strip=True)
        # 키워드 포함 여부로 대략 구분 (필요시 더 정교하게 수정)
        if '원료약품' in text or '원료' in text:
            raw_materials.append(text)
        elif '첨가제' in text:
            additives = text
        elif '효능효과' in text:
            efficacy = text
        elif '주의사항' in text or '부작용' in text:
            warnings_and_side_effects = text

    return {
        "raw_materials": raw_materials,
        "additives": additives,
        "efficacy": efficacy,
        "warnings_and_side_effects": warnings_and_side_effects
    }



if __name__ == "__main__":
    keyword = "옵티실드"  # 검색할 의약품명

    # 검색 결과에서 제품 기본정보, 상세페이지 URL 수집
    results = search_medicine(keyword)
    print(f"총 {len(results)}건 검색 완료")

    for idx, item in enumerate(results):
        print(f"\n[{idx +1}] 제품명: {item.get('제품명')}")
        print(f"업체명: {item.get('업체명')}")
        print(f"성분: {item.get('주성분')}")
        print(f"상세페이지: {item.get('detail_url')}")

        # 상세페이지 정보 크롤링
        detail_data = parse_detail_page(item.get('detail_url'))

        if detail_data:
            print("\n원료약품 및 분량:")
            for d in detail_data.get("raw_materials", []):
                print(d)

            print("\n첨가제:")
            print(detail_data.get("additives", "없음"))

            print("\n효능효과:")
            print(detail_data.get("efficacy", "없음"))

            print("\n주의사항 및 부작용:")
            print(detail_data.get("warnings_and_side_effects", "없음"))

        time.sleep(1)  # 서버부하 방지

