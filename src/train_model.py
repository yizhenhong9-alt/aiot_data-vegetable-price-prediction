import pandas as pd
import lightgbm as lgb
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# 1️⃣ 設定檔案路徑
# ===============================
DATA_DIR = Path("dataset/processed_data/merge_market_and_weather_after_engineering/Kai-lan")
TRAIN_FILE = DATA_DIR / "train_Kai-lan_after_engineering.csv"
VALID_FILE = DATA_DIR / "valid_Kai-lan_after_engineering.csv"
TEST_FILE = DATA_DIR / "test_Kai-lan_after_engineering.csv"
output_dir = Path("dataset/model/Kai-lan")
output_dir.mkdir(parents=True, exist_ok=True)

TARGET_COL = "價格(元/公斤)"

# ===============================
# 2️⃣ 讀取資料
# ===============================
train_df = pd.read_csv(TRAIN_FILE)
valid_df = pd.read_csv(VALID_FILE)
test_df = pd.read_csv(TEST_FILE)

# ===============================
# 3️⃣ 分特徵與目標
# ===============================
feature_cols = [c for c in train_df.columns if c != "日期" and c != TARGET_COL]

X_train, y_train = train_df[feature_cols], train_df[TARGET_COL]
X_valid, y_valid = valid_df[feature_cols], valid_df[TARGET_COL]
X_test, y_test = test_df[feature_cols], test_df[TARGET_COL]

# ===============================
# 4️⃣ 建立 LightGBM Dataset
# ===============================
lgb_train = lgb.Dataset(X_train, y_train)
lgb_valid = lgb.Dataset(X_valid, y_valid, reference=lgb_train)

# ===============================
# 5️⃣ 設定參數
# ===============================
params = {
    "objective": "regression",
    "metric": "rmse",
    "boosting_type": "gbdt",
    "learning_rate": 0.05,
    "num_leaves": 31,
    "max_depth": -1,
    "verbose": -1
}

# ===============================
# 6️⃣ 訓練模型
# ===============================
gbm = lgb.train(
    params,
    lgb_train,
    num_boost_round=1000,
    valid_sets=[lgb_train, lgb_valid],
    valid_names=["train", "valid"],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)

# ===============================
# 7️⃣ 測試與多指標評估
# ===============================
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)

# 計算指標
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n" + "="*30)
print("📊 模型評估報表 (Test Set)")
print("="*30)
print(f"MSE  (均方誤差): {mse:.4f}")
print(f"RMSE (均方根誤差): {rmse:.4f}")
print(f"MAE  (平均絕對誤差): {mae:.4f}")
print(f"R²   (判定係數): {r2:.4f}")
print("="*30)

# ===============================
# 8️⃣ 視覺化比較圖
# ===============================
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label="Actual Price", color="blue", alpha=0.7)
plt.plot(y_pred, label="Predicted Price", color="red", linestyle="--", alpha=0.8)
plt.title(f"Kai-lan Price Prediction (R²: {r2:.3f})")
plt.xlabel("Sample Index (Time Sequence)")
plt.ylabel("Price (NTD/kg)")
plt.legend()
plt.grid(True)
plt.show()

# ===============================
# 9️⃣ 儲存模型
# ===============================
MODEL_FILE = output_dir / "lgb_model_Kai-lan.txt"
gbm.save_model(str(MODEL_FILE))
print(f"\n✅ 模型已儲存至 {MODEL_FILE}")