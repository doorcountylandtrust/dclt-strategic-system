import os
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
input_path = os.path.join(BASE_DIR, "../data/landtrusts/datasets/landtrust_master_with_socials.tsv")
output_path = os.path.join(BASE_DIR, "../data/landtrusts/datasets/phase2_scrape.tsv")

# Load URLs
orgs = pd.read_csv(input_path, sep="\t")

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    for _, row in orgs.iterrows():
        org = row["Organization"]
        url = row["URL"]
        status = "Fail"
        h1_text, meta_title, meta_desc, nav_items, ctas, donate_provider = "", "", "", "", "", ""

        try:
            print(f"Scraping {org} → {url}")
            page.goto(url, timeout=45000)
            html = page.content()
            soup = BeautifulSoup(html, "lxml")

            # H1 + tagline
            h1 = soup.find("h1")
            if h1: h1_text = h1.get_text(strip=True)

            # Meta
            title_tag = soup.find("title")
            if title_tag: meta_title = title_tag.get_text(strip=True)

            desc_tag = soup.find("meta", attrs={"name": "description"})
            if desc_tag: meta_desc = desc_tag.get("content", "")

            # Nav items
            nav = soup.find("nav")
            if nav:
                nav_items = ", ".join([a.get_text(strip=True) for a in nav.find_all("a")[:10]])

            # CTA presence
            page_text = soup.get_text(" ", strip=True).lower()
            found_ctas = [cta for cta in ["donate", "join", "volunteer"] if cta in page_text]
            ctas = ", ".join(found_ctas)

            # Donation form provider
            form = soup.find("form", attrs={"action": True})
            if form:
                action_url = form.get("action")
                if action_url:
                    if "givelively" in action_url:
                        donate_provider = "GiveLively"
                    elif "classy" in action_url:
                        donate_provider = "Classy"
                    elif "blackbaud" in action_url or "convio" in action_url:
                        donate_provider = "Blackbaud"
                    elif "donorbox" in action_url:
                        donate_provider = "Donorbox"
                    else:
                        donate_provider = action_url

            status = "OK"

        except Exception as e:
            print(f"Error scraping {org}: {e}")
            status = "Error"

        results.append({
            "Organization": org,
            "URL": url,
            "H1": h1_text,
            "MetaTitle": meta_title,
            "MetaDescription": meta_desc,
            "NavItems": nav_items,
            "CTAs": ctas,
            "DonationProvider": donate_provider,
            "Status": status
        })

    browser.close()

# Save output
pd.DataFrame(results).to_csv(output_path, sep="\t", index=False)
print(f"\nPhase 2 scrape complete. Results saved to {output_path}")