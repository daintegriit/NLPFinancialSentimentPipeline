# src/tweet_scraper.py

import snscrape.modules.twitter as sntwitter
import pandas as pd
from datetime import datetime

def scrape_tweets(query, max_tweets=100, since="2023-01-01"):
    tweets = []
    print(f"🔎 Searching Twitter for: {query}")
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:{since}').get_items()):
        tweets.append({
            "date": tweet.date,
            "username": tweet.user.username,
            "content": tweet.content,
            "url": tweet.url
        })
        if i + 1 >= max_tweets:
            break
    df = pd.DataFrame(tweets)
    print(f"✅ Scraped {len(df)} tweets")
    return df

if __name__ == "__main__":
    # Example test
    df = scrape_tweets("AAPL OR Apple stock", max_tweets=20, since="2023-10-01")
    print(df.head())
    df.to_csv("data/raw_tweets/sample_aapl_tweets.csv", index=False)
