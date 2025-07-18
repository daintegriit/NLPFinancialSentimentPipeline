# backend/news_scraper.py
import pandas as pd
import os
import json
import feedparser
from datetime import datetime
from urllib.parse import quote_plus  # ✅ NEW

# === Output folder setup ===
os.makedirs("data/raw_news", exist_ok=True)
os.makedirs("data/skipped_raw_news", exist_ok=True)

# === Load Tickers and queries from JSON ===
with open("config/tickers.json") as f:
    tickers_json = json.load(f)

tickers = {entry["ticker"].upper(): entry["query"] for entry in tickers_json}

# === Scraper function ===
def scrape_google_news(query, max_entries=100):
    safe_query = quote_plus(query)  # ✅ Properly encode query string
    url = f"https://news.google.com/rss/search?q=({safe_query})+stock+OR+earnings+OR+market+OR+company+OR+finance+OR+shares&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    relevant_data = []
    skipped_data = []

    for entry in feed.entries[:max_entries]:
        title_lower = entry.title.lower()
        published_raw = entry.get("published", "")
        published_dt = pd.to_datetime(published_raw, errors="coerce", utc=True)

        row = {
            "title": entry.title,
            "link": entry.link,
            "published": published_raw,
            "date": published_dt.strftime("%Y-%m-%d %H:%M:%S") if pd.notnull(published_dt) else None,
            "source": "Google"
        }

        # === Classify based on relevance ===
        keywords = [
            "stock", "share", "company", "automotive", "motors", "market",
            "ipo", "acquisition", "earnings", "forecast", "results", "trading",
            "dividend", "price", "merger", "bond", "buyback", "equity", "capital",
            "profit", "loss", "revenue", "cloud", "ai", "data", "aws", "summit",
            "product", "launch", "airbnb"
        ]

        # First: keyword match
        if any(kw in title_lower for kw in keywords):
            relevant_data.append(row)
        # Rescue: if symbol like 'AMZN' or 'AAPL' is mentioned in title
        elif any(sym.lower() in title_lower for sym in tickers.keys()):
            print(f"🛟 Rescued headline for symbol match ➜ {entry.title}")
            relevant_data.append(row)
        # (Optional) Rescue: query string (e.g. "McDonald's") in title
        elif query.lower() in title_lower:
            print(f"🔄 Rescued by full name match ➜ {entry.title}")
            relevant_data.append(row)
        else:
            skipped_data.append(row)

    return pd.DataFrame(relevant_data), pd.DataFrame(skipped_data)

# === Main loop ===
if __name__ == "__main__":
    for symbol, query in tickers.items():
        df_relevant, df_skipped = scrape_google_news(query)

        # Save relevant
        relevant_path = f"data/raw_news/{symbol}_news.csv"
        df_relevant.to_csv(relevant_path, index=False)
        print(f"✅ Saved {len(df_relevant)} relevant headlines to {relevant_path}")

        # Save skipped
        skipped_path = f"data/skipped_raw_news/{symbol}_skipped.csv"
        df_skipped.to_csv(skipped_path, index=False)
        print(f"⚠️  Saved {len(df_skipped)} skipped (irrelevant) headlines to {skipped_path}")