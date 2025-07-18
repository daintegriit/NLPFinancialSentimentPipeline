from fastapi import APIRouter, Query
from typing import Optional, List
from datetime import datetime
from data_loader import load_pipeline_data  # ✅ Must return list of dicts (see below)

router = APIRouter()

@router.get("/api/pipeline-output")
def get_pipeline_output(
    ticker: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    sort_by: Optional[str] = "date",  # e.g. sentiment, confidence
    order: Optional[str] = "desc"
):
    """
    Filtered pipeline data for a given ticker, with pagination and sorting.
    """

    # 📦 Load data from CSV or cache
    data = load_pipeline_data(ticker)  # Must return list[dict]

    # 🕒 Optional date filtering
    if date_from:
        data = [row for row in data if row.get("date") and row["date"] >= date_from]
    if date_to:
        data = [row for row in data if row.get("date") and row["date"] <= date_to]

    # 🔃 Optional sorting
    reverse = order.lower() == "desc"
    if sort_by in data[0]:
        data = sorted(data, key=lambda x: x.get(sort_by, ""), reverse=reverse)

    # 📊 Pagination
    paginated = data[offset:offset + limit]

    return {
        "ticker": ticker,
        "total": len(data),
        "returned": len(paginated),
        "data": paginated
    }
