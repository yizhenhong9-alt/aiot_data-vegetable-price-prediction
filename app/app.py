import streamlit as st
import pandas as pd
import os
from datetime import datetime
import glob

# 設定頁面配置
st.set_page_config(
    page_title="蔬菜價格預測系統",
    page_icon="🥬",
    layout="wide"
)

# 蔬菜資訊配置（可輕鬆添加新蔬菜）
VEGETABLE_INFO = {
    "cabbage": {
        "name": "甘藍",
        "model_file": "lgb_model_cabbage.txt",
        "prediction_file": "finalPredict/甘藍_full_prediction.csv",
        "icon": "🥬"
    },
    "bok_choy": {
        "name": "小白菜",
        "model_file": "lgb_model_bok_choy.txt",
        "prediction_file": "finalPredict/小白菜_full_prediction.csv",
        "icon": "🥬"
    },
    "chinese_kale": {
        "name": "芥藍",
        "model_file": "lgb_model_chinese_kale.txt",
        "prediction_file": "finalPredict/芥藍_full_prediction.csv",
        "icon": "🥦"
    },
    "celery": {
        "name": "芹菜",
        "model_file": "lgb_model_celery.txt",
        "prediction_file": "finalPredict/芹菜_full_prediction.csv",
        "icon": "🌿"
    },
    "chrysanthemum": {
        "name": "茼蒿",
        "model_file": "lgb_model_chrysanthemum.txt",
        "prediction_file": "finalPredict/茼蒿_full_prediction.csv",
        "icon": "🌱"
    },
    "spinach": {
        "name": "菠菜",
        "model_file": "lgb_model_spinach.txt",
        "prediction_file": "finalPredict/菠菜_full_prediction.csv",
        "icon": "🥬"
    }
}

