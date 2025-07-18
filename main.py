from backend.scripts.news_scraper import scrape_google_news
from backend.scripts.sentiment_analysis import analyze_sentiment
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

if __name__ == "__main__":
    print("📰 Scraping news...")
    news_df = scrape_google_news("AAPL stock", max_entries=25)

    print("🧠 Analyzing sentiment...")
    news_df["sentiment"], news_df["score"] = zip(*news_df["title"].map(analyze_sentiment))

    # Ensure output folders exist
    os.makedirs("outputs/results", exist_ok=True)
    os.makedirs("outputs/visualizations", exist_ok=True)

    # Save sentiment-scored CSV
    news_df.to_csv("outputs/results/aapl_pipeline_output.csv", index=False)
    print("✅ Pipeline complete! Output saved to: outputs/results/aapl_pipeline_output.csv")
    print(news_df.head())

    # Create sentiment histogram plot
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 4))
    sns.histplot(data=news_df, x="score", hue="sentiment", bins=10, kde=True)

    plt.title("FinBERT Sentiment Score Distribution")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Number of Headlines")
    plt.tight_layout()

    plt.savefig("outputs/visualizations/sentiment_distribution.png")
    plt.show()

from backend.sentiment_analysis2 import merge_sentiment_with_prices
merge_sentiment_with_prices("AAPL")