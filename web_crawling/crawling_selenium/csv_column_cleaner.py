import pandas as pd

# 입력 파일과 출력 파일 이름 정의
input_file = 'lifet_products_final.csv'
output_file = 'lifet_products_cleaned.csv'

# 남기고 싶은 컬럼 목록 정의
columns_to_keep = ['PRODUCT_CODE', 'NAME', 'PRICE', 'REVIEW_COUNT', 'RATING_AVG']

try:
    # 원본 CSV 파일을 읽어옵니다.
    df = pd.read_csv(input_file)
    print("✅ 원본 파일 로딩 성공!")

    # 필요한 컬럼만 선택하여 새로운 데이터프레임을 만듭니다.
    cleaned_df = df[columns_to_keep]
    
    # 정제된 데이터를 새로운 CSV 파일로 저장합니다.
    # index=False: 불필요한 인덱스 열이 저장되지 않도록 함
    # encoding='utf-8-sig': Excel에서 한글이 깨지지 않도록 함
    cleaned_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"✅ 데이터 정제 완료! '{output_file}' 파일로 저장되었습니다.")
    print("\n--- 정제된 데이터 미리보기 ---")
    print(cleaned_df.head())

except FileNotFoundError:
    print(f"❌ 오류: '{input_file}' 파일을 찾을 수 없습니다.")
except KeyError:
    print(f"❌ 오류: 요청한 컬럼 중 일부가 파일에 없습니다. 파일의 컬럼을 확인해주세요.")
    print(f"    - 파일에 있는 컬럼: {df.columns.tolist()}")
    print(f"    - 요청한 컬럼: {columns_to_keep}")
except Exception as e:
    print(f"알 수 없는 오류가 발생했습니다: {e}")