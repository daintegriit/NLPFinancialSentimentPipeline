import os
import pandas as pd
from datetime import datetime
from sentiment_analysis import analyze_all_models
import hashlib

# === Directories ===
INPUT_DIR = "data/skipped_validated"
OUTPUT_DIR = "outputs/results/sentiment"
LOG_FILE = "logs/rescue_log.csv"
os.makedirs("logs", exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Create hash for deduplication
def make_hash(row):
    return hashlib.md5(f"{row.get('date','')}_{row.get('title','')}".lower().encode("utf-8")).hexdigest()

# === Load + update rescue log
def log_rescue(symbol, row):
    log_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "title": row.get("title", ""),
        "date": row.get("date", ""),
        "source": row.get("source", "skipped_validated"),
        "rescued_by": "auto_rescue.py"
    }
    pd.DataFrame([log_row]).to_csv(LOG_FILE, mode="a", header=not os.path.exists(LOG_FILE), index=False)

# === Main logic ===
def run_auto_rescue():
    print("🚨 Running auto-rescue on validated skipped headlines...")

    for filename in os.listdir(INPUT_DIR):
        if not filename.endswith("_skipped.csv"):
            continue

        symbol = filename.split("_")[0].upper()
        file_path = os.path.join(INPUT_DIR, filename)
        try:
            df = pd.read_csv(file_path)
            if "is_validated" not in df.columns or df["is_validated"].sum() == 0:
                continue

            df = df[df["is_validated"] == True].copy()
            df["title"] = df["title"].astype(str).str.strip()
            df = df[df["title"] != ""]
            if df.empty:
                continue

            # Run sentiment models
            model_outputs = df["title"].apply(analyze_all_models).apply(pd.Series)
            df = pd.concat([df.reset_index(drop=True), model_outputs.reset_index(drop=True)], axis=1)

            df["rescued"] = True
            df["__hash"] = df.apply(make_hash, axis=1)

            # Load existing output
            output_path = os.path.join(OUTPUT_DIR, f"{symbol}_sentiment.csv")
            if os.path.exists(output_path):
                existing_df = pd.read_csv(output_path)
                existing_df["__hash"] = existing_df.apply(make_hash, axis=1)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df = combined_df.drop_duplicates(subset="__hash").drop(columns="__hash")
            else:
                combined_df = df.drop(columns="__hash")

            # Save final result
            combined_df.to_csv(output_path, index=False)
            print(f"✅ Rescued {len(df)} headlines ➜ {output_path}")

            # Log each rescue
            for _, row in df.iterrows():
                log_rescue(symbol, row)

        except Exception as e:
            print(f"❌ Failed processing {filename}: {e}")

if __name__ == "__main__":
    run_auto_rescue()
