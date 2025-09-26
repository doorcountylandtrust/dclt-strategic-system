# scripts/scrapers/scrape_all.py
import os
import sys
import argparse
import pandas as pd

# --- Imports from your three scrapers ---
import requests
from bs4 import BeautifulSoup
import subprocess
import json

# ========== SCRAPER FUNCTIONS ==========

def scrape_socials(url):
    """Find Facebook, Instagram, Twitter, LinkedIn links on a site."""
    socials = {"facebook": None, "instagram": None, "twitter": None, "linkedin": None}
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "facebook.com" in href and not socials["facebook"]:
                socials["facebook"] = href
            elif "instagram.com" in href and not socials["instagram"]:
                socials["instagram"] = href
            elif "twitter.com" in href and not socials["twitter"]:
                socials["twitter"] = href
            elif "linkedin.com" in href and not socials["linkedin"]:
                socials["linkedin"] = href
    except Exception as e:
        print(f"⚠️ Social scrape failed for {url}: {e}")
    return socials


def scrape_metadata(url):
    """Pull <title>, first <h1>, and meta description."""
    meta = {"title": None, "h1": None, "description": None}
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "lxml")
        title = soup.find("title")
        if title:
            meta["title"] = title.text.strip()
        h1 = soup.find("h1")
        if h1:
            meta["h1"] = h1.text.strip()
        desc = soup.find("meta", attrs={"name": "description"})
        if desc and desc.get("content"):
            meta["description"] = desc["content"].strip()
    except Exception as e:
        print(f"⚠️ Metadata scrape failed for {url}: {e}")
    return meta


def scrape_lighthouse(url):
    """Run Lighthouse (needs Chrome + Node installed)."""
    result = {"lighthouse_perf": None, "lighthouse_access": None, "lighthouse_best": None, "lighthouse_seo": None}
    try:
        cmd = [
            "npx", "lighthouse", url,
            "--quiet", "--chrome-flags='--headless'",
            "--output=json", "--output-path=stdout"
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        report = json.loads(proc.stdout)
        cats = report.get("categories", {})
        result["lighthouse_perf"] = cats.get("performance", {}).get("score")
        result["lighthouse_access"] = cats.get("accessibility", {}).get("score")
        result["lighthouse_best"] = cats.get("best-practices", {}).get("score")
        result["lighthouse_seo"] = cats.get("seo", {}).get("score")
    except Exception as e:
        print(f"⚠️ Lighthouse failed for {url}: {e}")
    return result

# TODO: def scrape_logos(url): pass
# TODO: def scrape_hero(url): pass

# ========== MAIN PIPELINE ==========

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input TSV of orgs (State, Organization, URL)")
    parser.add_argument("--output", required=True, help="Output enriched TSV")
    args = parser.parse_args()

    # Load input
    df = pd.read_csv(args.input, sep="\t")
    print(f"✅ Loaded {len(df)} orgs from {args.input}")

    results = []

    for _, row in df.iterrows():
        url = str(row["URL"]).strip()
        if not url or url == "nan":
            continue

        print(f"🔎 Scraping {row['Organization']} ({url})")

        row_data = {
            "State": row.get("State", ""),
            "Organization": row.get("Organization", ""),
            "URL": url
        }

        # Socials
        row_data.update(scrape_socials(url))

        # Metadata
        row_data.update(scrape_metadata(url))

        # Lighthouse
        row_data.update(scrape_lighthouse(url))

        results.append(row_data)

    # Save
    out_df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    out_df.to_csv(args.output, sep="\t", index=False)
    print(f"✅ Saved {len(out_df)} rows to {args.output}")


if __name__ == "__main__":
    main()