#!/usr/bin/env python3
import os
import subprocess
import pandas as pd

INPUT_FILE = os.path.join("data", "landtrusts", "datasets", "accredited_land_trusts_remainder.tsv")
OUTPUT_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_lighthouse.tsv")

def run_lighthouse(url, out_json):
    """Run Lighthouse via CLI and save results to JSON."""
    try:
        # --quiet keeps logs minimal
        subprocess.run([
            "lighthouse", url,
            "--quiet",
            "--chrome-flags=--headless",
            "--output=json",
            f"--output-path={out_json}"
        ], check=True)
        return True
    except Exception as e:
        print(f"⚠️ Lighthouse failed for {url}: {e}")
        return False

def extract_scores(json_file):
    import json
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        categories = data.get("categories", {})
        return {
            "Performance": categories.get("performance", {}).get("score"),
            "Accessibility": categories.get("accessibility", {}).get("score"),
            "Best_Practices": categories.get("best-practices", {}).get("score"),
            "SEO": categories.get("seo", {}).get("score"),
        }
    except Exception as e:
        return {"Performance": None, "Accessibility": None, "Best_Practices": None, "SEO": None}

def main():
    df = pd.read_csv(INPUT_FILE, sep="\t")
    results = []

    tmp_json = "tmp_lighthouse.json"

    for _, row in df.iterrows():
        org = row["Organization"]
        url = row["URL"]

        if not isinstance(url, str) or not url.startswith("http"):
            continue

        print(f"🚦 Auditing {org} ({url}) ...")
        if run_lighthouse(url, tmp_json):
            scores = extract_scores(tmp_json)
        else:
            scores = {"Performance": None, "Accessibility": None, "Best_Practices": None, "SEO": None}

        results.append({
            "State": row["State"],
            "Organization": org,
            "URL": url,
            **scores
        })

    pd.DataFrame(results).to_csv(OUTPUT_FILE, sep="\t", index=False)
    print(f"✅ Saved Lighthouse results to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()