#!/usr/bin/env python3
import os
import pandas as pd

# Input files
META_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_site_metadata.tsv")
LIGHT_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_lighthouse.tsv")

# Output file
OUTPUT_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_combined.tsv")

def main():
    # Load data
    meta = pd.read_csv(META_FILE, sep="\t")
    light = pd.read_csv(LIGHT_FILE, sep="\t")

    # Merge on shared keys
    combined = pd.merge(
        meta,
        light,
        on=["State", "Organization", "URL"],
        how="outer"  # keep everything even if one file missed
    )

    # Save combined
    combined.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"✅ Merged {len(meta)} metadata rows with {len(light)} lighthouse rows")
    print(f"➡️ Saved combined results to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()