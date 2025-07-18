# backfill_tweets.py
import os
import pandas as pd
from datetime import datetime, timedelta
import subprocess

# Config
TICKER = 'AAPL'
START_DATE = '2025-05-05'
END_DATE = datetime.today().strftime('%Y-%m-%d')
OUTPUT_DIR = 'data/raw_news'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop over date range
start = pd.to_datetime(START_DATE)
end = pd.to_datetime(END_DATE)
delta = timedelta(days=1)

while start <= end:
    date_str = start.strftime('%Y-%m-%d')
    filename = f'{OUTPUT_DIR}/{TICKER}_{date_str}.csv'
    if os.path.exists(filename):
        print(f"✅ Already scraped {filename}")
        start += delta
        continue

    query = f'{TICKER} since:{date_str} until:{(start + delta).strftime("%Y-%m-%d")}'
    print(f"🔍 Scraping: {query}")
    command = f'snscrape --jsonl --max-results 100 twitter-search "{query}" > tmp.json'
    subprocess.run(command, shell=True)

    if os.path.exists('tmp.json'):
        df = pd.read_json('tmp.json', lines=True)
        df.to_csv(filename, index=False)
        os.remove('tmp.json')
        print(f"✅ Saved to {filename}")

    start += delta
