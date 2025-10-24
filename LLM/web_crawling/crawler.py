import requests
import csv

print("API 기반 크롤링을 시작합니다...")

# --- 1. 요청을 위한 기본 정보 설정 ---
# Headers 탭에서 찾은 User-Agent 값을 사용합니다.
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}
api_url = "https://lifet.co.kr/Store/Category"
all_products = []  # 모든 상품 데이터를 저장할 리스트

# --- 2. 여러 페이지를 돌면서 데이터 수집 ---
# 1페이지부터 10페이지까지 가져온다고 가정 (필요시 숫자를 늘리세요)
for page_num in range(1, 11): 
    # URL 파라미터를 딕셔너리 형태로 만듭니다.
    params = {
        'petKind': 1,
        'filter': 1,
        'page': page_num,
        'take': 12
    }
    
    print(f"{page_num}페이지에서 데이터를 가져오는 중...")
    response = requests.get(api_url, headers=headers, params=params)

    # 요청이 성공했는지 확인
    if response.status_code == 200:
        data = response.json()
        
        # 더 이상 상품이 없으면 반복을 멈춥니다.
        if not data:
            print("더 이상 상품이 없어 크롤링을 중단합니다.")
            break
            
        all_products.extend(data) # 가져온 상품 목록을 전체 리스트에 추가
    else:
        print(f"{page_num}페이지 요청 실패: {response.status_code}")
        break

# --- 3. 수집된 데이터를 CSV 파일로 저장 ---
if all_products:
    print(f"총 {len(all_products)}개의 상품 데이터를 CSV 파일로 저장합니다...")
    
    with open('lifet_products.csv', 'w', newline='', encoding='utf-8-sig') as f:
        # JSON 데이터의 키(key)들을 헤더로 사용합니다.
        # 첫 번째 상품 데이터의 키를 가져와 헤더로 설정합니다.
        header = all_products[0].keys()
        writer = csv.DictWriter(f, fieldnames=header)
        
        writer.writeheader() # 헤더 쓰기
        writer.writerows(all_products) # 모든 상품 데이터 쓰기

    print("'lifet_products.csv' 파일 저장이 완료되었습니다.")
else:
    print("수집된 상품 데이터가 없습니다.")