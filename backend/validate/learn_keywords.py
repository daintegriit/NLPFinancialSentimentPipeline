# backend/validate/learn_keywords.py

import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

REVIEW_DIR = "data/manual_review"
OUTPUT_FILE = "config/learned_keywords.txt"
MAX_FEATURES = 100
STOP_WORDS = "english"

def extract_keywords():
    keyword_set = set()
    all_titles = []

    for file in os.listdir(REVIEW_DIR):
        if file.endswith("_flagged_relevant.csv"):
            df = pd.read_csv(os.path.join(REVIEW_DIR, file))
            titles = df["title"].dropna().astype(str).tolist()
            all_titles.extend(titles)

    if not all_titles:
        print("🚫 No flagged titles found to learn from.")
        return

    vectorizer = CountVectorizer(stop_words=STOP_WORDS, max_features=MAX_FEATURES)
    X = vectorizer.fit_transform(all_titles)
    keywords = vectorizer.get_feature_names_out()

    keyword_set.update(keywords)

    # Save learned keywords
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        for kw in sorted(keyword_set):
            f.write(f"{kw}\n")

    print(f"✅ Learned {len(keyword_set)} keywords from flagged headlines.")
    print(f"📁 Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_keywords()
