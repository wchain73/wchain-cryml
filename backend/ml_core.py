import ccxt
import pandas as pd
import requests
import pickle
from datetime import datetime, timezone
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier

# 資料抓取
def fetch_8h_kline(symbol):
    exchange = ccxt.binance({
        "rateLimit": 1200, "options": {"defaultType": "future"}})
    market = symbol.replace('/', '')
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='15m', limit=32)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['symbol'] = market
    return df

def fetch_binance_futures_data(symbol):
    base = symbol.replace("/", "")
    try:
        fr = requests.get(f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={base}&limit=2").json()
        oi = requests.get(f"https://fapi.binance.com/futures/data/openInterestHist?symbol={base}&period=8h&limit=2").json()
        return {
            "funding_rate_diff": float(fr[-1]["fundingRate"]) - float(fr[-2]["fundingRate"]),
            "open_interest_diff": float(oi[-1]["sumOpenInterest"]) - float(oi[-2]["sumOpenInterest"])
        }
    except:
        return {"funding_rate_diff": 0, "open_interest_diff": 0}

def compute_features(df):
    vwap = (df['high'] + df['low'] + df['close']) / 3
    vwap_diff = vwap.iloc[-1] - vwap.iloc[-2]
    vol_diff = df['volume'].iloc[-1] - df['volume'].iloc[-2]
    price_diff = df['close'].iloc[-1] - df['close'].iloc[-2]
    return price_diff, vol_diff, vwap_diff

# 資料處理與訓練模型
def fetch_all_features():
    symbols = ["BTC/USDT", "ETH/USDT"]  # 自行替換為實際的交易對
    rows = []
    for symbol in symbols:
        try:
            df = fetch_8h_kline(symbol)
            price_diff, vol_diff, vwap_diff = compute_features(df)
            extra = fetch_binance_futures_data(symbol)
            label = "上漲" if price_diff > 0.01 else "下跌" if price_diff < -0.01 else "盤整"
            rows.append({
                "symbol": symbol,
                "Y": label,
                "X1_volume_diff": vol_diff,
                "X2_OI_diff": extra["open_interest_diff"],
                "X3_funding_rate_diff": extra["funding_rate_diff"],
                "X4_vwap_diff": vwap_diff,
                "timestamp": datetime.now(timezone.utc)
            })
        except Exception as e:
            print(f"Error on {symbol}: {e}")
    return pd.DataFrame(rows)

def train_model(df):
    X = df[["X1_volume_diff", "X2_OI_diff", "X3_funding_rate_diff", "X4_vwap_diff"]]
    y = df["Y"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = XGBClassifier()
    model.fit(X_train_scaled, y_train)
    with open("xgb_model.pkl", 'wb') as f:
        pickle.dump(model, f)
    with open("scaler.pkl", 'wb') as f:
        pickle.dump((scaler, label_encoder), f)
    print("Model saved.")
