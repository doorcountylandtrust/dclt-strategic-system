#!/usr/bin/env python3
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Input & output paths (relative to repo root)
INPUT_FILE = os.path.join("data", "landtrusts", "datasets", "accredited_land_trusts_remainder.tsv")
OUTPUT_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_site_metadata.tsv")

def clean_text(text):
    if not text:
        return ""
    return " ".join(text.split())

def extract_metadata(url):
    """Scrape metadata, title, H1s, nav links, donate/newsletter presence."""
    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return {"Status": f"Error {r.status_code}"}
        soup = BeautifulSoup(r.text, "lxml")

        title = clean_text(soup.title.string if soup.title else "")
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            description = clean_text(meta_desc["content"])

        h1_tags = [clean_text(h1.get_text()) for h1 in soup.find_all("h1")]
        h1_text = " | ".join(h1_tags)

        # Approximate word count from visible text
        text = soup.get_text(" ", strip=True)
        word_count = len(text.split())

        # Collect nav links
        nav_links = []
        for nav in soup.find_all(["nav", "header"]):
            for a in nav.find_all("a", href=True):
                nav_links.append(clean_text(a.get_text()))
        nav_links = list(set([n for n in nav_links if n]))  # unique, drop empties
        nav_links_str = ", ".join(nav_links)

        # Detect donate/newsletter links
        donate = any(re.search(r"donate|give", (a.get("href") or "").lower()) for a in soup.find_all("a", href=True))
        newsletter = any(re.search(r"newsletter|subscribe|join", (a.get("href") or "").lower()) for a in soup.find_all("a", href=True))

        return {
            "Status": "OK",
            "Title": title,
            "Meta_Description": description,
            "H1": h1_text,
            "Word_Count": word_count,
            "Nav_Links": nav_links_str,
            "Donate_Link": donate,
            "Newsletter_Link": newsletter,
        }

    except Exception as e:
        return {"Status": f"Error: {e}"}

def main():
    print(f"📥 Loading {INPUT_FILE} ...")
    df = pd.read_csv(INPUT_FILE, sep="\t")
    results = []

    for _, row in df.iterrows():
        state = row.get("State")
        org = row.get("Organization")
        url = row.get("URL")

        if not isinstance(url, str) or not url.startswith("http"):
            print(f"⚠️ Skipping {org}: invalid URL")
            continue

        print(f"🔎 Scraping {org} ({url}) ...")
        data = extract_metadata(url)
        results.append({
            "State": state,
            "Organization": org,
            "URL": url,
            **data
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_FILE, sep="\t", index=False)
    print(f"✅ Saved metadata to {OUTPUT_FILE} with {len(out_df)} rows")

if __name__ == "__main__":
    main()