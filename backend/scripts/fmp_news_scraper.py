import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
FMP_API_KEY = os.getenv("FMP_API_KEY")

# Load tickers from JSON file
with open("config/tickers.json", "r") as f:
    tickers_json = json.load(f)
TICKERS = [entry["ticker"] for entry in tickers_json]

NEWS_LIMIT = 10  # Number of news items per stock
OUTPUT_DIR = "data/fmp_news"

# === Ensure output directory exists ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_news(ticker):
    url = "https://financialmodelingprep.com/api/v4/general_news"
    params = {
        "tickers": ticker,
        "limit": NEWS_LIMIT,
        "apikey": FMP_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_items = response.json()

        if not news_items:
            print(f"⚠️ No news returned for {ticker}")
            return pd.DataFrame()

        df = pd.DataFrame(news_items)
        df["ticker"] = ticker
        return df

    except Exception as e:
        print(f"❌ Error fetching news for {ticker}: {e}")
        return pd.DataFrame()

def clean_and_save(df, ticker):
    if df.empty:
        return

    # === Clean and normalize ===
    df = df[["title", "publishedDate", "ticker"]].rename(columns={
        "title": "headline",
        "publishedDate": "date"
    })
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df = df.dropna()

    # === Deduplication key ===
    df["__hash__"] = df.apply(lambda x: hash((x["date"], x["headline"])), axis=1)

    output_path = os.path.join(OUTPUT_DIR, f"{ticker}_news.csv")

    if os.path.exists(output_path):
        existing_df = pd.read_csv(output_path)
        if not existing_df.empty:
            existing_df["__hash__"] = existing_df.apply(lambda x: hash((x["date"], x["headline"])), axis=1)
            df = pd.concat([existing_df, df], ignore_index=True)
            df = df.drop_duplicates(subset="__hash__")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.drop(columns=["__hash__"])
    df = df.sort_values("date")

    # === Save ===
    df.to_csv(output_path, index=False)
    print(f"✅ Saved ({len(df)}) total articles for {ticker} ➜ {output_path}")


# === MAIN SCRAPER LOOP ===
if __name__ == "__main__":
    for ticker in TICKERS:
        df = fetch_news(ticker)
        clean_and_save(df, ticker)
