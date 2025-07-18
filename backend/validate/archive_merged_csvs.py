import os
import shutil
from datetime import date

# === Paths ===
MERGED_DIR = "outputs/results/merged"
ARCHIVE_BASE_DIR = "outputs/archives"
today_str = date.today().isoformat()
archive_dir = os.path.join(ARCHIVE_BASE_DIR, today_str)

# === Create archive directory if needed ===
os.makedirs(archive_dir, exist_ok=True)

# === Archive only merged CSVs ===
archived = []
errors = []

print(f"📦 Starting archive step → {archive_dir}")

for file in os.listdir(MERGED_DIR):
    if file.startswith("merged_") and file.endswith(".csv"):
        src = os.path.join(MERGED_DIR, file)
        dst = os.path.join(archive_dir, file)
        try:
            shutil.copy2(src, dst)
            archived.append(file)
        except Exception as e:
            errors.append((file, str(e)))

# === Print final report ===
if archived:
    print(f"✅ Archived {len(archived)} merged files to: {archive_dir}")
else:
    print(f"⚠️ No files archived. Check if merged_*.csv files exist.")

if errors:
    print("❌ Errors occurred during archiving:")
    for f, e in errors:
        print(f" - {f}: {e}")
