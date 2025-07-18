# backend/daily_runner.py
import os
import sys
import subprocess
import traceback
import time
from datetime import datetime
import pytz

from rich.console import Console
from rich.spinner import Spinner
from rich.table import Table

console = Console()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# === Logging setup ===
LOG_PATH = "outputs/logs/pipeline_run.log"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# 🌍 Set local timezone
local_tz = pytz.timezone("America/New_York")

def log(msg):
    timestamp = datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")  # Local time
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def save_script_log(script_name, output):
    log_dir = "logs/script_runs"
    os.makedirs(log_dir, exist_ok=True)
    filename = f"{script_name}__{datetime.now(local_tz).strftime('%Y-%m-%d_%H-%M-%S')}.log"
    with open(os.path.join(log_dir, filename), "w") as f:
        f.write(output)

log(f"\n🧠 NLP Pipeline Start | {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')}")

# === Core Data Pipeline Scripts ===
scripts = [
    "scripts/news_scraper.py",
    "scripts/fmp_news_scraper.py",
    "scripts/sentiment_analysis.py",
    "scripts/stock_analysis.py",
    "scripts/update_nextday_returns.py"

]

for script in scripts:
    log(f"▶️ Running {script}")
    start_time = time.time()

    try:
        proc = subprocess.run(
            ["python3", script],
            capture_output=True,
            text=True
        )
        duration = time.time() - start_time

        # Save log output to file
        output_log = f"\n--- STDOUT ---\n{proc.stdout}\n--- STDERR ---\n{proc.stderr}\n"
        log_file = f"logs/script_runs/{os.path.basename(script)}__{datetime.now(local_tz).strftime('%Y-%m-%d_%H-%M-%S')}.log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "w") as f:
            f.write(output_log)

        # Display output summary
        print(output_log)

        if proc.returncode == 0:
            log(f"✅ Finished {script} in {duration:.2f}s\n")
        else:
            log(f"❌ Error running {script} | Exit code: {proc.returncode}\n")
            sys.exit(1)

    except Exception as e:
        log(f"❌ Exception in {script}: {e}")
        traceback.print_exc()
        sys.exit(1)


# === Apply user-flagged skipped headlines ===
log("\n🧠 Applying user-flagged skipped headlines...")
try:
    subprocess.run(["python3", "validate/apply_manual_flags.py"], check=True)
    log("✅ Manual flag application successful")
except subprocess.CalledProcessError as e:
    log(f"❌ Manual flag merge failed: {e}")
    sys.exit(1)


# === Learn new keywords from flagged headlines ===
log("\n🧠 Learning new keywords from flagged entries...")
try:
    subprocess.run(["python3", "validate/learn_keywords.py"], check=True)
    log("✅ Keyword learning complete")
except subprocess.CalledProcessError as e:
    log(f"❌ Keyword learning failed: {e}")
    sys.exit(1)


# === Run Auto-Rescue on Validated Skipped ===
log("\n🧠 Running auto_rescue.py to reprocess validated skipped headlines...")
try:
    subprocess.run(["python3", "scripts/auto_rescue.py"], check=True)
    log("✅ Auto-rescue completed successfully")
except subprocess.CalledProcessError as e:
    log(f"❌ Auto-rescue failed: {e}")
    sys.exit(1)


# === Prune unused learned keywords ===
log("\n🧹 Pruning unused learned keywords...")
try:
    subprocess.run(["python3", "validate/prune_dead_keywords.py"], check=True)
    log("✅ Keyword pruning complete")
except subprocess.CalledProcessError as e:
    log(f"❌ Keyword pruning failed: {e}")
    sys.exit(1)


# === Validation, Checksum, Archive, Alert ===
validation_scripts = [
    "validate/validate_csvs.py",
    "validate/generate_checksums_and_rowdiffs.py",
    "validate/archive_merged_csvs.py",
    "validate/alert_if_anomalies_email.py"  # or alert_if_anomalies.py if non-email
]

log("\n🔎 Running post-ingestion validation and alert steps...")
for script in validation_scripts:
    spinner = console.status(f"Running {script}", spinner="line")
    with spinner:
        start_time = time.time()
        try:
            proc = subprocess.run(["python3", script], capture_output=True, text=True)
            duration = time.time() - start_time
            save_script_log(os.path.basename(script), proc.stdout + "\n" + proc.stderr)

            if proc.returncode == 0:
                log(f"✔️  Step complete: {script} in {duration:.2f}s")
            else:
                log(f"❌ Validation error in {script} | Exit code: {proc.returncode}")
                sys.exit(1)
        except Exception as e:
            log(f"❌ Exception during script: {e}")
            traceback.print_exc()
            sys.exit(1)

# === Add this after all script runs ===
log("\n🧩 Running CSV unifier...")
try:
    subprocess.run(["python3", "validate/unify_sentiment_price_csvs.py"], check=True)
    log("✅ Unifier finished successfully")
except subprocess.CalledProcessError as e:
    log(f"❌ Unifier failed: {e}")
    sys.exit(1)

log(f"\n🏁 Pipeline finished at {datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S')} — All steps ✅\n")

