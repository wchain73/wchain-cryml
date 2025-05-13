import os
import pandas as pd
import pickle
from datetime import datetime
from backend.ml_core import fetch_8h_kline, fetch_binance_futures_data, compute_features
import telegram
from telegram import Bot
import asyncio
from flask import Flask, jsonify, request

# Telegram Bot 設定
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
bot = Bot(token=TELEGRAM_TOKEN)

# 模型、scaler 路徑設定
MODEL_PATH = "xgb_model.pkl"
SCALER_PATH = "scaler.pkl"
CSV_PATH = "data/market_features.csv"

app = Flask(__name__)


# 取得可用的交易對列表
def get_symbols():
    if not os.path.exists(CSV_PATH):
        return []
    df = pd.read_csv(CSV_PATH)
    return sorted(df["symbol"].dropna().unique().tolist())


# 取得最新的市場數據
def get_latest_data():
    if not os.path.exists(CSV_PATH):
        return []
    df = pd.read_csv(CSV_PATH)
    latest = df.sort_values("timestamp", ascending=False).groupby("symbol").first().reset_index()
    return latest.to_dict(orient="records")


# 取得歷史走勢數據
def get_historical_chart_data(symbol):
    if not os.path.exists(CSV_PATH):
        return {"labels": [], "prediction": [], "vwap_diff": []}
    df = pd.read_csv(CSV_PATH)
    symbol_data = df[df["symbol"] == symbol]
    if symbol_data.empty:
        return {"labels": [], "prediction": [], "vwap_diff": []}

    labels = symbol_data["timestamp"].tolist()
    vwap_diff = symbol_data["X4_vwap_diff"].tolist()
    prediction = symbol_data["Y"].tolist()
    return {"labels": labels, "vwap_diff": vwap_diff, "prediction": prediction}


# 預測並發送 Telegram 通知
async def predict_and_notify(df):
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler, label_encoder = pickle.load(f)
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        return

    X = df[["X1_volume_diff", "X2_OI_diff", "X3_funding_rate_diff", "X4_vwap_diff"]]
    X_scaled = scaler.transform(X)
    preds = model.predict(X_scaled)
    df["prediction"] = label_encoder.inverse_transform(preds)

    msg = f"\ud83d\udcca 預測結果 ({datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC)\n"
    top_results = df[["symbol", "prediction"]].groupby("prediction").head(5)
    for _, row in top_results.iterrows():
        msg += f"{row['symbol']}: {row['prediction']}\n"

    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
    print("Telegram notification sent.")


# 路由 1: 取得所有支持的交易對
@app.route('/symbols', methods=['GET'])
def get_symbols_route():
    symbols = get_symbols()
    return jsonify(symbols)


# 路由 2: 取得最新市場數據
@app.route('/latest-data', methods=['GET'])
def latest_data_route():
    latest_data = get_latest_data()
    return jsonify(latest_data)


# 路由 3: 取得指定交易對的歷史走勢數據
@app.route('/historical-data', methods=['GET'])
def historical_data_route():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400
    historical_data = get_historical_chart_data(symbol)
    return jsonify(historical_data)


# 路由 4: 觸發預測並發送通知
@app.route('/predict', methods=['POST'])
def predict_route():
    if not os.path.exists(CSV_PATH):
        return jsonify({"error": "CSV file not found."}), 500

    df = pd.read_csv(CSV_PATH)
    # 發送預測通知的異步操作
    asyncio.run(predict_and_notify(df))
    return jsonify({"status": "Prediction and notification sent."})


if __name__ == '__main__':
    # 手動抓資料並訓練模型
    df = fetch_all_features()
    df.to_csv("market_features.csv", mode='a', index=False, header=not os.path.exists("market_features.csv"))
    train_model(df)
    app.run(debug=True)
