import os
import argparse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_logo(url, output_dir, org_name):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        ext = ".png"
        if "svg" in content_type:
            ext = ".svg"
        elif "jpeg" in content_type or "jpg" in content_type:
            ext = ".jpg"
        filename = f"{org_name.replace(' ', '_')}_logo{ext}"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            f.write(resp.content)
        return filename
    except Exception as e:
        print(f"⚠️ Failed to download {url} for {org_name}: {e}")
        return None

def find_logo(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        for img in soup.find_all("img"):
            src = img.get("src", "")
            if any(k in src.lower() for k in ["logo", "header", "brand"]):
                return urljoin(url, src)
        return None
    except Exception as e:
        print(f"⚠️ Failed to scrape {url}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input TSV")
    parser.add_argument("--output", required=True, help="Path to output TSV")
    parser.add_argument("--start", help="State name or org name to start after")
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t")
    print(f"✅ Loaded {len(df)} rows from {args.input}")

    # If --start is given, find where to start
    if args.start:
        start_idx = None
        for i, row in df.iterrows():
            if args.start.lower() in str(row["State"]).lower() or args.start.lower() in str(row["Organization"]).lower():
                start_idx = i
                break
        if start_idx is not None:
            df = df.iloc[start_idx+1:]  # start *after* the match
            print(f"➡️ Starting scrape after '{args.start}' (row {start_idx}) → {len(df)} rows remain")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    results = []
    for _, row in df.iterrows():
        org = str(row["Organization"])
        url = str(row["URL"])
        if not url or url == "nan":
            continue
        print(f"🔍 {org} → {url}")
        logo_url = find_logo(url)
        logo_file = None
        if logo_url:
            logo_file = download_logo(logo_url, os.path.dirname(args.output), org)
        results.append({
            "State": row.get("State", ""),
            "Organization": org,
            "URL": url,
            "LogoFile": logo_file if logo_file else ""
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv(args.output, sep="\t", index=False)
    print(f"✅ Saved {len(out_df)} rows to {args.output}")

if __name__ == "__main__":
    main()