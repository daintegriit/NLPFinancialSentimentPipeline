# validate/flag_skipped_relevant.py

import pandas as pd
import os

def list_skipped_files(skipped_dir="data/raw_news"):
    return [f for f in os.listdir(skipped_dir) if f.endswith("_skipped.csv")]

def select_rows(df):
    print("\n🔍 Previewing skipped headlines...\n")
    for idx, row in df.iterrows():
        print(f"[{idx}] {row['title']}")
    print("\n👉 Enter comma-separated row numbers to mark as relevant (e.g. 0,3,4):")
    selection = input("> ")
    indices = [int(i.strip()) for i in selection.split(",") if i.strip().isdigit()]
    return df.loc[indices]

def main():
    skipped_files = list_skipped_files()
    print("📂 Available skipped files:")
    for i, file in enumerate(skipped_files):
        print(f"[{i}] {file}")
    
    choice = int(input("\n🗂️ Choose file to review: "))
    file_name = skipped_files[choice]
    symbol = file_name.split("_")[0]
    
    path = f"data/raw_news/{file_name}"
    df = pd.read_csv(path)

    if df.empty:
        print("🚫 No skipped entries found.")
        return

    selected = select_rows(df)
    if selected.empty:
        print("❌ No entries selected.")
        return

    os.makedirs("data/manual_review", exist_ok=True)
    save_path = f"data/manual_review/{symbol}_flagged_relevant.csv"

    # Append mode
    if os.path.exists(save_path):
        selected.to_csv(save_path, mode="a", index=False, header=False)
    else:
        selected.to_csv(save_path, index=False)
    
    print(f"✅ Saved {len(selected)} flagged entries to {save_path}")

if __name__ == "__main__":
    main()
