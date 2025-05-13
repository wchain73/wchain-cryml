from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.routes import get_symbols, get_latest_data, get_historical_chart_data
from backend.routes import app

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "🚀 Crypto ML API running!"

@app.route("/api/symbols")
def symbols():
    return jsonify(get_symbols())

@app.route("/api/latest")
def latest():
    return jsonify(get_latest_data())

@app.route("/api/chart")
def chart():
    symbol = request.args.get("symbol", "BTC/USDT")
    return jsonify(get_historical_chart_data(symbol))

if __name__ == "__main__":
    # 手動抓資料並訓練模型
    df = fetch_all_features()
    df.to_csv("market_features.csv", mode='a', index=False, header=not os.path.exists("market_features.csv"))
    train_model(df)

    app.run(host="0.0.0.0", port=9600)
