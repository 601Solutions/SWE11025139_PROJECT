import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm

# --- 1단계: 정제된 상품 목록 파일 읽기 ---
try:
    df = pd.read_csv('lifet_products_cleaned.csv') 
    print(f"✅ 총 {len(df)}개 상품 중 10개만 테스트 크롤링을 시작합니다.")
except FileNotFoundError:
    print("❌ 'lifet_products_cleaned.csv' 파일을 먼저 생성해야 합니다.")
    exit()

final_product_data = []
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 5)

print("각 상품의 상세 페이지 정보 수집 중...")

# ✅ df.head(10)을 사용하여 원본 데이터에서 10개만 선택합니다.
df_sample = df.head(10)

# tqdm의 반복 대상을 df_sample로 변경합니다.
for index, product_base_info in tqdm(df_sample.iterrows(), total=df_sample.shape[0]):
    product_code = product_base_info['PRODUCT_CODE']
    detail_url = f'https://lifet.co.kr/Store/Product/Detail?productCode={product_code}'
    
    driver.get(detail_url)

    try:
        toggle_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '성분 상세')]")))
        toggle_button.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.ingre-info")))
    except Exception as e:
        pass

    detail_soup = BeautifulSoup(driver.page_source, 'html.parser')

    ingredient_details = []
    ingre_info_div = detail_soup.select_one('div.ingre-info') 
    if ingre_info_div:
        items = ingre_info_div.select('dl')
        for item in items:
            title = item.select_one('dt').text.strip()
            desc = item.select_one('dd').text.strip()
            ingredient_details.append(f"{title}: {desc}")

    combined_info = product_base_info.to_dict()
    combined_info['ingredient_details'] = " | ".join(ingredient_details)
    
    final_product_data.append(combined_info)

driver.quit()

# --- 최종 결과를 CSV 파일로 저장 ---
if final_product_data:
    final_df = pd.DataFrame(final_product_data)
    # 파일 이름에 _SAMPLE을 붙여 구분합니다.
    final_df.to_csv('lifet_products_with_FULL_details_SAMPLE.csv', index=False, encoding='utf-8-sig')
    print(f"\n✅ 10개 샘플 상품 정보를 'lifet_products_with_FULL_details_SAMPLE.csv'에 저장했습니다.")
else:
    print("❌ 최종 상품 정보를 수집하지 못했습니다.")