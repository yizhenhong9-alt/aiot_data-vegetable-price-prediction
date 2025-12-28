import pandas as pd
from pathlib import Path

weather_dir = Path("dataset/processed_data/feature_engineering/weather/Kai-lan")
market_dir = Path("dataset/processed_data/feature_engineering/market/Kai-lan")
output_dir = Path("dataset/processed_data/merge_market_and_weather_after_engineering/Kai-lan")
output_dir.mkdir(parents=True, exist_ok=True)

csv_name = "_Kai-lan_after_engineering"

weather_files = sorted(weather_dir.glob("weather_feat_*.csv"))
market_files = sorted(market_dir.glob("features_daily_market_*.csv"))

merged_list = []

# ===============================
# 民國 → 西元（只用於算星期）
# ===============================
def roc_to_ad(d):
    try:
        y, m, day = d.split("/")
        return pd.Timestamp(int(y) + 1911, int(m), int(day))
    except:
        return pd.NaT

for wf, mf in zip(weather_files, market_files):
    weather_df = pd.read_csv(wf, encoding="utf-8-sig")
    market_df = pd.read_csv(mf, encoding="utf-8-sig")

    merged_df = pd.merge(market_df, weather_df, on="日期", how="left")

    # ===============================
    # 新增「星期特徵」
    # ===============================
    merged_df["日期_dt"] = merged_df["日期"].apply(roc_to_ad)

    merged_df["weekday"] = merged_df["日期_dt"].dt.weekday  # 0=Mon
    merged_df["is_weekend"] = merged_df["weekday"].isin([5, 6]).astype(int)
    merged_df["is_mon"] = (merged_df["weekday"] == 0).astype(int)
    merged_df["is_fri"] = (merged_df["weekday"] == 4).astype(int)

    merged_df = merged_df.drop(columns=["日期_dt"])

    merged_list.append(merged_df)

# ===============================
# 切分資料
# ===============================
train_df = pd.concat(merged_list[:5], ignore_index=True)
valid_df = merged_list[-2]
test_df  = merged_list[-1]

train_df.to_csv(output_dir / f"train{csv_name}.csv", index=False, encoding="utf-8-sig")
valid_df.to_csv(output_dir / f"valid{csv_name}.csv", index=False, encoding="utf-8-sig")
test_df.to_csv(output_dir / f"test{csv_name}.csv", index=False, encoding="utf-8-sig")

print("✅ 合併完成（含星期特徵）")
print(f"Train features count: {len(train_df.columns) - 1}")
print(train_df.columns.tolist())
