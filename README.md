# 蔬菜價格預測與購買建議系統 🥬
## Vegetable Price Prediction and Shopping Recommendation System

一個基於機器學習的蔬菜價格預測與購買建議平台，整合市場交易數據和氣象資料，使用 LightGBM 模型進行精準價格預測。本系統提供 Web UI 介面，幫助消費者了解蔬菜價格走勢、獲得購買建議，並推薦相應的食譜。

**A machine learning-based vegetable price prediction and shopping recommendation platform that integrates market trading data with weather information to help consumers make informed purchasing decisions with LightGBM models.**

---

## 📋 目錄 | Table of Contents

- [專案概述](#專案概述)
- [功能特性](#功能特性)
- [系統架構](#系統架構)
- [快速開始](#快速開始)
- [資料流程](#資料流程)
- [項目結構](#項目結構)
- [使用指南](#使用指南)
- [模型訓練](#模型訓練)
- [支持的蔬菜](#支持的蔬菜)
- [技術棧](#技術棧)
- [常見問題](#常見問題)

---

## 🎯 專案概述 | Project Overview

本專案旨在透過整合**市場交易數據**（價格、交易量等）和**氣象數據**（溫度、濕度、降雨量等），建立準確的蔬菜價格預測模型。

**主要目標：**
 預測蔬菜價格走勢，幫助消費者選擇最佳購買時機
 提供個性化的購買建議，讓消費者買得聰明更省錢
 透過科學的數據分析降低盲目購物的成本
 根據價格推薦合適的食譜，優化家庭飲食預算

**核心特點：**
- ✅ 多蔬菜支持（甘藍、小白菜、芥藍、芹菜、茼蒿、菠菜）
- ✅ 融合市場和氣象特徵
- ✅ 高精度 LightGBM 模型
- ✅ 互動式 Streamlit Web 應用
- ✅ 完整的數據處理管道

---

## ⚡ 功能特性 | Features

### 核心功能
1. **價格預測**：預測未來蔬菜價格走勢，幫助把握購買時機
2. **購買建議**：根據當前價格和歷史趨勢提供智慧購買建議
3. **趨勢分析**：可視化展示價格變化趨勢，一目了然
4. **食譜推薦**：推薦當季便宜蔬菜的美味食譜，省錢又健康
5. **歷史對比**：查看歷史價格和預測準確度，增進購買信心

### 支持蔬菜
- 🥬 **甘藍 (Cabbage)**
- 🥬 **小白菜 (Bok Choy)**
- 🥦 **芥藍 (Chinese Kale)**
- 🌿 **芹菜 (Celery)**
- 🌱 **茼蒿 (Chrysanthemum)**
- 🥬 **菠菜 (Spinach)**

---

## 🏗️ 系統架構 | System Architecture

```
📊 蔬菜價格預測系統
│
├─ 📁 數據層 (Data Layer)
│  ├─ 市場交易數據 (Market Data)
│  │  └─ 價格、交易量、高低價等
│  └─ 氣象數據 (Weather Data)
│     └─ 溫度、濕度、降雨量等
│
├─ 🔧 處理層 (Processing Layer)
│  ├─ 預處理 (Preprocessing)
│  │  ├─ 數據清理
│  │  ├─ 缺值處理
│  │  └─ 異常值檢測
│  ├─ 特徵工程 (Feature Engineering)
│  │  ├─ Lag 特徵（1、7、14天）
│  │  ├─ 移動平均（3、7天）
│  │  ├─ 星期特徵
│  │  └─ 複合特徵
│  └─ 數據融合 (Data Merging)
│     └─ 市場與氣象數據合併
│
├─ 🤖 模型層 (Model Layer)
│  ├─ 模型訓練 (Training)
│  │  └─ LightGBM Regressor
│  ├─ 驗證評估 (Validation)
│  │  ├─ RMSE
│  │  ├─ MAE
│  │  └─ R² Score
│  └─ 模型保存 (Model Persistence)
│
└─ 🎨 應用層 (Application Layer)
   └─ Streamlit Web UI
      ├─ 價格預測界面
      ├─ 趨勢分析圖表
      ├─ 歷史數據查詢
      └─ 食譜推薦
```

---

## 🚀 快速開始 | Quick Start

### 環境需求
- Python 3.8+
- pip 或 conda 套件管理器

### 1️⃣ 克隆專案
```bash
git clone <repository-url>
cd aiot_data-vegetable-price-prediction
```

### 2️⃣ 安裝依賴
```bash
pip install -r requirements.txt
```

**所需套件：**
- `pandas` - 數據處理
- `lightgbm` - 機器學習模型
- `scikit-learn` - 評估指標
- `streamlit` - Web 應用框架
- `matplotlib`, `seaborn` - 數據視覺化

### 3️⃣ 運行應用
```bash
cd app
streamlit run app.py
```

應用將在 `http://localhost:8501` 啟動

---

## 📊 資料流程 | Data Pipeline

### 完整流程圖

```
原始數據 (Raw Data)
    ↓
┌─────────────────────────────┐
│  1️⃣ 分割 (Split)            │
│  split_raw_market.py        │
│  split_raw_weather.py       │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  2️⃣ 預處理 (Preprocessing)  │
│  preprocessing_market.py    │
│  preprocessing_weather.py   │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  3️⃣ 特徵工程 (Engineering)   │
│  engineering_market.py      │
│  engineering_weather.py     │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  4️⃣ 融合 (Merging)          │
│  merge_weather_and_market.py│
│  (訓練/驗證/測試集分割)      │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  5️⃣ 模型訓練 (Training)      │
│  train_model.py             │
│  (LightGBM)                 │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  6️⃣ 預測 (Prediction)       │
│  生成預測結果 CSV            │
└─────────────────────────────┘
    ↓
預測結果 & 模型文件
```

### 各步驟詳解

#### 📍 Step 1: 數據分割 (Splitting)
```python
# src/split_raw_market.py
# 按月份分割原始市場數據，便於模塊化處理
市場原始數據 → split_market/ (按月)
```

```python
# src/split_raw_weather.py
# 按月份分割原始氣象數據
氣象原始數據 → split_weather/ (按月)
```

**輸入：** `dataset/raw_data/market/`, `dataset/raw_data/weather/`  
**輸出：** `dataset/raw_data/split_market/`, `dataset/raw_data/split_weather/`

---

#### 📍 Step 2: 數據預處理 (Preprocessing)
```python
# src/preprocessing_market.py
清理市場數據：
  ✓ 處理缺失值
  ✓ 異常值檢測
  ✓ 類型轉換
  ✓ 日期標準化
  ✓ 每日聚合（同日多市場取平均）
```

```python
# src/preprocessing_weather.py
清理氣象數據：
  ✓ 處理缺失值
  ✓ 溫度、濕度、降雨量數據驗證
  ✓ 日期配對
```

**輸入：** `dataset/raw_data/split_market/`, `dataset/raw_data/split_weather/`  
**輸出：** `dataset/processed_data/preprocessing/market/`, `dataset/processed_data/preprocessing/weather/`

---

#### 📍 Step 3: 特徵工程 (Feature Engineering)
```python
# src/engineering_market.py
市場特徵創建：
  1️⃣ Lag 特徵
     - 1天、7天、14天滯後價格
  2️⃣ 移動平均
     - 3天、7天移動平均價格
  3️⃣ 統計特徵
     - 價格區間 (上價 - 下價)
     - 交易量變化

# src/engineering_weather.py
氣象特徵創建：
  1️⃣ Lag 特徵
     - 過去溫度、濕度、降雨
  2️⃣ 移動平均
     - 7天平均溫度
  3️⃣ 複合特徵
     - 溫度差異、降雨累計
```

**輸入：** `dataset/processed_data/preprocessing/`  
**輸出：** `dataset/processed_data/feature_engineering/`

---

#### 📍 Step 4: 數據融合 (Merging)
```python
# src/merge_weather_and_market.py
融合步驟：
  1. 市場特徵 + 氣象特徵 → 合併
  2. 添加時間特徵 (weekday, is_weekend, is_mon, is_fri)
  3. 分割數據集
     - Train: 前 5 個月 (70%)
     - Valid: 倒數第 2 個月 (15%)
     - Test:  倒數第 1 個月 (15%)
```

**輸入：** `dataset/processed_data/feature_engineering/`  
**輸出：** `dataset/processed_data/merge_market_and_weather_after_engineering/`
- `train_蔬菜_after_engineering.csv`
- `valid_蔬菜_after_engineering.csv`
- `test_蔬菜_after_engineering.csv`

---

#### 📍 Step 5: 模型訓練 (Training)
```python
# src/train_model.py
訓練配置：
  ✅ 模型類型：LightGBM Regression
  ✅ 目標變數：價格 (元/公斤)
  ✅ 特徵：市場 + 氣象特徵
  ✅ 參數：
     - learning_rate: 0.05
     - num_leaves: 31
     - num_boost_round: 1000
     - early_stopping: 50 rounds
```

**訓練流程：**
```
1. 讀取訓練/驗證/測試數據
2. 創建 LightGBM Dataset
3. 設置超參數
4. 訓練模型（帶早停）
5. 評估模型
6. 保存模型文件 (.txt)
7. 生成預測結果
8. 可視化效果圖
```

---

#### 📍 Step 6: 預測生成 (Prediction)
- 使用訓練好的模型進行預測
- 生成 `finalPredict/蔬菜_full_prediction.csv`
- 包含實際價格、預測價格、誤差等

---

## 📁 項目結構 | Project Structure

```
aiot_data-vegetable-price-prediction/
│
├── README.md                          # 本文件
│
├── app/                               # 🎨 Streamlit 應用
│   ├── app.py                         # 主應用程式
│   ├── lgb_model_*.txt                # 預訓練模型
│   └── finalPredict/                  # 預測結果
│       ├── 小白菜_full_prediction.csv
│       ├── 甘藍_full_prediction.csv
│       ├── 芥藍_full_prediction.csv
│       ├── 芹菜_full_prediction.csv
│       ├── 茼蒿_full_prediction.csv
│       └── 菠菜_full_prediction.csv
│
├── src/                               # 🔧 數據處理腳本
│   ├── split_raw_market.py            # 分割市場數據
│   ├── split_raw_weather.py           # 分割氣象數據
│   ├── preprocessing_market.py        # 預處理市場數據
│   ├── preprocessing_weather.py       # 預處理氣象數據
│   ├── engineering_market.py          # 市場特徵工程
│   ├── engineering_weather.py         # 氣象特徵工程
│   ├── merge_weather_and_market.py    # 融合並分割數據
│   └── train_model.py                 # 訓練模型
│
└── dataset/                           # 📊 數據目錄
    ├── raw_data/                      # 原始數據
    │   ├── market/                    # 市場交易數據
    │   ├── weather/                   # 氣象數據
    │   ├── split_market/              # 分割後的市場數據
    │   └── split_weather/             # 分割後的氣象數據
    │
    ├── processed_data/                # 處理過的數據
    │   ├── preprocessing/             # 預處理結果
    │   │   ├── market/
    │   │   └── weather/
    │   ├── feature_engineering/       # 特徵工程結果
    │   │   ├── market/
    │   │   └── weather/
    │   └── merge_market_and_weather_after_engineering/  # 融合數據
    │
    ├── model/                         # 訓練好的模型
    │   ├── 小白菜/
    │   ├── 甘藍/
    │   ├── 芥藍/
    │   ├── 芹菜/
    │   ├── 茼蒿/
    │   ├── 菠菜/
    │   ├── cabbage/
    │   ├── Kai-lan/
    │   ├── ponkan/
    │   └── strawberry/
    │
    ├── predict/                       # 預測結果數據
    │   └── [蔬菜名]/test_with_prediction.csv
    │
    └── finalPredict/                  # 最終預測結果
        └── [蔬菜名]_full_prediction.csv
```

---

## 🎯 使用指南 | Usage Guide

### 運行完整數據管道

#### 方案 A：運行所有步驟（從頭開始）
```bash
# 1. 分割數據
python src/split_raw_market.py
python src/split_raw_weather.py

# 2. 預處理
python src/preprocessing_market.py
python src/preprocessing_weather.py

# 3. 特徵工程
python src/engineering_market.py
python src/engineering_weather.py

# 4. 數據融合
python src/merge_weather_and_market.py

# 5. 訓練模型
python src/train_model.py
```

#### 方案 B：直接使用預訓練模型
如果您已有訓練好的模型，只需運行應用：
```bash
cd app
streamlit run app.py
```

### Web UI 使用方法

#### 1️⃣ 蔬菜選擇
- 在側邊欄選擇要查看的蔬菜
- 支持 6 種常見蔬菜

#### 2️⃣ 查看預測
- **預測圖表**：實時價格 vs. 預測價格
- **模型性能**：RMSE、MAE、R² 等指標
- **預測數據**：詳細的預測結果表格

#### 3️⃣ 歷史數據
- 查看歷史的實際價格和預測
- 支持日期篩選

#### 4️⃣ 食譜推薦
- 基於當前蔬菜推薦食譜
- 包含詳細的材料和步驟

---

## 🤖 模型訓練 | Model Training

### 訓練配置

```python
params = {
    "objective": "regression",           # 迴歸任務
    "metric": "rmse",                    # 評估指標
    "boosting_type": "gbdt",             # 梯度提升決策樹
    "learning_rate": 0.05,               # 學習率
    "num_leaves": 31,                    # 葉子節點數
    "max_depth": -1,                     # 最大深度（無限制）
    "verbose": -1                        # 靜默模式
}
```

### 訓練流程

```python
# 創建 LightGBM 數據集
lgb_train = lgb.Dataset(X_train, y_train)
lgb_valid = lgb.Dataset(X_valid, y_valid, reference=lgb_train)

# 訓練模型
gbm = lgb.train(
    params,
    lgb_train,
    num_boost_round=1000,
    valid_sets=[lgb_train, lgb_valid],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)
```

### 模型評估指標

| 指標 | 公式 | 說明 |
|------|------|------|
| **RMSE** | $\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$ | 均方根誤差，越小越好 |
| **MAE** | $\frac{1}{n}\sum_{i=1}^{n}\|y_i - \hat{y}_i\|$ | 平均絕對誤差，越小越好 |
| **R²** | $1 - \frac{SS_{res}}{SS_{tot}}$ | 決定係數，越接近 1 越好 |

### 預測輸出

模型訓練完成後會生成：
1. **模型文件**：`lgb_model_蔬菜.txt`
2. **預測 CSV**：包含以下列：
   - 日期 (Date)
   - 實際價格 (Actual Price)
   - 預測價格 (Predicted Price)
   - 誤差 (Error)

---

## 🥬 支持的蔬菜 | Supported Vegetables

### 蔬菜清單

| 蔬菜 | 英文名 | 模型文件 | 預測文件 | 圖標 |
|------|--------|---------|---------|------|
| 甘藍 | Cabbage | `lgb_model_cabbage.txt` | `甘藍_full_prediction.csv` | 🥬 |
| 小白菜 | Bok Choy | `lgb_model_bok_choy.txt` | `小白菜_full_prediction.csv` | 🥬 |
| 芥藍 | Chinese Kale | `lgb_model_chinese_kale.txt` | `芥藍_full_prediction.csv` | 🥦 |
| 芹菜 | Celery | `lgb_model_celery.txt` | `芹菜_full_prediction.csv` | 🌿 |
| 茼蒿 | Chrysanthemum | `lgb_model_chrysanthemum.txt` | `茼蒿_full_prediction.csv` | 🌱 |
| 菠菜 | Spinach | `lgb_model_spinach.txt` | `菠菜_full_prediction.csv` | 🥬 |

### 添加新蔬菜

若要添加新蔬菜支持，請修改 `app/app.py` 中的 `VEGETABLE_INFO`：

```python
VEGETABLE_INFO = {
    "vegetable_code": {
        "name": "蔬菜中文名",
        "model_file": "lgb_model_vegetable_code.txt",
        "prediction_file": "finalPredict/蔬菜中文名_full_prediction.csv",
        "icon": "🥬"
    }
}
```

---

## 🛠️ 技術棧 | Technology Stack

### 核心庫

| 庫 | 版本 | 用途 |
|----|------|------|
| **pandas** | ≥1.3.0 | 數據處理和分析 |
| **LightGBM** | ≥3.0.0 | 機器學習模型 |
| **scikit-learn** | ≥0.24.0 | 模型評估和度量 |
| **Streamlit** | ≥1.0.0 | Web 應用框架 |
| **matplotlib** | ≥3.3.0 | 數據視覺化 |
| **seaborn** | ≥0.11.0 | 高級視覺化 |
| **numpy** | ≥1.19.0 | 數值計算 |

### 環境要求
- **Python**: 3.8 或更高版本
- **操作系統**: Windows, macOS, Linux
- **RAM**: 至少 4GB（推薦 8GB）

### 依賴安裝

創建 `requirements.txt`：
```
pandas>=1.3.0
lightgbm>=3.0.0
scikit-learn>=0.24.0
streamlit>=1.0.0
matplotlib>=3.3.0
seaborn>=0.11.0
numpy>=1.19.0
```

安裝命令：
```bash
pip install -r requirements.txt
```

---

## ❓ 常見問題 | FAQ

### Q1: 如何開始使用這個項目？
**A:** 請按照「快速開始」部分的步驟：
1. 克隆 repo
2. 安裝依賴
3. 運行 `streamlit run app/app.py`

### Q2: 如何使用自己的數據重新訓練模型？
**A:** 
1. 將新數據放入 `dataset/raw_data/market/` 和 `dataset/raw_data/weather/`
2. 按順序運行 `src/` 中的所有腳本
3. 新的模型文件將保存到 `dataset/model/`

### Q3: 模型文件在哪裡？
**A:** 
- 已訓練的模型在 `app/` 和 `dataset/model/` 目錄
- 格式為 LightGBM 的文本格式 (`*.txt`)

### Q4: 預測結果如何解讀？
**A:** 預測 CSV 文件包含：
- 日期：預測的日期
- 實際價格：市場上的真實價格
- 預測價格：模型預測的價格
- 誤差：實際價格 - 預測價格

### Q5: 如何改進模型準確度？
**A:** 可以嘗試：
1. **增加數據**：收集更多歷史數據
2. **調整特徵**：修改 lag 天數、移動平均窗口
3. **調整超參數**：`learning_rate`, `num_leaves`, `max_depth`
4. **增加特徵**：添加市場或氣象的新特徵

### Q6: Streamlit 應用無法啟動？
**A:** 檢查以下事項：
```bash
# 確認安裝了 Streamlit
pip install streamlit

# 確認在正確目錄
cd app
streamlit run app.py

# 如果仍有問題，檢查日誌
streamlit run app.py --logger.level=debug
```

### Q7: 數據文件格式有什麼要求？
**A:** 
- **市場數據**：需包含日期、價格、交易量等列
- **氣象數據**：需包含日期、溫度、濕度、降雨量等列
- **格式**：CSV (逗號分隔或其他)
- **編碼**：建議使用 UTF-8

### Q8: 可以預測其他蔬菜嗎？
**A:** 可以！按以下步驟：
1. 準備新蔬菜的市場和氣象數據
2. 運行完整的數據處理管道
3. 訓練新模型
4. 在 `app.py` 中添加新蔬菜配置

---

## 📊 模型性能示例 | Model Performance

以下是各蔬菜模型的典型性能指標（示例）：

| 蔬菜 | RMSE | MAE | R² |
|------|------|-----|-----|
| 甘藍 | 2.45 | 1.89 | 0.87 |
| 小白菜 | 1.23 | 0.95 | 0.91 |
| 芥藍 | 3.12 | 2.34 | 0.84 |
| 芹菜 | 2.67 | 2.01 | 0.86 |
| 茼蒿 | 1.98 | 1.54 | 0.89 |
| 菠菜 | 2.34 | 1.78 | 0.88 |

---

## 🤝 貢獻指南 | Contributing

歡迎提交 Issue 和 Pull Request！

### 提交流程
1. Fork 本倉庫
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打開 Pull Request

---

## 📝 許可證 | License

本項目採用 MIT 許可證。詳見 [LICENSE](LICENSE) 文件。

---

## 📧 聯繫方式 | Contact

如有問題或建議，歡迎透過以下方式聯繫：
- 提交 GitHub Issue
- 發送郵件至 [your-email@example.com]

---

## 🙏 致謝 | Acknowledgments

感謝以下開源項目和社區：
- [LightGBM](https://github.com/microsoft/LightGBM) - 高效梯度提升框架
- [Streamlit](https://streamlit.io/) - 快速構建數據應用
- [Scikit-learn](https://scikit-learn.org/) - 機器學習庫

---

## 📚 參考資源 | References

- [LightGBM 官方文檔](https://lightgbm.readthedocs.io/)
- [Streamlit 文檔](https://docs.streamlit.io/)
- [Pandas 文檔](https://pandas.pydata.org/docs/)
- [時間序列預測最佳實踐](https://machinelearningmastery.com/)

---

**最後更新：2025 年 12 月 28 日**

Happy Predicting! 🌾📈