import pandas as pd
from pathlib import Path

CSV_DIR = Path(r"../csv_data")
OUTPUT_FILE = "merged_unique.csv"

dfs = []
for csv_file in CSV_DIR.glob("*.csv"):
    df = pd.read_csv(csv_file)
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True)

# 根据 title 去重，只保留第一条出现的新闻
merged_unique_df = merged_df.drop_duplicates(subset=["title"], keep="first")

merged_unique_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(merged_unique_df.shape) # (38359, 4)


