from flask import Flask, jsonify, request
import pandas as pd
import os

app = Flask(__name__)

# API 來提供交易對的歷史資料及 VWAP、預測結果
@app.route("/api/chart")
def chart_data():
    symbol = request.args.get("symbol", default="BTC/USDT")
    symbol_filename = symbol.replace("/", "").lower()
    file_path = f"data/history_{symbol_filename}.csv"

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        return jsonify({"error": "資料未找到"}), 404

    # 只取近20筆資料
    df = df.tail(20)
    chart_data = {
        "timestamp": df["timestamp"].tolist(),
        "price": df["close"].tolist(),
        "vwap": (((df["high"] + df["low"] + df["close"]) / 3).round(4)).tolist(),
        "prediction": df["prediction"].tolist() if "prediction" in df else ["未知"] * len(df),
    }
    return jsonify(chart_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