# 食譜資料
RECIPES = {
    "甘藍": [
        {
            "name": "高麗菜炒肉片",
            "ingredients": ["甘藍 半顆", "豬肉片 200g", "蒜頭 3瓣", "醬油 1大匙", "鹽 適量"],
            "steps": [
                "甘藍洗淨切片，蒜頭切片",
                "肉片用醬油醃製10分鐘",
                "熱鍋炒香蒜片和肉片",
                "加入甘藍快炒至軟",
                "加鹽調味即可"
            ]
        },
        {
            "name": "涼拌甘藍絲",
            "ingredients": ["甘藍 半顆", "紅蘿蔔 1條", "白醋 3大匙", "糖 2大匙", "鹽 1小匙"],
            "steps": [
                "甘藍和紅蘿蔔切細絲",
                "用鹽抓醃15分鐘後擠乾水分",
                "混合白醋和糖製成醬汁",
                "將醬汁拌入蔬菜絲",
                "冷藏30分鐘後即可食用"
            ]
        },
        {
            "name": "甘藍豬肉捲",
            "ingredients": ["甘藍葉 8片", "豬肉片 8片", "紅蘿蔔絲 適量", "醬油 2大匙", "味醂 1大匙"],
            "steps": [
                "甘藍葉汆燙軟化",
                "每片甘藍葉包入肉片和紅蘿蔔絲捲起",
                "熱鍋煎至肉片熟透",
                "加入醬油和味醂煮至收汁",
                "切段擺盤即可"
            ]
        }
    ],
    "小白菜": [
        {
            "name": "清炒小白菜",
            "ingredients": ["小白菜 300g", "蒜頭 3瓣", "鹽 適量", "香油 少許"],
            "steps": [
                "小白菜洗淨切段，蒜頭切片",
                "熱鍋下油，爆香蒜片",
                "加入小白菜快炒2-3分鐘",
                "加鹽調味，起鍋前淋香油"
            ]
        },
        {
            "name": "小白菜豆腐湯",
            "ingredients": ["小白菜 200g", "嫩豆腐 1盒", "高湯 500ml", "薑片 3片", "鹽 適量"],
            "steps": [
                "小白菜洗淨切段，豆腐切塊",
                "高湯加薑片煮滾",
                "加入豆腐煮3分鐘",
                "加入小白菜煮至軟",
                "加鹽調味即可"
            ]
        },
        {
            "name": "蠔油小白菜",
            "ingredients": ["小白菜 300g", "蠔油 2大匙", "蒜頭 4瓣", "糖 1小匙"],
            "steps": [
                "小白菜洗淨切段",
                "蒜頭切末",
                "熱鍋炒香蒜末",
                "加入小白菜快炒",
                "加入蠔油和糖拌炒均勻"
            ]
        }
    ],
    "芥藍": [
        {
            "name": "蠔油芥藍",
            "ingredients": ["芥藍 300g", "蠔油 2大匙", "蒜頭 3瓣", "糖 1小匙", "水 3大匙"],
            "steps": [
                "芥藍洗淨切段，蒜頭切片",
                "芥藍汆燙1分鐘後撈起",
                "熱鍋爆香蒜片",
                "加入蠔油、糖和水煮滾",
                "淋在芥藍上即可"
            ]
        },
        {
            "name": "芥藍炒牛肉",
            "ingredients": ["芥藍 250g", "牛肉片 200g", "薑片 3片", "醬油 1大匙", "米酒 1大匙"],
            "steps": [
                "牛肉用醬油和米酒醃製15分鐘",
                "芥藍切段，分開菜梗和葉子",
                "熱鍋炒香薑片和牛肉",
                "先炒菜梗，再加葉子",
                "快炒至熟即可"
            ]
        },
        {
            "name": "涼拌芥藍",
            "ingredients": ["芥藍 300g", "芝麻醬 2大匙", "醬油 1大匙", "醋 1大匙", "糖 1小匙"],
            "steps": [
                "芥藍汆燙後泡冰水",
                "瀝乾切段擺盤",
                "混合芝麻醬、醬油、醋和糖",
                "淋在芥藍上",
                "撒上白芝麻即可"
            ]
        }
    ],
    "芹菜": [
        {
            "name": "芹菜炒豆乾",
            "ingredients": ["芹菜 200g", "豆乾 5片", "辣椒 1條", "醬油 1大匙", "鹽 適量"],
            "steps": [
                "芹菜切段，豆乾切絲",
                "辣椒切片",
                "熱鍋炒香辣椒",
                "加入豆乾炒香",
                "加入芹菜和醬油快炒"
            ]
        },
        {
            "name": "芹菜炒花枝",
            "ingredients": ["芹菜 150g", "花枝 200g", "薑片 3片", "米酒 1大匙", "鹽 適量"],
            "steps": [
                "花枝切花後汆燙",
                "芹菜切段",
                "熱鍋炒香薑片",
                "加入花枝和米酒",
                "加入芹菜快炒調味"
            ]
        },
        {
            "name": "芹菜拌花生",
            "ingredients": ["芹菜 200g", "花生 100g", "香油 1大匙", "鹽 1小匙", "糖 1小匙"],
            "steps": [
                "芹菜汆燙後切段",
                "花生炒香或用熟花生",
                "芹菜和花生混合",
                "加入香油、鹽和糖",
                "拌勻後冷藏即可"
            ]
        }
    ],
    "茼蒿": [
        {
            "name": "清炒茼蒿",
            "ingredients": ["茼蒿 300g", "蒜頭 3瓣", "鹽 適量", "米酒 1大匙"],
            "steps": [
                "茼蒿洗淨切段，蒜頭切片",
                "熱鍋下油爆香蒜片",
                "加入茼蒿快炒",
                "加米酒和鹽調味",
                "炒至軟即可起鍋"
            ]
        },
        {
            "name": "茼蒿炒蛋",
            "ingredients": ["茼蒿 200g", "雞蛋 3顆", "鹽 適量", "白胡椒 適量"],
            "steps": [
                "茼蒿洗淨切碎",
                "雞蛋打散加鹽",
                "將茼蒿拌入蛋液",
                "熱鍋下油",
                "倒入蛋液煎至兩面金黃"
            ]
        },
        {
            "name": "茼蒿拌豆腐",
            "ingredients": ["茼蒿 150g", "嫩豆腐 1盒", "芝麻醬 2大匙", "醬油 1大匙"],
            "steps": [
                "茼蒿汆燙後切碎",
                "豆腐蒸熟後壓碎",
                "混合茼蒿和豆腐",
                "加入芝麻醬和醬油",
                "拌勻即可"
            ]
        }
    ],
    "菠菜": [
        {
            "name": "清炒菠菜",
            "ingredients": ["菠菜 300g", "蒜頭 4瓣", "鹽 適量", "橄欖油 2大匙"],
            "steps": [
                "菠菜洗淨切段，蒜頭切片",
                "熱鍋下油爆香蒜片",
                "加入菠菜快炒",
                "加鹽調味",
                "炒軟即可起鍋"
            ]
        },
        {
            "name": "菠菜豬肝湯",
            "ingredients": ["菠菜 200g", "豬肝 150g", "薑片 5片", "枸杞 適量", "米酒 1大匙"],
            "steps": [
                "豬肝切片泡水去血水",
                "菠菜洗淨切段",
                "水煮滾加薑片和米酒",
                "加入豬肝煮熟",
                "最後加菠菜和枸杞即可"
            ]
        },
        {
            "name": "菠菜拌芝麻",
            "ingredients": ["菠菜 300g", "白芝麻 2大匙", "醬油 1大匙", "糖 1小匙", "香油 1大匙"],
            "steps": [
                "菠菜汆燙後泡冰水",
                "擠乾水分切段",
                "白芝麻炒香研碎",
                "混合醬油、糖和香油",
                "拌入菠菜和芝麻即可"
            ]
        }
    ]
}


