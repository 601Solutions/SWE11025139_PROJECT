import pandas as pd
import json

chunksize = 150  # 한 번에 1만 행씩 처리
with open("util/animal_medicine.jsonl", "w", encoding="utf-8") as f:
    for chunk in pd.read_csv("util/animal_medicine.csv", chunksize=chunksize):
        for row in chunk.to_dict(orient="records"):
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
