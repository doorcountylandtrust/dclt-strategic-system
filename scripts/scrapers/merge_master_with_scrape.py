# scripts/scrapers/merge_master_with_scrape.py
import os
import pandas as pd

BASE_FILE = os.path.join("data", "landtrusts", "datasets", "landtrust_master_final.tsv")
SCRAPE_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_combined.tsv")
OUTPUT_FILE = os.path.join("data", "landtrusts", "datasets", "landtrust_master_enriched.tsv")

def main():
    print(f"📂 Loading {BASE_FILE}")
    master = pd.read_csv(BASE_FILE, sep="\t")
    print(f"✅ Loaded master: {len(master)} rows, {len(master.columns)} columns")

    print(f"📂 Loading {SCRAPE_FILE}")
    scrape = pd.read_csv(SCRAPE_FILE, sep="\t")
    print(f"✅ Loaded scrape: {len(scrape)} rows, {len(scrape.columns)} columns")

    # Merge on URL
    merged = pd.merge(master, scrape, on="URL", how="left", suffixes=("", "_scrape"))

    print(f"🔗 Merged dataset has {len(merged)} rows and {len(merged.columns)} columns")

    # Save
    merged.to_csv(OUTPUT_FILE, sep="\t", index=False)
    print(f"💾 Saved enriched dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()