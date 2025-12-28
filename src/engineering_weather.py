import pandas as pd
from pathlib import Path
import numpy as np

# ===============================
# 設定路徑
# ===============================
INPUT_DIR = Path("dataset/processed_data/preprocessing/weather/Kai-lan")
OUTPUT_DIR = Path("dataset/processed_data/feature_engineering/weather/Kai-lan")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# 欄位設定
# ===============================
NUMERIC_COLS = [
    "氣溫(℃)", "最高氣溫(℃)", "最低氣溫(℃)",
    "日照時數(hour)", "降水量(mm)", "降水時數(hour)",
    "相對溼度(%)", "最大陣風(m/s)"
]

LAG_DAYS = [1]
ROLL_DAYS = [3, 7, 15, 30]

# 極端事件閾值
EXTREME_TEMP_THRESH = 10   # 寒流
STRONG_COLD_THRESH = 7     # 強寒流
FROST_THRESH = 5           # 結霜
STRONG_WIND_THRESH = 15    # 強風
HEAVY_RAIN_THRESH = 50     # 強降雨

# ===============================
# 民國 ↔ 西元
# ===============================
def roc_to_ad(d):
    if isinstance(d, str):
        parts = d.split("/")
        if len(parts) == 3:
            y, m, day = int(parts[0])+1911, int(parts[1]), int(parts[2])
            return pd.Timestamp(f"{y}-{m:02d}-{day:02d}")
    return pd.NaT

def ad_to_roc(d):
    return f"{d.year-1911:03d}/{d.month:02d}/{d.day:02d}"

# ===============================
# 處理 CSV
# ===============================
weather_files = sorted(INPUT_DIR.glob("雲林芥藍_avg_*.csv"))

for wf in weather_files:
    print(f"🔄 處理檔案: {wf.name}")
    df = pd.read_csv(wf, encoding="utf-8-sig")
    if "日期" not in df.columns:
        raise KeyError(f"{wf.name} 找不到日期欄位")

    df["日期_dt"] = df["日期"].apply(roc_to_ad)
    df = df.sort_values("日期_dt").reset_index(drop=True)

    # 確保數值欄位存在
    for col in NUMERIC_COLS:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df[["日期_dt"] + NUMERIC_COLS]

    feat_list = []

    # ===============================
    # 前 1/2/3 天氣象特徵
    # ===============================
    for lag in LAG_DAYS:
        lag_df = df[NUMERIC_COLS].shift(lag)
        lag_df.columns = [f"{col}_lag{lag}d" for col in NUMERIC_COLS]
        feat_list.append(lag_df)

    # ===============================
    # 滾動平均 / 最大 / 最小特徵
    # ===============================
    ROLLMEAN_COLS = ["氣溫(℃)", "最高氣溫(℃)", "最低氣溫(℃)",
                     "日照時數(hour)", "相對溼度(%)", "最大陣風(m/s)"]
    ROLLSUM_COLS = ["降水量(mm)", "降水時數(hour)"]

    for col in ROLLMEAN_COLS:
        for r in ROLL_DAYS:
            roll = df[col].shift(1).rolling(r)
            feat_list.append(pd.DataFrame({
                f"{col}_rollmean_{r}d_prev": roll.mean(),
                f"{col}_rollmax_{r}d_prev": roll.max(),
                f"{col}_rollmin_{r}d_prev": roll.min()
            }))

    for col in ROLLSUM_COLS:
        for r in ROLL_DAYS:
            roll = df[col].shift(1).rolling(r)
            feat_list.append(pd.DataFrame({
                f"{col}_rollsum_{r}d_prev": roll.sum()
            }))

    # ===============================
    # 極端事件 / 二元特徵
    # ===============================
    feat_list.append(pd.DataFrame({
        "daily_temp_range_prev": (df["最高氣溫(℃)"] - df["最低氣溫(℃)"]).shift(1),
        "is_cold_wave_prev": (df["最低氣溫(℃)"].shift(1) <= EXTREME_TEMP_THRESH).astype(int),
        "is_strong_cold_prev": (df["最低氣溫(℃)"].shift(1) <= STRONG_COLD_THRESH).astype(int),
        "is_frost_risk_prev": ((df["最低氣溫(℃)"].shift(1) <= FROST_THRESH) &
                               (df["日照時數(hour)"].shift(1) < 1)).astype(int),
        "is_strong_wind_prev": (df["最大陣風(m/s)"].shift(1) >= STRONG_WIND_THRESH).astype(int),
        "is_heavy_rain_prev": (df["降水量(mm)"].shift(1) >= HEAVY_RAIN_THRESH).astype(int),
        "rainy_day_prev": (df["降水量(mm)"].shift(1) > 0).astype(int)
    }))

    # 連續降雨天數
    rainy_day_prev = (df["降水量(mm)"].shift(1) > 0).astype(int)
    consec_rainy = rainy_day_prev.groupby((rainy_day_prev != rainy_day_prev.shift()).cumsum()).cumsum().fillna(0)
    feat_list.append(pd.DataFrame({"consec_rainy_days_prev": consec_rainy}))

    # ===============================
    # 月份 / 週期 / 季節
    # ===============================
    month = df["日期_dt"].dt.month
    feat_list.append(pd.DataFrame({
        "month": month,
        "month_sin": np.sin(2 * np.pi * month / 12),
        "month_cos": np.cos(2 * np.pi * month / 12),
        "is_winter": month.isin([11,12,1,2]).astype(int)
    }))

    # ===============================
    # 合併所有欄位
    # ===============================
    feat_df = pd.concat([df["日期_dt"]] + feat_list, axis=1)
    feat_df["日期"] = feat_df["日期_dt"].apply(ad_to_roc)
    feat_df = feat_df.drop(columns=["日期_dt"])

    # 將日期放最前面
    cols = feat_df.columns.tolist()
    cols.remove("日期")
    feat_df = feat_df[["日期"] + cols]

    # ===============================
    # 輸出 CSV
    # ===============================
    output_file = OUTPUT_DIR / f"weather_feat_{wf.stem}.csv"
    feat_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"✅ 輸出完成: {output_file.name}")
