🛠️ Crypto ML Prediction System Template
這是一個基於 Flask + React 的加密貨幣預測系統模板，提供了使用 機器學習模型 進行加密貨幣價格走勢預測的基本架構。可以根據需求修改與擴充，並部署於 Render（後端）與 Vercel（前端）。

本模板包含後端 API、機器學習模型（XGBoost）、前端 React 應用與互動圖表，並支援 Telegram 推播功能。

🔮 功能介紹
⏱ 每 8 小時自動抓取 Binance 資料，並使用 ML 模型預測走勢
🧠 訓練 XGBoost 模型來預測市場走勢：上漲、下跌或盤整
📈 前端展示可切換交易對的 VWAP 與預測走勢圖表
🔔 支援 Telegram 推播預測結果
🌐 Flask 後端 API 與定時任務整合（部署於 Render）
🎨 React 前端應用與可視化圖表（部署於 Vercel）

🗂️ 專案結構
crypto-ml-app-template/
├── backend/                          # 後端 Python API 與 ML 核心模組
│   ├── ml_core.py                    # 特徵擷取、資料處理與模型訓練
│   ├── routes.py                     # Flask API 路由定義
│   ├── jobs/
│   │   └── schedule_runner.py        # 啟動 Flask 與排程任務（APScheduler）
│   └── __init__.py                   # backend 模組初始化（推薦加上）
│
├── main.py                           # 本地啟動 Flask app 用的主程式（選用）
├── requirements.txt                  # Python 套件需求清單
├── render.yaml                       # Render 部署用設定檔
├── .gitignore                        # Git 忽略規則
│
└── frontend/                         # 前端 React + TypeScript 應用（建議部署至 Vercel）
    ├── public/
    │   └── index.html                # 前端 HTML 入口（Vite 使用）
    │
    ├── src/
    │   ├── components/
    │   │   ├── Chart.tsx            # 顯示預測結果與 VWAP 線圖
    │   │   └── SelectSymbol.tsx     # 選擇交易對的下拉選單元件
    │   │
    │   ├── pages/
    │   │   └── index.tsx            # 首頁：組合顯示圖表與選擇器
    │   │
    │   ├── services/
    │   │   └── api.ts               # 封裝 axios，提供與後端的 API 對接方法
    │   │
    │   ├── App.tsx                  # App 主要組件
    │   └── index.tsx                # React 應用入口（渲染到 DOM）
    │
    ├── index.css                    # 基本樣式表（若已使用）
    ├── package.json                 # 前端相依套件與腳本定義
    ├── tsconfig.json                # TypeScript 編譯器設定
    └── vite.config.ts              # Vite 前端建構工具設定

🚀 快速啟動
🔧 安裝後端依賴並啟動
-進入後端資料夾並安裝依賴：
cd backend
pip install -r ../requirements.txt
-啟動 Flask API：
python ../main.py
-開啟瀏覽器，訪問： http://localhost:5000

🧪 本地測試定時任務
若需要測試定時任務，可以執行 schedule_runner.py：
python backend/jobs/schedule_runner.py


🌐 部署指南
🛰️ Render（Flask 後端）
-登入 Render
-新增 Web Service 並連結 GitHub 專案

設定：
Root Directory：backend/
Start Command：python ../main.py
Environment：選擇 Python 3.10+

環境變數：
TELEGRAM_TOKEN=你的_bot_token
TELEGRAM_CHAT_ID=你的_chat_id

新增 Background Worker 執行定時任務：
Command：python backend/jobs/schedule_runner.py

🎨 Vercel（React 前端）
登入 Vercel
匯入此 GitHub 專案

設定：
Root Directory：frontend/
Build Command：npm run build
Output Directory：dist

在 .env 檔案中加入後端 API 基本 URL：
env
VITE_API_BASE_URL=https://your-render-url.onrender.com
點選「Deploy」完成部署。

🔌 API 路由說明
Endpoint	Method	描述
/api/symbols	GET	回傳支援的交易對列表
/api/latest	GET	回傳各交易對最新預測結果
/api/chart?symbol=	GET	回傳特定交易對的歷史資料圖表

🧠 特徵說明與預測
本模型使用以下特徵進行預測：
X1_volume_diff：成交量變化
X2_OI_diff：持倉量變化
X3_funding_rate_diff：資金費率變化
X4_vwap_diff：VWAP 價差

📦 模型與資料儲存
xgb_model.pkl：訓練好的 XGBoost 模型
scaler.pkl：StandardScaler + LabelEncoder
data/market_features.csv：包含所有預測歷史紀錄

🔔 Telegram 推播格式
當預測結果發送至 Telegram 時，格式如下：
📈 預測結果 (2025-05-13 08:00 UTC)
BTC/USDT: 上漲
ETH/USDT: 下跌
...

🧭 未來優化建議
支援更多技術指標（如 MACD, RSI, Bollinger Bands）
引入短期與長期模型融合（如日線與短線預測）
使用深度學習方法（如 LSTM、Transformer）
增加使用者登入與儀表板自訂功能

📬 聯絡方式
如有建議或問題，請提交 Issue 或聯絡作者。

🪪 授權條款
本專案採用 MIT License。