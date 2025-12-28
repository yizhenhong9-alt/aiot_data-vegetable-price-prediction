import pandas as pd
from pathlib import Path
import re

# ===============================
# 設定
# ===============================
# 指向你存放多個氣象站 .csv 的資料夾
INPUT_DIR = Path("dataset/raw_data/split_weather/Kai-lan")
OUTPUT_DIR = Path("dataset/processed_data/preprocessing/weather/Kai-lan")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COLUMNS_TO_KEEP = [
    "氣溫(℃)", "最高氣溫(℃)", "最低氣溫(℃)",
    "降水量(mm)", "降水時數(hour)", "日照時數(hour)",
    "相對溼度(%)", "最大陣風(m/s)"
]

NON_NEGATIVE_COLS = ["降水量(mm)", "降水時數(hour)", "日照時數(hour)", "相對溼度(%)", "最大陣風(m/s)"]
TEMP_COLS = ["氣溫(℃)", "最高氣溫(℃)", "最低氣溫(℃)"]
TEMP_MIN = -5

# ===============================
# 工具函式
# ===============================
def find_time_column(columns):
    for col in columns:
        if any(keyword in col for keyword in ["觀測時間", "日期", "Date", "Time"]):
            return col
    return None

# ===============================
# 主流程
# ===============================
def main():
    # 1. 取得資料夾內所有 CSV 檔案
    all_files = list(INPUT_DIR.glob("*.csv"))

    # 2. 建立年度群組 (Key: "2018-09-01_2019-01-31", Value: [file1, file2...])
    year_groups = {}
    # 使用正則表達式抓取檔名中的日期區間：XXXX-XX-XX_XXXX-XX-XX
    pattern = re.compile(r"(\d{4}-\d{2}-\d{2}_\d{4}-\d{2}-\d{2})")

    for f in all_files:
        match = pattern.search(f.name)
        if match:
            period = match.group(1)
            if period not in year_groups:
                year_groups[period] = []
            year_groups[period].append(f)

    if not year_groups:
        print("❌ 找不到符合日期區間檔名的檔案。")
        return

    # 3. 逐一年度群組處理
    for period, files in sorted(year_groups.items()):
        print(f"\n➡ 處理區間：{period} (共有 {len(files)} 個氣象站資料)")

        dfs = []
        start_year_str = period.split('-')[0] # 抓取開頭年份 (西元)
        start_year = int(start_year_str)

        for csv_path in files:
            df = pd.read_csv(csv_path, encoding="utf-8-sig")
            time_col = find_time_column(df.columns)

            if not time_col:
                print(f"  ⚠️ {csv_path.name} 找不到時間欄位，跳過")
                continue

            # 日期標準化
            df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

            # 數值清洗與轉型
            for col in COLUMNS_TO_KEEP:
                if col not in df.columns:
                    df[col] = pd.NA
                df[col] = pd.to_numeric(df[col], errors="coerce")

                # 負值/異常值處理
                if col in NON_NEGATIVE_COLS:
                    df.loc[df[col] < 0, col] = pd.NA
                if col in TEMP_COLS:
                    df.loc[df[col] < TEMP_MIN, col] = pd.NA

            # 只取需要的欄位
            df = df[[time_col] + COLUMNS_TO_KEEP]
            dfs.append(df)

        if not dfs:
            continue

        # 4. 合併所有站點並計算每日平均
        merged_df = pd.concat(dfs, ignore_index=True)
        merged_df["日期"] = merged_df[time_col].dt.date

        # Groupby 平均 (會自動忽略 NaN，即某站某日缺值不影響其他站)
        daily_avg = merged_df.groupby("日期").mean(numeric_only=True).reset_index()

        # 5. 格式化日期為民國年 (0XXX/MM/DD) 並存檔
        # 民國年計算
        def to_tw_date(d):
            return f"{d.year-1911:03d}/{d.month:02d}/{d.day:02d}"

        tw_period_name = f"{start_year-1911:03d}0901-{start_year+1-1911:03d}0131"
        daily_avg["日期"] = daily_avg["日期"].apply(to_tw_date)

        output_file = OUTPUT_DIR / f"雲林芥藍_avg_{tw_period_name}.csv"
        daily_avg.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"  ✅ 完成！輸出檔名：{output_file.name}")

if __name__ == "__main__":
    main()