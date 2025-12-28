import pandas as pd
from pathlib import Path

# =========================
# 使用者設定
# =========================
# 設定輸入資料夾的路徑
INPUT_DIR = r"dataset\raw_data\weather\Kai-lan"
OUTPUT_DIR = r"dataset\raw_data\split_weather\Kai-lan"

START_SEASON_YEAR = 2018
END_SEASON_YEAR = 2024

# =========================
# 從檔名取氣象站編號
# =========================
def get_station_id_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    parts = stem.split("_")

    if len(parts) < 4 or parts[0] != "daily":
        # 如果格式不符，回傳檔名的一部分或報錯
        print(f"  ⚠️ 檔名格式非預期（{filename}），嘗試提取第二部分作為 ID")
        return parts[1] if len(parts) > 1 else "unknown"

    return parts[1]

# =========================
# 自動找時間欄位（處理 BOM）
# =========================
def find_time_column(columns):
    for col in columns:
        if "觀測時間" in col:
            return col
    raise KeyError("❌ 找不到包含「觀測時間」標籤的欄位")

# =========================
# 單一檔案處理邏輯
# =========================
def process_single_file(file_path: Path, output_root: Path):
    print(f"\n➡ 正在處理檔案：{file_path.name}")

    try:
        # 取得氣象站編號
        station_id = get_station_id_from_filename(file_path.name)

        # 讀取 CSV
        df = pd.read_csv(file_path, encoding="utf-8-sig")

        # 自動偵測時間欄位
        time_col = find_time_column(df.columns)
        df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

        if df[time_col].isna().any():
            print(f"  ❌ {file_path.name} 時間轉換有誤，跳過該檔")
            return

        df = df.sort_values(time_col)

        # 依產期切割
        for year in range(START_SEASON_YEAR, END_SEASON_YEAR + 1):
            start_date = pd.Timestamp(f"{year}-09-01")
            end_date = pd.Timestamp(f"{year + 1}-01-31")

            df_season = df[
                (df[time_col] >= start_date) &
                (df[time_col] <= end_date)
            ]

            if df_season.empty:
                continue

            output_name = f"daily_{station_id}_{start_date.date()}_{end_date.date()}.csv"

            # 若想區分不同測站到不同子資料夾，可改為 output_root / station_id
            save_path = output_root / output_name
            df_season.to_csv(save_path, index=False, encoding="utf-8-sig")
            print(f"  ✅ 已生成：{output_name}")

    except Exception as e:
        print(f"  💥 處理 {file_path.name} 時發生錯誤: {e}")

# =========================
# 主程式
# =========================
def main():
    input_dir = Path(INPUT_DIR)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_dir.exists():
        raise FileNotFoundError(f"❌ 找不到輸入資料夾：{INPUT_DIR}")

    # 取得資料夾下所有 .csv 檔案
    csv_files = list(input_dir.glob("*.csv"))

    if not csv_files:
        print("Empty! 找不到任何 CSV 檔案。")
        return

    print(f"📂 找到 {len(csv_files)} 個檔案，準備開始切割...")

    for file_path in csv_files:
        process_single_file(file_path, output_dir)

    print("\n🎉 所有檔案處理完成！")

if __name__ == "__main__":
    main()