import os
import pandas as pd
from datetime import datetime, timedelta

# === Config ===
MERGED_DIR = "outputs/results/merged"
CRITICAL_COLUMNS = ["date", "close", "nextdayclose", "nextdayreturn"]
ALLOWED_LATENESS_DAYS = 1

# === Output Logs ===
VALIDATION_LOG = []

print("🛠️ Starting CSV validation pipeline...")

# === Main validation loop ===
for file in os.listdir(MERGED_DIR):
    if not file.startswith("merged_") or not file.endswith(".csv"):
        continue

    path = os.path.join(MERGED_DIR, file)
    symbol = file.replace("merged_", "").replace(".csv", "")
    result = {"symbol": symbol, "status": "✅ OK", "issues": []}

    try:
        df = pd.read_csv(path)

        # === Check row count ===
        if df.empty:
            result["status"] = "❌ FAILED"
            result["issues"].append("Empty file")
            VALIDATION_LOG.append(result)
            continue

        # === Normalize column names ===
        df.columns = [c.strip().lower() for c in df.columns]

        # === Check date column ===
        if "date" not in df.columns:
            result["status"] = "❌ FAILED"
            result["issues"].append("Missing 'date' column")
            VALIDATION_LOG.append(result)
            continue

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        latest_date = df["date"].max()

        if latest_date < datetime.today() - timedelta(days=ALLOWED_LATENESS_DAYS):
            result["status"] = "⚠️ STALE"
            result["issues"].append(f"Latest date is {latest_date.date()}")

        # === Check nulls and presence in critical columns ===
        for col in CRITICAL_COLUMNS:
            if col not in df.columns:
                result["status"] = "❌ FAILED"
                result["issues"].append(f"Missing column: {col}")
            elif df[col].isna().all():
                result["status"] = "❌ FAILED"
                result["issues"].append(f"ALL NaN in column: {col}")

    except Exception as e:
        result["status"] = "❌ ERROR"
        result["issues"].append(str(e))

    VALIDATION_LOG.append(result)

# === Save validation log ===
log_df = pd.DataFrame(VALIDATION_LOG)
os.makedirs("outputs/logs", exist_ok=True)
log_df.to_csv("outputs/logs/validation_log.csv", index=False)
print("✅ Validation complete = outputs/logs/validation_log.csv")
