import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Paths relative to repo root
INPUT_FILE = os.path.join("data", "landtrusts", "datasets", "accredited_land_trusts_remainder.tsv")
OUTPUT_FILE = os.path.join("data", "landtrusts", "datasets", "scrape_socials_expanded.tsv")

def scrape_social_links(url):
    socials = {"website": url, "facebook": "", "instagram": "", "youtube": "", "twitter": "", "linkedin": ""}

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return socials

    soup = BeautifulSoup(resp.text, "lxml")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "facebook.com" in href and not socials["facebook"]:
            socials["facebook"] = href
        elif "instagram.com" in href and not socials["instagram"]:
            socials["instagram"] = href
        elif "youtube.com" in href or "youtu.be" in href:
            socials["youtube"] = href
        elif "twitter.com" in href and not socials["twitter"]:
            socials["twitter"] = href
        elif "linkedin.com" in href and not socials["linkedin"]:
            socials["linkedin"] = href

    return socials

def main():
    df = pd.read_csv(INPUT_FILE, sep="\t")

    # Auto-detect columns
    name_col = None
    url_col = None
    for col in df.columns:
        lower = col.lower()
        if "org" in lower or "name" in lower:
            name_col = col
        if "url" in lower or "website" in lower:
            url_col = col

    print(f"✅ Loaded {len(df)} rows from {INPUT_FILE}")
    print(f"Detected name_col={name_col}, url_col={url_col}")

    results = []
    for _, row in df.iterrows():
        name = row.get(name_col)
        url = row.get(url_col)
        if not isinstance(url, str) or not url.startswith("http"):
            print(f"⚠️ Skipping {name}: no valid website")
            continue

        print(f"🔎 Scraping {name} -> {url}")
        socials = scrape_social_links(url)
        socials["name"] = name
        results.append(socials)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_FILE, sep="\t", index=False)
    print(f"✅ Saved results to {OUTPUT_FILE} with {len(out_df)} rows")

if __name__ == "__main__":
    main()