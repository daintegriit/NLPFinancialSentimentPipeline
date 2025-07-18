from transformers import pipeline
from tqdm import tqdm
import pandas as pd
import os
import json

# === Load Tickers from JSON ===
with open("config/tickers.json") as f:
    tickers_json = json.load(f)
ACTIVE_TICKERS = set(entry["ticker"].upper() for entry in tickers_json)

# === Define Multiple Sentiment Models ===
print("⏳ Loading FinBERT...")
finbert_model = pipeline("sentiment-analysis", model="yiyanghkust/finbert-tone")

print("⏳ Loading RoBERTa...")
roberta_model = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
    # Add more as needed (e.g., "deberta": ..., "llama": ...)


MODEL_PIPELINES = {
    "finbert": finbert_model,
    "roberta": roberta_model,
}
print("✅ All models loaded.")

def analyze_all_models(text, verbose=False):
    text = text[:512]  # Truncate
    results = {}
    for model_name, pipe in MODEL_PIPELINES.items():
        try:
            result = pipe(text)[0]
            label = result["label"]
            score = result["score"]
            results[f"label_{model_name}"] = label
            results[f"score_{model_name}"] = score
            if verbose:
                tqdm.write(f"  ✅ {model_name} ➜ {label.upper()} ({score * 100:.1f}%)")
        except Exception as e:
            results[f"label_{model_name}"] = "ERROR"
            results[f"score_{model_name}"] = 0.0
            if verbose:
                tqdm.write(f"  ❌ {model_name} failed ➜ {e}")
    return results



def run_sentiment_analysis():
    import hashlib

    input_dirs = ["data/raw_news", "data/fmp_news"]
    output_dir = "outputs/results/sentiment"
    os.makedirs(output_dir, exist_ok=True)

    # Tracks all results per ticker
    from collections import defaultdict
    combined_by_symbol = defaultdict(list)

    for input_dir in input_dirs:
        for filename in tqdm(os.listdir(input_dir), desc=f"🔄 {input_dir}"):
            if not filename.endswith(".csv"):
                continue
            if "_skipped" in filename:
                continue

            symbol = filename.split("_")[0].upper()
            if symbol not in ACTIVE_TICKERS:
                print(f"⚠️ Skipping {filename}: '{symbol}' not in ACTIVE_TICKERS")
                continue

            input_path = os.path.join(input_dir, filename)

            try:
                df = pd.read_csv(input_path, parse_dates=["date"], encoding="utf-8")
                df.columns = [col.strip().lower() for col in df.columns]
                if "title" not in df.columns or df.empty:
                    print(f"⚠️ Skipping {filename}; no 'title' column or empty.")
                    continue

                # Run sentiment models
                df = df[df["title"].notnull()]
                model_results = df["title"].apply(analyze_all_models).apply(pd.Series)
                df = pd.concat([df.reset_index(drop=True), model_results.reset_index(drop=True)], axis=1)

                combined_by_symbol[symbol].append(df)
                tqdm.write(f"✅ {symbol}: Processed {len(df)} rows from {filename}")


            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    print("🔁 Merging, deduping, and saving final per-symbol sentiment files...")

    for symbol, dfs in combined_by_symbol.items():
        merged_df = pd.concat(dfs, ignore_index=True)

        # Create hash for deduplication
        def make_hash(row):
            return hashlib.md5(f"{row.get('date','')}_{row.get('title','')}".lower().encode("utf-8")).hexdigest()

        merged_df["__hash"] = merged_df.apply(make_hash, axis=1)
        deduped_df = merged_df.drop_duplicates(subset="__hash").drop(columns="__hash")

        if "date" in deduped_df.columns:
            deduped_df["date"] = pd.to_datetime(deduped_df["date"], errors="coerce")
            deduped_df = deduped_df.sort_values("date", ascending=False)

        output_path = os.path.join(output_dir, f"{symbol}_sentiment.csv")
        deduped_df.to_csv(output_path, index=False)

        print(f"✅ {symbol}: {len(dfs)} source files ➜ {len(deduped_df)} unique rows ➜ {output_path}")



if __name__ == "__main__":
    run_sentiment_analysis()
