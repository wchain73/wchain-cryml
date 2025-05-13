
# 🤖 Crypto ML Prediction System

本專案是一套以 Flask + React 打造的加密貨幣走勢預測系統，透過機器學習模型（XGBoost）結合 Binance Futures 的 8 小時資料，預測幣價短期內走勢為上漲、下跌或盤整，並可視覺化結果、定時推送到 Telegram。

---

## 🔮 功能介紹

- ⏱ 每 8 小時自動拉取 Binance 資料，並使用 ML 模型預測趨勢
- 🧠 使用 XGBoost 訓練分類模型
- 📈 前端可切換交易對，查看 VWAP 與預測歷史圖表
- 🔔 Telegram 自動推播預測結果
- 🌐 Flask + Schedule 任務整合後端（Render）
- 🎨 React + Chart.js/Victory 前端視覺化（Vercel）

---

## 🗂️ 專案結構

```
crypto-ml-app/
├── backend/
│   ├── ml_core.py                # 特徵擷取與模型訓練
│   ├── routes.py                 # API 定義
│   ├── jobs/
│   │   └── schedule_runner.py    # Flask 與定時任務整合
│   └── ...
├── main.py                       # 啟動 Flask 應用程式
├── requirements.txt
├── render.yaml                   # Render 部署設定
├── .gitignore
└── frontend/                     # 前端專案（Vercel 部署）
    ├── public/
    ├── src/
    │   ├── components/
    │   │   ├── Chart.tsx         # 顯示預測與 VWAP 的圖表
    │   │   └── SelectSymbol.tsx  # 下拉選單選交易對
    │   ├── pages/
    │   │   └── index.tsx
    │   ├── services/
    │   │   └── api.ts            # API 請求模組
    │   ├── App.tsx
    │   └── index.tsx
    ├── package.json
    └── tsconfig.json
```

---

## 🚀 快速啟動

### 🔧 安裝後端（Flask）

```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

開啟瀏覽器，前往 [http://localhost:5000](http://localhost:5000)

---

### 🧪 本地測試定時任務

```bash
python backend/jobs/schedule_runner.py
```

---

## 🌐 部署教學

### 📡 Render（後端）

1. 登入 [Render](https://render.com/)
2. 建立新 Web Service，連結此 GitHub 專案
3. 設定：
   - **Root Directory**：`backend/`
   - **Start Command**：`python ../main.py`
   - **Environment**：Python 3.10+
   - 加入環境變數：
     ```
     TELEGRAM_TOKEN=你的_bot_token
     TELEGRAM_CHAT_ID=你的_chat_id
     ```
4. 如需定時任務，新增一個 **Background Worker**
   - Command: `python backend/jobs/schedule_runner.py`

---

### 🎨 Vercel（前端）

1. 登入 [Vercel](https://vercel.com/)
2. 連接此 GitHub 專案
3. 設定：
   - Root directory：`frontend/`
   - Build Command：`npm run build`
   - Output：`build`
4. 在 `.env` 中加入後端網址：
   ```env
   VITE_API_BASE_URL=https://your-render-url.onrender.com
   ```
5. 點選「Deploy」

---

## 🔗 API 文件

| Endpoint               | Method | 說明                     |
|------------------------|--------|--------------------------|
| `/symbols`            | GET    | 回傳支援的交易對列表     |
| `/latest`             | GET    | 回傳各交易對最新預測結果 |
| `/historical/:symbol` | GET    | 回傳特定交易對的歷史資料 |

---

## 📊 特徵與預測內容

- `X1_volume_diff`: 成交量差異
- `X2_OI_diff`: Open Interest 差異
- `X3_funding_rate_diff`: 資金費率變化
- `X4_vwap_diff`: VWAP 價差

---

## 📦 模型儲存

- `xgb_model.pkl`: 訓練好的 XGBoost 模型
- `scaler.pkl`: StandardScaler + LabelEncoder
- `data/market_features.csv`: 所有預測紀錄

---

## 🤖 Telegram 通知格式

```
📈 預測結果 (2025-05-13 08:00 UTC)
BTC/USDT: 上漲
ETH/USDT: 下跌
...
```

---

## 🧠 未來功能建議

- 加入更多技術指標（MACD、RSI、Bollinger）
- 長短期模型融合（短線+日線）
- 使用 LSTM/BERT 等深度學習方法
- 用戶介面登入與訂閱功能

---

## 📬 聯絡方式

如有問題請提 Issue 或聯絡作者。

---

## 🪪 License

MIT License
