import pandas as pd
from pathlib import Path

# ===============================
# 設定
# ===============================
MARKET_DIR = Path("dataset/processed_data/preprocessing/market/Kai-lan")
OUTPUT_DIR = Path("dataset/processed_data/feature_engineering/market/Kai-lan")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

LAG_DAYS = [1, 7, 14]
MA_DAYS = [3, 7]

# y（只能保留，不能當特徵）
TARGET_COL = "價格(元/公斤)"

# 只能用「過去」的市場欄位
MARKET_STRUCT_COLS = [
    "上價", "中價", "下價", "價格區間", "交易量(公斤)"
]

# ===============================
# 民國 → 西元
# ===============================
def roc_to_ad(d):
    try:
        y, m, d = d.split("/")
        return pd.Timestamp(int(y) + 1911, int(m), int(d))
    except:
        return pd.NaT

def ad_to_roc(d):
    return f"{d.year-1911:03d}/{d.month:02d}/{d.day:02d}"

# ===============================
# 逐檔處理
# ===============================
market_files = sorted(MARKET_DIR.glob("daily_market_Kai-lan_*.csv"))

for file_path in market_files:
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    # 日期排序
    df["日期_dt"] = df["日期"].apply(roc_to_ad)
    df = df.sort_values("日期_dt").reset_index(drop=True)

    # -------------------------------
    # 對「市場結構欄位」做 lag / ma
    # -------------------------------
    for col in MARKET_STRUCT_COLS:
        if col not in df.columns:
            continue

        for lag in LAG_DAYS:
            df[f"{col}_lag{lag}"] = df[col].shift(lag)

        for window in MA_DAYS:
            df[f"{col}_ma{window}"] = df[col].shift(1).rolling(window).mean()

    # -------------------------------
    # 對目標價格做 lag（納入前幾天的價格特徵）
    # -------------------------------
    for lag in LAG_DAYS:
        df[f"{TARGET_COL}_lag{lag}"] = df[TARGET_COL].shift(lag)

    # -------------------------------
    # ❌ 移除「當天市場結果特徵」
    # ✅ 保留 y 與前幾天價格
    # -------------------------------
    df = df.drop(columns=[c for c in MARKET_STRUCT_COLS if c in df.columns])

    # -------------------------------
    # 日期轉回民國（供 merge）
    # -------------------------------
    df["日期"] = df["日期_dt"].apply(ad_to_roc)
    df = df.drop(columns=["日期_dt"])

    output_file = OUTPUT_DIR / f"features_{file_path.name}"
    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ 完成市場特徵工程: {output_file.name}")
