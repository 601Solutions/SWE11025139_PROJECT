import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm # 진행 상황을 시각적으로 보여주는 라이브러리

# --- 1단계: 정제된 상품 목록(주소록) 읽기 ---
try:
    df = pd.read_csv('lifet_products_cleaned.csv') 
    print(f"✅ 총 {len(df)}개의 상품 중 20개만 상세 정보 수집을 시작합니다.")
except FileNotFoundError:
    print("❌ 오류: 'lifet_products_cleaned.csv' 파일을 먼저 생성해야 합니다.")
    exit()

# --- 2단계: 각 상품의 상세 페이지를 순회하며 세부 정보 수집 ---
final_product_data = []

# Selenium 드라이버를 반복문 밖에서 한 번만 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

print("각 상품의 상세 페이지 정보 수집 중...")

df_sample = df.head(20)
# tqdm을 사용해 진행 막대를 표시
for index, product_base_info in tqdm(df_sample.iterrows(), total=df_sample.shape[0]):
    product_code = product_base_info['PRODUCT_CODE']
    detail_url = f'https://lifet.co.kr/Store/Product/Detail?productCode={product_code}'
    
    driver.get(detail_url)
    time.sleep(2) # 상세 페이지가 로딩될 때까지 잠시 대기

    detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 상세 정보 추출 (핵심 기능, 기본 정보)
    # 1. 핵심 기능
    feature_titles = []
    title_wrap = detail_soup.select_one('div.title-wrap')
    if title_wrap:
        features = title_wrap.select('span')
        for feature in features:
            feature_titles.append(feature.text.strip())
    
    # 2. 기본 정보
    product_info = {}
    info_table = detail_soup.select_one('div.info-table')
    if info_table:
        rows = info_table.select('dl')
        for row in rows:
            dt = row.select_one('dt').text.strip()
            dd = row.select_one('dd').text.strip()
            product_info[dt] = dd
            
    # 1단계 정보와 2단계 정보 병합
    combined_info = product_base_info.to_dict() # 기본 정보를 딕셔너리로 변환
    combined_info['features'] = ", ".join(feature_titles) # 추출한 핵심 기능 추가
    combined_info.update(product_info) # 추출한 기본 정보(딕셔너리)를 합침
    
    final_product_data.append(combined_info)

driver.quit() # 모든 작업이 끝났으므로 브라우저 종료

# --- 3단계: 최종 결과를 CSV 파일로 저장 ---
if final_product_data:
    final_df = pd.DataFrame(final_product_data)
    final_df.to_csv('lifet_products_with_details.csv', index=False, encoding='utf-8-sig')
    print(f"\n✅ 모든 상세 정보가 포함된 {len(final_df)}개 상품 정보를 'lifet_products_with_details.csv'에 저장했습니다.")
else:
    print("❌ 최종 상품 정보를 수집하지 못했습니다.")