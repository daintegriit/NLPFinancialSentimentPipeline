# validate/unify_sentiment_price_csvs.py
import os
import glob
import pandas as pd

INPUT_DIR = "outputs/results/merged"
OUTPUT_PATH = "outputs/results/merged_sentiment_price.csv"

def unify_csvs():
    files = glob.glob(os.path.join(INPUT_DIR, "merged_*.csv"))
    all_dfs = []

    for file in files:
        ticker = os.path.basename(file).replace("merged_", "").replace(".csv", "")
        try:
            df = pd.read_csv(file)
            df["ticker"] = ticker
            all_dfs.append(df)
        except Exception as e:
            print(f"⚠️ Error processing {ticker}: {e}")

    if all_dfs:
        unified_df = pd.concat(all_dfs, ignore_index=True)
        unified_df.to_csv(OUTPUT_PATH, index=False)
        print(f"✅ Unified CSV saved to {OUTPUT_PATH} ({len(unified_df)} rows)")
    else:
        print("❌ No CSVs found or failed to load.")

if __name__ == "__main__":
    unify_csvs()
