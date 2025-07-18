# validate/prune_dead_keywords.py

import os
import pandas as pd

KEYWORDS_FILE = "config/learned_keywords.txt"
NEWS_DIR = "data/raw_news"
PRUNE_THRESHOLD = 0  # Appear at least once to be kept

def load_keywords():
    with open(KEYWORDS_FILE, "r") as f:
        return [kw.strip().lower() for kw in f.readlines() if kw.strip()]

def save_keywords(keywords):
    with open(KEYWORDS_FILE, "w") as f:
        for kw in sorted(set(keywords)):
            f.write(f"{kw}\n")

def collect_all_headlines():
    all_titles = []
    for file in os.listdir(NEWS_DIR):
        if file.endswith("_news.csv"):
            df = pd.read_csv(os.path.join(NEWS_DIR, file))
            if "title" in df.columns:
                all_titles.extend(df["title"].dropna().astype(str).tolist())
    return " ".join(all_titles).lower()

def prune_keywords():
    print("🧹 Pruning unused learned keywords...")
    current_keywords = load_keywords()
    all_text = collect_all_headlines()

    surviving_keywords = [kw for kw in current_keywords if all_text.count(kw) > PRUNE_THRESHOLD]

    removed = set(current_keywords) - set(surviving_keywords)
    save_keywords(surviving_keywords)

    print(f"✅ Kept {len(surviving_keywords)} keywords")
    print(f"🗑️ Removed {len(removed)} unused keywords")
    if removed:
        print(f"❌ Pruned: {', '.join(sorted(removed))}")

if __name__ == "__main__":
    prune_keywords()
