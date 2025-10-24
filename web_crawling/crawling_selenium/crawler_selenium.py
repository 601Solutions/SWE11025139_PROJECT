import requests
import csv

print("API 기반 크롤링을 시작합니다...")

# --- 1. 요청을 위한 기본 정보 설정 (보강된 헤더) ---
# 실제 브라우저가 보내는 헤더 정보들을 최대한 포함합니다.
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://lifet.co.kr/Store/Category',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}
api_url = "https://lifet.co.kr/Store/Product/List" # ✅ API 엔드포인트를 정확히 지정
category_url = "https://lifet.co.kr/Store/Category"
all_products = []

# --- 2. Session 객체 생성 및 쿠키 획득 ---
# Session 객체를 만들면 쿠키가 자동으로 관리됩니다.
session = requests.Session()

# 데이터 요청 전에, 메인 페이지를 먼저 방문하여 세션 쿠키를 받습니다.
print("세션 쿠키를 얻기 위해 메인 페이지에 접속합니다...")
session.get(category_url, headers=headers)
print("쿠키 획득 완료.")

# --- 3. 여러 페이지를 돌면서 데이터 수집 ---
# 1페이지부터 60페이지까지 시도 (665개 상품 / 한 페이지당 12개 = 약 56페이지)
for page_num in range(1, 61): 
    params = {
        'petKind': 1,
        'filter': 1,
        'page': page_num,
        'take': 12
    }
    
    print(f"{page_num}페이지에서 데이터를 가져오는 중...")
    # session.get()을 사용하여 쿠키와 함께 요청을 보냅니다.
    response = session.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            if not data:
                print("더 이상 상품이 없어 크롤링을 중단합니다.")
                break
            all_products.extend(data)
        except requests.exceptions.JSONDecodeError:
            print(f"❌ {page_num}페이지에서 JSON 디코딩 오류가 발생했습니다.")
            print("서버 실제 응답 내용:", response.text)
            break
    else:
        print(f"{page_num}페이지 요청 실패: {response.status_code}")
        break

# --- 4. 수집된 데이터를 CSV 파일로 저장 ---
if all_products:
    print(f"총 {len(all_products)}개의 상품 데이터를 CSV 파일로 저장합니다...")
    
    with open('lifet_products_final.csv', 'w', newline='', encoding='utf-8-sig') as f:
        header = all_products[0].keys()
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(all_products)

    print("'lifet_products_final.csv' 파일 저장이 완료되었습니다.")
else:
    print("수집된 상품 데이터가 없습니다.")