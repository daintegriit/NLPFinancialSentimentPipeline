import os
import json
import pandas as pd
from datetime import date

# === Paths ===
LOG_DIR = "outputs/logs"
today_str = date.today().isoformat()

validation_log_path = os.path.join(LOG_DIR, "validation_log.csv")
rowdiff_path = os.path.join(LOG_DIR, f"rowdiff_{today_str}.json")

# === Load logs ===
alerts = []

# 1. Check validation log
if os.path.exists(validation_log_path):
    val_df = pd.read_csv(validation_log_path)
    problems = val_df[val_df["status"].str.startswith("❌") | val_df["status"].str.startswith("⚠️")]
    for _, row in problems.iterrows():
        alerts.append(f"⚠️ {row['symbol']}: {row['status']} → {row['issues']}")
else:
    alerts.append("❌ Missing validation_log.csv")

# 2. Check rowdiffs
if os.path.exists(rowdiff_path):
    with open(rowdiff_path, "r") as f:
        rowdiffs = json.load(f)
    for symbol, stats in rowdiffs.items():
        if stats["new_rows"] == 0:
            alerts.append(f"⚠️ {symbol} had 0 new rows today (unchanged)")
else:
    alerts.append("ℹ️ No row diff file for today")

# === Print or deliver alert summary ===
if alerts:
    print("\n🚨 PIPELINE ALERT SUMMARY 🚨")
    for a in alerts:
        print(" -", a)

    # === Optional future: send_email(alerts) or post_to_webhook(alerts)
else:
    print(f"✅ All systems normal as of {today_str}")
