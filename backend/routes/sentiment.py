from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import pandas as pd
import json
import os

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
def load_csv_filtered_by_ticker(ticker: str):
    ticker = normalize_ticker(ticker)

    if ticker not in valid_tickers:
        raise HTTPException(status_code=400, detail=f"Invalid ticker: {ticker}")

    if not os.path.exists(CSV_PATH):
        raise HTTPException(status_code=404, detail="Merged CSV not found")

    try:
        print(f"📥 Loading merged CSV from {CSV_PATH}")
        df = pd.read_csv(CSV_PATH)
        print("📄 Columns in CSV:", df.columns.tolist())

        df = df[df["ticker"].str.contains(ticker, case=False, na=False, regex=False)]
        print(f"🔍 Filtered rows for {ticker}: {len(df)}")

        if df.empty:
            print(f"⚠️ No rows found for ticker: {ticker}")

        return df

    except Exception as e:
        print(f"❌ CSV loading or filtering failed: {e}")
        raise HTTPException(status_code=500, detail="Error loading CSV")

# 🚀 Test route for debug
@router.get("/api/sentiment")
def get_sentiment(
    ticker: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    try:
        df = pd.read_csv(CSV_PATH)

        # Clean strings
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df = df.dropna(subset=["title", "published"])

        # ✅ Ticker filter
        if ticker:
            df = df[df["ticker"].str.upper() == ticker.upper()]

        # ✅ Date filter (use datetime for filtering)
        if "published" in df.columns:
            df["published"] = pd.to_datetime(df["published"], errors="coerce")

            today_str = datetime.now().strftime("%Y-%m-%d")
            if not start:
                start = today_str
            if not end:
                end = today_str

            start_d = datetime.strptime(start, "%Y-%m-%d")
            end_d = datetime.strptime(end, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

            df = df[(df["published"] >= start_d) & (df["published"] <= end_d)]

        # ✅ Convert datetime columns to string **after filtering**
        for col in ["published", "date"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        return JSONResponse(content=df.to_dict(orient="records"))

    except Exception as e:
        print("❌ Sentiment route error:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})



# 📈 Aggregated sentiment over time
@router.get("/api/sentiment-over-time")
def get_sentiment_over_time(ticker: str = Query(...)):
    try:
        ticker = normalize_ticker(ticker)

        df = load_csv_filtered_by_ticker(ticker)
        print("🐞 DEBUG ➜ Columns in df:", df.columns.tolist())

        df.columns = df.columns.str.lower()
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        df = df.dropna(subset=["date", "score_finbert", "score_roberta", "close"])

        df_grouped = df.sort_values("date").groupby("date").agg({
            "score_finbert": "mean",
            "score_roberta": "mean",
            "close": "last",  # 🟢 Most recent close price of the day
        }).reset_index()

        df_grouped["date"] = df_grouped["date"].dt.strftime("%Y-%m-%d")
        df_grouped["score_finbert"] = df_grouped["score_finbert"].round(4)
        df_grouped["score_roberta"] = df_grouped["score_roberta"].round(4)
        df_grouped["close"] = df_grouped["close"].round(2)
        df_grouped.rename(columns={"close": "price"}, inplace=True)

        df_grouped["ticker"] = ticker  # Optional but useful

        return df_grouped.to_dict(orient="records")

    except Exception as e:
        print("❌ Sentiment Over Time Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# 🔍 Model comparison endpoint
@router.get("/api/model-comparison")
def model_comparison(ticker: str = Query(...)):
    try:
        ticker = normalize_ticker(ticker)

        df = load_csv_filtered_by_ticker(ticker)
        df = df.dropna(subset=["score_finbert", "score_roberta", "date"])
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        data = df[["date", "score_finbert", "score_roberta"]].copy()
        data["score_finbert"] = data["score_finbert"].round(4)
        data["score_roberta"] = data["score_roberta"].round(4)
        data["ticker"] = ticker  # optional, but helpful for frontend

        return data.to_dict(orient="records")

    except Exception as e:
        print("❌ Model comparison error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/debug")
def debug_route():
    try:
        print("🛠️ Entering debug route")

        with open("config/tickers.json", "r") as f:
            data = json.load(f)
            print("📄 Ticker file loaded")

        df = pd.read_csv("outputs/results/merged_sentiment_price.csv")
        print("✅ CSV file loaded")
        print("📊 Columns:", df.columns.tolist())
        print("🧪 Sample rows:", df.head(3).to_dict())
        print("📏 Row count:", len(df))

        expected = {"title", "ticker", "score_finbert", "score_roberta", "link"}
        missing = expected - set(df.columns)
        if missing:
            raise HTTPException(status_code=500, detail=f"Missing expected columns: {missing}")

        return {
            "status": "✅ all clear",
            "rows": len(df),
            "columns": df.columns.tolist()
        }

    except Exception as e:
        print("❌ Debug error:", e)
        raise HTTPException(status_code=500, detail=str(e))
