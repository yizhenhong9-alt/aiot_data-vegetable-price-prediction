import pandas as pd
from pathlib import Path

# =========================
# 使用者設定
# =========================
INPUT_FILE = r"dataset/raw_data/market/Kai-lan/蔬菜產品日交易行情-芥藍.xls"
OUTPUT_DIR = Path("dataset/raw_data/split_market/Kai-lan")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 你需要的 7 個年度 (以產期開始年為準)
# 例如 107 產期 = 2018/11/01 ~ 2019/01/31
SEASON_YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

# =========================
# 核心處理函式
# =========================
def parse_tw_date(date_val):
    """處理怪異日期：將 '107/11/01' 或 1071101 轉為西元 Timestamp"""
    try:
        date_str = str(date_val).strip()
        if '/' in date_str:
            parts = date_str.split('/')
            y = int(parts[0]) + 1911
            m = int(parts[1])
            d = int(parts[2])
            return pd.Timestamp(y, m, d)
        elif len(date_str) >= 6: # 處理 1071101 這種格式
            y = int(date_str[:-4]) + 1911
            m = int(date_str[-4:-2])
            d = int(date_str[-2:])
            return pd.Timestamp(y, m, d)
    except:
        return pd.NaT
    return pd.NaT

def main():
    input_path = Path(INPUT_FILE)
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        print(f"❌ 找不到原始檔案：{INPUT_FILE}")
        return

    print(f"➡ 正在讀取並解析：{input_path.name}")

    # 1. 讀取 Excel (header=4 避開上方標題列)
    df = pd.read_excel(input_path, header=4, engine="xlrd")
    df.columns = [str(c).strip() for c in df.columns]

    # 2. 找到日期欄位（解決日期欄位名稱不固定的問題）
    try:
        date_col = next(c for c in df.columns if '日' in c and '期' in c)
    except StopIteration:
        print("❌ 找不到包含 '日期' 的欄位，請檢查 Excel header 層級")
        return

    # 3. 建立標準化西元時間欄位以便切割
    df['temp_date'] = df[date_col].apply(parse_tw_date)
    df = df.dropna(subset=['temp_date']).sort_values('temp_date')

    # 4. 開始切割 7 個年度
    for year in SEASON_YEARS:
        # 設定產期區間 (11/01 ~ 隔年 01/31)
        start_dt = pd.Timestamp(f"{year}-11-01")
        end_dt = pd.Timestamp(f"{year + 1}-01-31")

        # 篩選資料
        df_season = df[(df['temp_date'] >= start_dt) & (df['temp_date'] <= end_dt)].copy()

        if df_season.empty:
            print(f"⚠️ {year} 年產期 (民國 {year-1911}年) 無資料，跳過")
            continue

        # 5. 格式化輸出檔名 (民國年格式)
        tw_s = f"{year - 1911}1101"
        tw_e = f"{year + 1 - 1911}0131"
        file_name = f"market_Kai-lan_{tw_s}-{tw_e}.csv"

        # 移除暫存欄位並存檔
        output_file = output_path / file_name
        df_season.drop(columns=['temp_date']).to_csv(output_file, index=False, encoding="utf-8-sig")

        print(f"✅ 已成功切割：{file_name} (共 {len(df_season)} 筆)")

    print("\n🎉 7 個年度切割完成！")

if __name__ == "__main__":
    main()