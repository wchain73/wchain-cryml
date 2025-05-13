import os
import pandas as pd
from datetime import datetime, timezone
from backend.ml_core import fetch_all_features, train_model
from backend.routes import predict_and_notify  # async 方法
import asyncio


def run_job():
    print(f"[{datetime.now()}] Running scheduled job...")
    df = fetch_all_features()

    os.makedirs("data", exist_ok=True)
    csv_path = "data/market_features.csv"
    df.to_csv(csv_path, mode='a', index=False, header=not os.path.exists(csv_path))

    if datetime.now(timezone.utc).hour == 0:
        try:
            df_all = pd.read_csv(csv_path)
            train_model(df_all)
        except Exception as e:
            print("Training failed:", e)

    asyncio.run(predict_and_notify(df))


if __name__ == "__main__":
    run_job()
