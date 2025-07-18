# src/data_loader.py

import pandas as pd
import os

DATA_PATH = "outputs/results/merged_sentiment_price.csv"

def load_pipeline_data(ticker: str) -> list:
    """
    Load merged sentiment/price pipeline data from local CSV for a given ticker.
    Returns list of dicts ready for API response.
    """
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] CSV not found at {DATA_PATH}")
        return []

    try:
        df = pd.read_csv(DATA_PATH)
        df = df.dropna()
        df = df[df["ticker"] == ticker.upper()]
        df["date"] = pd.to_datetime(df["date"]).astype(str)  # ✅ Ensure it's stringified
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"[ERROR] Failed to load pipeline data: {e}")
        return []
