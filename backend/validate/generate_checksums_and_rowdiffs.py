import os
import hashlib
import pandas as pd
import json
from datetime import date, timedelta

MERGED_DIR = "outputs/results/merged"
LOG_DIR = "outputs/logs"
os.makedirs(LOG_DIR, exist_ok=True)

today_str = date.today().isoformat()
yesterday_str = (date.today() - timedelta(days=1)).isoformat()

checksums = {}
row_counts = {}
row_diff_report = {}

print("🔍 Starting checksum + rowdiff generation...")

# === Step 1: Generate MD5 checksums and row counts for today ===
def compute_md5(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

for file in os.listdir(MERGED_DIR):
    if not file.startswith("merged_") or not file.endswith(".csv"):
        continue

    symbol = file.replace("merged_", "").replace(".csv", "")
    path = os.path.join(MERGED_DIR, file)

    try:
        checksum = compute_md5(path)
        row_count = pd.read_csv(path).shape[0]
        checksums[symbol] = checksum
        row_counts[symbol] = row_count
    except Exception as e:
        checksums[symbol] = f"❌ Error: {e}"

# === Step 2: Save today's checksums and row counts ===
with open(f"{LOG_DIR}/checksums_{today_str}.json", "w") as f:
    json.dump(checksums, f, indent=2)

with open(f"{LOG_DIR}/rowcounts_{today_str}.json", "w") as f:
    json.dump(row_counts, f, indent=2)

# === Step 3: Compare to yesterday’s row counts (if exists) ===
prev_counts_path = f"{LOG_DIR}/rowcounts_{yesterday_str}.json"
if os.path.exists(prev_counts_path):
    with open(prev_counts_path, "r") as f:
        prev_counts = json.load(f)

    for symbol, new_count in row_counts.items():
        if isinstance(new_count, int) and symbol in prev_counts:
            old_count = prev_counts.get(symbol, 0)
            diff = new_count - int(prev_counts.get(symbol, 0))
            row_diff_report[symbol] = {
                "yesterday": old_count,
                "today": new_count,
                "new_rows": diff
            }

    with open(f"{LOG_DIR}/rowdiff_{today_str}.json", "w") as f:
        json.dump(row_diff_report, f, indent=2)

    print(f"📈 Row diff report saved = {LOG_DIR}/rowdiff_{today_str}.json")
else:
    print("🕐 No previous rowcounts file found. Diff report skipped today.")

print(f"✅ Checksums saved = {LOG_DIR}/checksums_{today_str}.json")
