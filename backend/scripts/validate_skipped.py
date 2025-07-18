import os
import pandas as pd
import json

# === Load tickers and queries ===
with open("config/tickers.json") as f:
    tickers_json = json.load(f)

tickers = [entry["ticker"].lower() for entry in tickers_json]

# === Smart keyword rules ===
validation_keywords = [
    "stock", "share", "ipo", "company", "acquisition", "earnings", "forecast",
    "results", "trading", "dividend", "price", "merger", "buyback", "equity",
    "capital", "ceo", "profit", "loss", "revenue", "cloud", "ai", "aws",
    "summit", "product", "launch", "report", "announcement"
]

# === Validation logic ===
def is_valid_headline(title):
    title_lower = str(title).lower()
    if any(kw in title_lower for kw in validation_keywords):
        return True
    if any(sym.lower() in title_lower for sym in tickers):
        return True
    return False

# === Process skipped CSVs ===
input_dir = "data/skipped_raw_news"
output_dir = "data/skipped_validated"
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if not filename.endswith("_skipped.csv"):
        continue

    input_path = os.path.join(input_dir, filename)
    df = pd.read_csv(input_path)

    if "title" not in df.columns:
        print(f"⚠️ Skipped: No title column in {filename}")
        continue

    # Apply smart validation
    df["is_validated"] = df["title"].apply(is_valid_headline)

    # Save validated output
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False)
    num_validated = df["is_validated"].sum()
    print(f"✅ Validated {num_validated}/{len(df)} headlines in {filename} ➜ {output_path}")
