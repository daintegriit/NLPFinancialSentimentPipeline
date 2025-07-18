from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import numpy as np
import pandas as pd
from typing import Optional
import traceback
import os
import json


router = APIRouter()

CSV_PATH = "outputs/results/merged_sentiment_price.csv"
TICKER_PATH = "config/tickers.json"

# 🔄 Normalize tickers like BRK-B -> BRK.B
def normalize_ticker(ticker: str) -> str:
    return ticker.upper().replace("-", ".")

# 📥 Load valid tickers from tickers.json
def load_valid_tickers() -> set:
    try:
        with open(TICKER_PATH, "r") as f:
            data = json.load(f)
        return set(entry["ticker"].upper() for entry in data)
    except Exception as e:
        print("❌ Error loading tickers.json:", e)
        return set()

valid_tickers = load_valid_tickers()

# 📊 Filter CSV by ticker
def load_csv(ticker: str) -> pd.DataFrame:
    ticker = normalize_ticker(ticker)
    
    if ticker not in valid_tickers:
        raise HTTPException(status_code=400, detail=f"Invalid ticker: {ticker}")
    
    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="Merged CSV not found")
    
    try:
        df = pd.read_csv(CSV_PATH)
        df = df[df["ticker"].str.contains(ticker, case=False, na=False, regex=False)]
        return df
    except Exception as e:
        print(f"❌ CSV loading or filtering failed: {e}")
        raise HTTPException(status_code=500, detail="Error loading CSV")


@router.get("/api/news-table")
def get_news_table(
    ticker: Optional[str] = Query(None),
    sector: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    marketCap: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    try:
        print(f"🧠 /news-table| Query received: ticker={ticker}, sector={sector}, region={region}, marketCap={marketCap}, type={type}, start={start}, end={end}")

        df = load_csv(ticker)
        print(f"📄 Loaded CSV with {len(df)} rows")

        # Filter out rows with missing title/link
        df = df[df["title"].notnull() & df["link"].notnull()]

        # Normalize inputs
        if ticker:
            ticker = normalize_ticker(ticker.upper())
            df = df[df["ticker"].str.upper() == ticker]
            print(f"🔍 Filtered by ticker = {ticker}: {len(df)} rows")

        if sector:
            df = df[df["sector"].astype(str).str.lower() == sector.lower()]
            print(f"🔍 Filtered by sector = {sector}: {len(df)} rows")

        if region:
            df = df[df["region"].astype(str).str.lower() == region.lower()]
            print(f"🔍 Filtered by region = {region}: {len(df)} rows")

        if marketCap:
            df = df[df["marketCap"].astype(str).str.lower() == marketCap.lower()]
            print(f"🔍 Filtered by marketCap = {marketCap}: {len(df)} rows")

        if type:
            df = df[df["type"].astype(str).str.lower() == type.lower()]
            print(f"🔍 Filtered by type = {type}: {len(df)} rows")

        # 🕒 Filter by date range
        if start or end:
            from datetime import datetime

            if start and end:
                # Use 'published' column — this is the correct datetime field
                df["published"] = pd.to_datetime(df["published"], errors="coerce")

                start_date = datetime.strptime(start, "%Y-%m-%d")
                end_date = datetime.strptime(end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

                df = df[(df["published"] >= start_date) & (df["published"] <= end_date)]
                print(f"🗓️ Filtered by published date: {start_date} to {end_date} ➜ {len(df)} rows")


        print(f"✅ Returning {len(df)} records")
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(axis=0, how='any', inplace=True)

        return JSONResponse(
            df.drop(columns=["parsed_date"], errors="ignore").to_dict(orient="records")
        )

    except Exception as e:
        import traceback
        print("❌ FULL EXCEPTION TRACE:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/api/extreme-scores")
def get_extreme_scores(
    ticker: str = Query(...),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None)
):
    try:
        print("🧠 Normalized ticker")
        ticker = normalize_ticker(ticker)

        if ticker not in valid_tickers:
            print("❌ Invalid ticker")
            raise HTTPException(status_code=400, detail=f"Invalid ticker: {ticker}")

        df = load_csv(ticker)
        print("✅ Loaded CSV:", df.columns.tolist())

        if "score_finbert" not in df.columns:
            print("❌ Missing 'score_finbert' in CSV ❌")
            raise HTTPException(status_code=500, detail="Missing sentiment score column")

        required_cols = ["title", "link", "ticker", "score_finbert", "score_roberta"]
        for col in required_cols:
            if col not in df.columns:
                raise HTTPException(status_code=500, detail=f"Missing required column: {col}")

        df = df[df["title"].notnull() & df["link"].notnull()]
        df = df[df["ticker"].str.contains(ticker, case=False, na=False, regex=False)]

        # 🗓️ Date filter (same logic as headlines)
        if start and end:
            df["published"] = pd.to_datetime(df["published"], errors="coerce")

            start_dt = datetime.strptime(start, "%Y-%m-%d")
            end_dt = datetime.strptime(end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

            df = df[(df["published"] >= start_dt) & (df["published"] <= end_dt)]
            print(f"🗓️ Filtered by published date: {start} to {end} ➜ {len(df)} rows")

        # 🔻 Filter by extreme sentiment scores
        filtered = df[
            (df["score_finbert"] >= 0.95) |
            (df["score_finbert"] <= 0.05) |
            (df["score_roberta"] >= 0.95) |
            (df["score_roberta"] <= 0.05)
        ]

        print("✅ Filtered shape:", filtered.shape)

        # 📦 Make JSON-safe
        filtered = filtered.replace({float("inf"): None, float("-inf"): None})
        filtered = filtered.dropna()

        return filtered.to_dict(orient="records")

    except Exception as e:
        print("❌ FULL EXCEPTION TRACE:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


