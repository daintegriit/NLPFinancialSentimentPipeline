# update_nextday_returns.py

import pandas as pd
import os

INPUT_PATH = "outputs/results/merged_sentiment_price.csv"
OUTPUT_PATH = "outputs/results/merged_sentiment_price.csv"

def compute_next_day_returns(df):
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['ticker', 'date'])

    def group_logic(group):
        group = group.sort_values(by='date')
        group['nextdayclose'] = group['close'].shift(-1)
        group['nextdayreturn'] = (group['nextdayclose'] - group['close']) / group['close']
        return group

    df = df.groupby('ticker', group_keys=False).apply(group_logic)
    return df

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input CSV not found at {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)
    updated_df = compute_next_day_returns(df)
    updated_df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ nextdayclose and nextdayreturn added successfully to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
