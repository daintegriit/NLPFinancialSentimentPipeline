# validate/apply_manual_flags.py

import pandas as pd
import os

def deduplicate(df):
    return df.drop_duplicates(subset=["title", "link", "date"])

def apply_flags():
    review_dir = "data/manual_review"
    news_dir = "data/raw_news"

    flagged_files = [f for f in os.listdir(review_dir) if f.endswith("_flagged_relevant.csv")]

    for file in flagged_files:
        symbol = file.split("_")[0]
        flagged_path = os.path.join(review_dir, file)
        news_path = os.path.join(news_dir, f"{symbol}_news.csv")
        skipped_path = os.path.join(news_dir, f"{symbol}_skipped.csv")

        flagged_df = pd.read_csv(flagged_path)
        news_df = pd.read_csv(news_path) if os.path.exists(news_path) else pd.DataFrame(columns=flagged_df.columns)

        # Append flagged rows
        updated_news = pd.concat([news_df, flagged_df], ignore_index=True)
        updated_news = deduplicate(updated_news)
        updated_news.to_csv(news_path, index=False)

        print(f"✅ Patched {symbol}_news.csv with {len(flagged_df)} flagged entries")

        # Optional: remove from skipped file
        if os.path.exists(skipped_path):
            skipped_df = pd.read_csv(skipped_path)
            cleaned_skipped = skipped_df[~skipped_df["title"].isin(flagged_df["title"])]
            cleaned_skipped.to_csv(skipped_path, index=False)
            print(f"🧹 Removed flagged rows from {symbol}_skipped.csv")

if __name__ == "__main__":
    apply_flags()
