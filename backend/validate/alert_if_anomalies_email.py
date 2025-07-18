import os
import json
import pandas as pd
import smtplib
from datetime import date
from email.message import EmailMessage
from dotenv import load_dotenv

# === Load secrets from .env ===
load_dotenv()

LOG_DIR = "outputs/logs"
today_str = date.today().isoformat()

EMAIL_TO = os.getenv("ALERT_EMAIL_TO")
EMAIL_FROM = os.getenv("ALERT_EMAIL_FROM")
EMAIL_SUBJECT = os.getenv("ALERT_EMAIL_SUBJECT", "🚨 NLP Pipeline Alert Summary")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

validation_log_path = os.path.join(LOG_DIR, "validation_log.csv")
rowdiff_path = os.path.join(LOG_DIR, f"rowdiff_{today_str}.json")

alerts = []

# === Check validation log ===
if os.path.exists(validation_log_path):
    val_df = pd.read_csv(validation_log_path)
    problems = val_df[val_df["status"].str.startswith("❌") | val_df["status"].str.startswith("⚠️")]
    for _, row in problems.iterrows():
        alerts.append(f"⚠️ {row['symbol']}: {row['status']} ➜ {row['issues']}")
else:
    alerts.append("❌ Missing validation_log.csv")

# === Check rowdiff report ===
if os.path.exists(rowdiff_path):
    with open(rowdiff_path, "r") as f:
        rowdiffs = json.load(f)
    for symbol, stats in rowdiffs.items():
        if stats["new_rows"] == 0:
            alerts.append(f"⚠️ {symbol} had 0 new rows today (unchanged)")
else:
    alerts.append("📭 No row diff file for today")

# === Send email if alerts exist ===
if alerts:
    msg = EmailMessage()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content("🚨 NLP Pipeline Alert Summary:\n\n" + "\n".join(alerts))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"✅ Alert email sent to {EMAIL_TO}")
    except Exception as e:
        print(f"❌ Failed to send alert email: {e}")
else:
    print("✅ No alerts. Email not sent.")