@st.cache_data
def load_predictions(vegetable_key):
    """載入預測資料"""
    file_path = VEGETABLE_INFO[vegetable_key]["prediction_file"]
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    return None


def get_latest_predictions(vegetable_key, days=5):
    """獲取最新N天的預測價格"""
    df = load_predictions(vegetable_key)
    if df is not None and '預測價格' in df.columns:
        # 取最後N筆資料
        latest = df.tail(days)[['日期', '預測價格']].copy()
        latest['蔬菜'] = VEGETABLE_INFO[vegetable_key]["name"]
        return latest
    return None


def analyze_price_trend(predictions_df):
    """分析價格趨勢"""
    if predictions_df is None or len(predictions_df) == 0:
        return "無法分析"
    
    prices = predictions_df['預測價格'].values
    
    # 計算價格變化
    if len(prices) >= 2:
        first_price = prices[0]
        last_price = prices[-1]
        change_rate = ((last_price - first_price) / first_price) * 100
        
        if change_rate > 5:
            return "上漲"
        elif change_rate < -5:
            return "下跌"
        else:
            return "平穩"
    return "平穩"


def get_purchase_recommendation(all_predictions):
    """根據價格預測給出購買建議"""
    recommendations = []
    
    for veg_key, pred_df in all_predictions.items():
        if pred_df is not None and len(pred_df) > 0:
            veg_name = VEGETABLE_INFO[veg_key]["name"]
            trend = analyze_price_trend(pred_df)
            prices = pred_df['預測價格'].values
            dates = pred_df['日期'].values
            
            # 找到最低價的日期
            min_price_idx = prices.argmin()
            min_price_date = dates[min_price_idx]
            min_price = prices[min_price_idx]
            
            rec = {
                "vegetable": veg_name,
                "trend": trend,
                "best_date": min_price_date,
                "best_price": min_price,
                "current_price": prices[0] if len(prices) > 0 else 0
            }
            recommendations.append(rec)
    
    return recommendations


def display_recipe(recipe, vegetable_name):
    """顯示食譜"""
    with st.expander(f"📖 {recipe['name']}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛒 食材")
            for ingredient in recipe['ingredients']:
                st.write(f"• {ingredient}")
        
        with col2:
            st.subheader("👨‍🍳 步驟")
            for i, step in enumerate(recipe['steps'], 1):
                st.write(f"{i}. {step}")


