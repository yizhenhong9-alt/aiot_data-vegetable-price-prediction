import pandas as pd
from pathlib import Path

# -------------------------------
# 設定輸入與輸出
# -------------------------------
INPUT_DIR = Path("dataset/raw_data/split_market/Kai-lan")
OUTPUT_DIR = Path("dataset/processed_data/preprocessing/market/Kai-lan")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------
# 主處理函式
# -------------------------------
def process_market_file(file_path):
    # 改為讀取 CSV (因為前一步已經處理過 utf-8-sig)
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    df.columns = [str(c).strip() for c in df.columns]

    try:
        # 1. 找必要欄位 (使用模糊匹配)
        date_col = next(c for c in df.columns if '日' in c and '期' in c)
        avg_col = next(c for c in df.columns if '平均價' in c)
        high_col = next((c for c in df.columns if '上價' in c), None)
        mid_col  = next((c for c in df.columns if '中價' in c), None)
        low_col  = next((c for c in df.columns if '下價' in c), None)
        vol_col  = next((c for c in df.columns if '交易量' in c), None)

        use_cols = [date_col, avg_col, high_col, mid_col, low_col, vol_col]
        use_cols = [c for c in use_cols if c is not None]

        df = df[use_cols].copy()

        # 2. 轉數值 (處理可能出現的 '-' 或 非數字字元)
        for c in use_cols:
            if c != date_col:
                df[c] = pd.to_numeric(df[c], errors="coerce")

        # 3. 清理無效資料
        df = df.dropna(subset=[date_col, avg_col])

        # 4. 每日平均 (避免同日有多個市場資料)
        daily = df.groupby(date_col).mean().reset_index()

        # 5. 統一欄位名稱
        rename_map = {
            date_col: "日期",
            avg_col: "價格(元/公斤)",
            high_col: "上價",
            mid_col: "中價",
            low_col: "下價",
            vol_col: "交易量(公斤)"
        }
        daily = daily.rename(columns=rename_map)

        # 6. 移除非日期列 (只保留包含斜線的日期格式)
        daily = daily[daily["日期"].astype(str).str.contains("/")].copy()

        # 7. 額外欄位計算：價格區間
        if "上價" in daily.columns and "下價" in daily.columns:
            daily["價格區間"] = daily["上價"] - daily["下價"]

        # 輸出檔案 (檔名前綴加上 preprocessed_)
        output_file = OUTPUT_DIR / f"daily_{file_path.name}"
        daily.to_csv(output_file, index=False, encoding="utf-8-sig")
        print(f"  ✅ 預處理完成：{output_file.name}")

    except Exception as e:
        print(f"  ❌ 處理 {file_path.name} 時出錯: {e}")

# -------------------------------
# 執行
# -------------------------------
def main():
    # 自動抓取資料夾下所有 .csv
    csv_files = list(INPUT_DIR.glob("market_Kai-lan_*.csv"))

    if not csv_files:
        print(f"⚠ 在 {INPUT_DIR} 找不到任何 CSV 檔案")
        return

    print(f"📂 找到 {len(csv_files)} 個檔案，開始進行預處理...")
    for fp in csv_files:
        print(f"➡ 處理：{fp.name}")
        process_market_file(fp)

    print("\n🎉 所有年度預處理完成！")

if __name__ == "__main__":
    main()