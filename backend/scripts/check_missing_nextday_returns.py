# scripts/check_missing_nextday_returns.py

import os
import pandas as pd

MERGED_DIR = "outputs/results/merged"
COLUMNS_TO_CHECK = ["nextdayclose", "nextdayreturn"]

def check_missing_returns():
    missing_report = []

    for fname in os.listdir(MERGED_DIR):
        if not fname.endswith(".csv"):
            continue

        fpath = os.path.join(MERGED_DIR, fname)
        df = pd.read_csv(fpath)

        # Check if required columns exist
        if not all(col in df.columns for col in COLUMNS_TO_CHECK):
            print(f"❌ {fname} is missing columns: {COLUMNS_TO_CHECK}")
            continue

        missing_rows = df[df["nextdayclose"].isna() | df["nextdayreturn"].isna()]
        if not missing_rows.empty:
            missing_report.append((fname, len(missing_rows)))
            print(f"⚠️ {fname}: {len(missing_rows)} rows missing nextday return data")

    if not missing_report:
        print("✅ All files have complete nextdayclose and nextdayreturn columns.")
    else:
        print("\n🔎 Summary of Files with Missing Data:")
        for fname, count in missing_report:
            print(f" - {fname}: {count} rows missing")

if __name__ == "__main__":
    check_missing_returns()
