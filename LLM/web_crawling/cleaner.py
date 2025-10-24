import pandas as pd

# 처리할 원본 파일 이름
source_file = 'lifet_products.csv'
# 저장할 새 파일 이름
cleaned_file = 'lifet_products_cleaned.csv'

try:
    # 1. CSV 파일을 읽어옵니다.
    df = pd.read_csv(source_file)
    print("성공적으로 파일을 읽었습니다. 원본 데이터 샘플:")
    print(df.head())

    # 2. 상품명과 가격에 해당하는 열(column) 이름을 찾습니다.
    #    (실제 파일의 열 이름이 다를 수 있으므로 확인 후 수정해주세요.)
    product_col = 'NAME' # 상품명 열 이름 (예: 'name', '상품명' 등)
    price_col = 'PRICE'  # 가격 열 이름 (예: 'price', '금액', '가격' 등)

    if product_col in df.columns and price_col in df.columns:
        # 3. '[묶음 할인]'과 같은 불필요한 텍스트를 상품명에서 제거합니다.
        df[product_col] = df[product_col].str.replace('[묶음 할인]', '', regex=False).str.strip()

        # 4. 가격에서 쉼표(,)와 '원'을 제거하고, 숫자로 변환합니다.
        #    먼저 문자열로 변환하여 .str을 안전하게 사용합니다.
        df[price_col] = df[price_col].astype(str).str.replace(',', '').str.replace('원', '').astype(float)

        # 5. 필요한 열만 선택하여 새로운 데이터 프레임을 만듭니다.
        cleaned_df = df[[product_col, price_col]]

        # 6. 정제된 데이터를 새로운 CSV 파일로 저장합니다.
        cleaned_df.to_csv(cleaned_file, index=False, encoding='utf-8-sig')

        print(f"\n데이터 정제가 완료되었습니다. '{cleaned_file}' 파일로 저장되었습니다.")
        print("정제된 데이터 샘플:")
        print(cleaned_df.head())

    else:
        print(f"\n오류: '{product_col}' 또는 '{price_col}' 열을 찾을 수 없습니다.")
        print("실제 파일의 열 이름을 확인하고 코드를 수정해주세요.")
        print("현재 파일의 열 목록:", df.columns.tolist())

except FileNotFoundError:
    print(f"오류: '{source_file}' 파일을 찾을 수 없습니다. 파일 이름을 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")