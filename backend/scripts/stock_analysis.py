import pandas as pd
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === Paths ===
FMP_API_KEY = os.getenv("FMP_API_KEY")
if not FMP_API_KEY:
    raise EnvironmentError("❌ Missing FMP_API_KEY in .env")

input_dir = "outputs/results/sentiment"
output_dir = "outputs/results/merged"
os.makedirs(output_dir, exist_ok=True)

# === Fetch FMP Price Data ===
def get_fmp_stock_data(symbol, start_date, end_date):
    # Add a 3-day buffer to increase chance of valid nextdayclose
    buffered_end_date = min(end_date + pd.Timedelta(days=3), datetime.today().date())

    url = (
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
        f"?from={start_date}&to={buffered_end_date}&apikey={FMP_API_KEY}"
    )

    print(f"🔍 Fetching FMP data for {symbol} from {start_date} to {buffered_end_date}")
    print(f"🌐 URL: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"❌ FMP request failed: {response.text}")

    raw_data = response.json().get("historical", [])
    if not raw_data:
        print(f"⚠️ No stock data returned for {symbol} (empty response).")
        return pd.DataFrame()

    # Build DataFrame
    df = pd.DataFrame(raw_data)
    df.columns = [col.strip().lower() for col in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    print(f"✅ Fetched {len(df)} rows of price data for {symbol}")
    return df


# === Merge Sentiment + Price Data ===
for filename in os.listdir(input_dir):
    if not filename.endswith("sentiment.csv"):
        continue

    symbol = filename.split("_")[0].upper()
    if symbol in ["BRK-A", "BRK.A"]:
        symbol = "BRK-A"
    elif symbol in ["BRK-B", "BRK.B"]:
        symbol = "BRK-B"

    sentiment_path = os.path.join(input_dir, filename)

    try:
        sentiment_df = pd.read_csv(sentiment_path)
        sentiment_df.columns = [col.strip().lower() for col in sentiment_df.columns]

        if "date" not in sentiment_df.columns:
            raise ValueError(f"❌ No 'date' column in {filename}")

        sentiment_df["date"] = pd.to_datetime(sentiment_df["date"]).dt.normalize()
        start_date = sentiment_df["date"].min().date()
        end_date = sentiment_df["date"].max().date() + pd.Timedelta(days=1)

        stock_df = get_fmp_stock_data(symbol, start_date, end_date)

        if stock_df.empty:
            print(f"⚠️ Skipping {symbol}: No stock data to merge.")
            continue  # ✅ Prevents crashing on NaNs if stock data is missing

        stock_df["nextdayclose"] = stock_df["close"].shift(-1)
        stock_df["nextdayreturn"] = (stock_df["nextdayclose"] / stock_df["close"]) - 1
        stock_df["date"] = pd.to_datetime(stock_df["date"]).dt.normalize()

        merged_df = pd.merge(
            sentiment_df,
            stock_df[["date", "close", "nextdayclose", "nextdayreturn"]],
            on="date",
            how="left"
        )

        missing_count = merged_df["nextdayreturn"].isna().sum()
        if missing_count > 0:
            print(f"⚠️ {symbol} has {missing_count} rows with missing return data.")

        merged_path = os.path.join(output_dir, f"merged_{symbol}.csv")
        merged_df.to_csv(merged_path, index=False)
        print(f"✅ Merged and saved: {merged_path}")

    except Exception as e:
        print(f"❌ Failed for {filename} ➜ {e}")