def main():
    # 標題
    st.title("🥬 蔬菜價格預測與購買建議系統")
    st.markdown("---")
    
    # 側邊欄
    st.sidebar.title("📊 系統資訊")
    st.sidebar.info(f"目前追蹤 {len(VEGETABLE_INFO)} 種蔬菜")
    st.sidebar.markdown("---")
    st.sidebar.subheader("蔬菜列表")
    for veg_key, veg_info in VEGETABLE_INFO.items():
        st.sidebar.write(f"{veg_info['icon']} {veg_info['name']}")
    
    # 主要內容
    st.header("📈 未來五天價格預測")
    
    # 載入所有蔬菜的預測
    all_predictions = {}
    for veg_key in VEGETABLE_INFO.keys():
        pred = get_latest_predictions(veg_key, days=5)
        all_predictions[veg_key] = pred
    
    # 顯示每種蔬菜的預測
    cols = st.columns(len(VEGETABLE_INFO))
    for idx, (veg_key, veg_info) in enumerate(VEGETABLE_INFO.items()):
        with cols[idx]:
            st.subheader(f"{veg_info['icon']} {veg_info['name']}")
            pred_df = all_predictions[veg_key]
            
            if pred_df is not None:
                # 顯示預測表格
                display_df = pred_df[['日期', '預測價格']].copy()
                display_df['預測價格'] = display_df['預測價格'].round(2)
                display_df = display_df.rename(columns={'預測價格': '價格 (元/公斤)'})
                st.dataframe(display_df, hide_index=True, width='stretch')
                
                # 顯示圖表
                st.line_chart(pred_df.set_index('日期')['預測價格'])
                
                # 顯示趨勢
                trend = analyze_price_trend(pred_df)
                if trend == "上漲":
                    st.warning(f"📈 趨勢：{trend}")
                elif trend == "下跌":
                    st.success(f"📉 趨勢：{trend}")
                else:
                    st.info(f"➡️ 趨勢：{trend}")
            else:
                st.error("無預測資料")
    
    st.markdown("---")
    
    # 購買建議
    st.header("💡 購買建議")
    recommendations = get_purchase_recommendation(all_predictions)
    
    if recommendations:
        # 找出價格上漲和下跌的蔬菜
        rising = [r for r in recommendations if r['trend'] == "上漲"]
        falling = [r for r in recommendations if r['trend'] == "下跌"]
        stable = [r for r in recommendations if r['trend'] == "平穩"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 最佳購買時機")
            for rec in recommendations:
                st.write(f"**{rec['vegetable']}**：建議在 **{rec['best_date']}** 購買")
                st.write(f"預測最低價：**{rec['best_price']:.2f}** 元/公斤")
                st.write("---")
        
        with col2:
            st.subheader("🔔 價格提醒")
            
            if rising:
                st.warning("📈 **價格上漲的蔬菜**")
                for rec in rising:
                    st.write(f"• {rec['vegetable']}：建議盡早購買或選擇其他蔬菜")
            
            if falling:
                st.success("📉 **價格下跌的蔬菜**")
                for rec in falling:
                    st.write(f"• {rec['vegetable']}：可等待更優惠的價格")
            
            if stable:
                st.info("➡️ **價格平穩的蔬菜**")
                for rec in stable:
                    st.write(f"• {rec['vegetable']}：價格穩定，可隨時購買")
    
    st.markdown("---")
    
    # 食譜區域
    st.header("🍳 美味食譜推薦")
    
    # 為每種蔬菜顯示食譜
    for veg_key, veg_info in VEGETABLE_INFO.items():
        veg_name = veg_info['name']
        if veg_name in RECIPES:
            st.subheader(f"{veg_info['icon']} {veg_name}料理")
            
            # 使用列來排列食譜
            recipe_cols = st.columns(len(RECIPES[veg_name]))
            for idx, recipe in enumerate(RECIPES[veg_name]):
                with recipe_cols[idx]:
                    display_recipe(recipe, veg_name)
            
            st.markdown("---")


if __name__ == "__main__":
    main()
