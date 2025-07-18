# routes/tickers.py

from fastapi import APIRouter
from fastapi.responses import JSONResponse
import json
import os

router = APIRouter()

TICKER_PATH = "config/tickers.json"

@router.get("/api/tickers")
def get_tickers():
    try:
        if not os.path.exists(TICKER_PATH):
            return JSONResponse(status_code=404, content={"error": "Tickers JSON not found"})

        with open(TICKER_PATH, "r") as f:
            data = json.load(f)

        # Return only safe subset
        safe = [
            {
                "ticker": x.get("ticker"),
                "query": x.get("query"),
                "sector": x.get("sector"),
                "type": x.get("type")
            }
            for x in data
            if x.get("ticker") and x.get("query")
        ]

        return JSONResponse(content={"tickers": safe})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.get("/api/tickers/full")
def get_full_tickers():
    try:
        if not os.path.exists(TICKER_PATH):
            return JSONResponse(status_code=404, content={"error": "Tickers JSON not found"})

        with open(TICKER_PATH, "r") as f:
            data = json.load(f)

        return JSONResponse(content={"tickers": data})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
