import os
import pandas as pd
import requests
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
missing_path = os.path.join(BASE_DIR, "../data/landtrusts/datasets/missing_logos.tsv")
logos_dir = os.path.join(BASE_DIR, "../data/landtrusts/datasets/screens/logos")
report_path = os.path.join(BASE_DIR, "../data/landtrusts/datasets/retry_logos_report.tsv")

os.makedirs(logos_dir, exist_ok=True)

# Load missing orgs
missing = pd.read_csv(missing_path, sep="\t")

def normalize_name(name):
    return (
        name.strip()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("&", "and")
        .replace("__", "_")
    )

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    for _, row in missing.iterrows():
        org = row["Organization"]
        url = row["URL"]
        base_filename = normalize_name(org)
        png_path = os.path.join(logos_dir, f"{base_filename}_logo.png")
        svg_path = os.path.join(logos_dir, f"{base_filename}_logo.svg")
        status = "Fail"

        try:
            print(f"Trying {org} → {url}")
            page.goto(url, timeout=45000)

            # 1. Try <img> with "logo" in src
            logo_el = page.query_selector('img[src*="logo"]')
            if logo_el:
                src = logo_el.get_attribute("src")
                if src:
                    # Handle relative URLs
                    src_url = urljoin(url, src)
                    r = requests.get(src_url, timeout=20)
                    if r.status_code == 200:
                        with open(png_path, "wb") as f:
                            f.write(r.content)
                        status = "DownloadedIMG"
                        print(f" → Saved {png_path}")
                        results.append({"Organization": org, "URL": url, "File": png_path, "Status": status})
                        continue

            # 2. Try inline <svg>
            svg_el = page.query_selector("header svg, nav svg, svg")
            if svg_el:
                outer_html = svg_el.evaluate("(el) => el.outerHTML")
                if outer_html:
                    with open(svg_path, "w") as f:
                        f.write(outer_html)
                    status = "SavedSVG"
                    print(f" → Saved {svg_path}")
                    results.append({"Organization": org, "URL": url, "File": svg_path, "Status": status})
                    continue

            # 3. Fallback: screenshot header
            header_el = page.query_selector("header, nav, .site-header, .navbar")
            if header_el:
                header_el.screenshot(path=png_path)
                status = "HeaderScreenshot"
                print(f" → Fallback screenshot {png_path}")

        except Exception as e:
            print(f"Error with {org}: {e}")
            status = "Error"

        results.append({"Organization": org, "URL": url, "File": base_filename, "Status": status})

    browser.close()

# Save results
pd.DataFrame(results).to_csv(report_path, sep="\t", index=False)
print(f"\nRetry complete. Report saved to {report_path}")