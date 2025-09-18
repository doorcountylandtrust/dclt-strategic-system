import os
import csv
import asyncio
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from playwright.async_api import async_playwright

# -------------- Helpers ----------------

def safe_text(el):
    return el.get_text(strip=True) if el else ""

def extract_social_links(soup, base_url):
    socials = {"facebook": "", "instagram": "", "youtube": "", "linkedin": ""}
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if "facebook.com" in href and not socials["facebook"]:
            socials["facebook"] = href
        elif "instagram.com" in href and not socials["instagram"]:
            socials["instagram"] = href
        elif "youtube.com" in href or "youtu.be" in href:
            if not socials["youtube"]:
                socials["youtube"] = href
        elif "linkedin.com" in href and not socials["linkedin"]:
            socials["linkedin"] = href
    return socials

def detect_donation_provider(href):
    if not href:
        return ""
    if "donorperfect" in href: return "DonorPerfect"
    if "paypal.com" in href: return "PayPal"
    if "stripe.com" in href: return "Stripe"
    if "networkforgood" in href: return "Network for Good"
    if "givebutter" in href: return "Givebutter"
    if "justgiving" in href: return "JustGiving"
    if "classy.org" in href: return "Classy"
    if "everyaction" in href: return "EveryAction"
    if "qgiv" in href: return "Qgiv"
    return "Other"

# -------------- Main Scraper ----------------

async def scrape_org(playwright, org, url, out_dir, screenshots=True):
    result = {
        "Organization": org,
        "URL": url,
        "H1": "",
        "MetaTitle": "",
        "MetaDescription": "",
        "NavItems": "",
        "CTAs": "",
        "DonateURL": "",
        "DonationProvider": "",
        "NewsletterURL": "",
        "EventsURL": "",
        "StaffBoardURL": "",
        "Facebook": "",
        "Instagram": "",
        "YouTube": "",
        "LinkedIn": "",
        "Status": "Error"
    }

    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()

    try:
        await page.goto(url, timeout=60000)
        content = await page.content()
        soup = BeautifulSoup(content, "html.parser")

        # --- Basic Metadata
        result["H1"] = safe_text(soup.find("h1"))
        if soup.title:
            result["MetaTitle"] = soup.title.string.strip()
        desc = soup.find("meta", attrs={"name": "description"})
        if desc and desc.get("content"):
            result["MetaDescription"] = desc["content"].strip()

        # --- Nav Items
        nav_links = [safe_text(a) for a in soup.find_all("a") if a and safe_text(a)]
        result["NavItems"] = " | ".join(nav_links[:15])  # limit for readability

        # --- CTAs
        ctas = []
        for a in soup.find_all("a", href=True):
            txt = safe_text(a).lower()
            if any(x in txt for x in ["donate", "give", "join", "renew", "volunteer", "support"]):
                ctas.append(txt)
                if "donate" in txt and not result["DonateURL"]:
                    result["DonateURL"] = a["href"]
        result["CTAs"] = ", ".join(set(ctas))
        result["DonationProvider"] = detect_donation_provider(result["DonateURL"])

        # --- Newsletter, Events, Staff/Board
        for a in soup.find_all("a", href=True):
            txt = safe_text(a).lower()
            href = a["href"].lower()
            if "subscribe" in txt or "newsletter" in txt or "email" in href:
                result["NewsletterURL"] = a["href"]
            if "event" in txt or "calendar" in txt:
                result["EventsURL"] = a["href"]
            if "board" in txt or "staff" in txt or "team" in txt:
                result["StaffBoardURL"] = a["href"]

        # --- Social Links
        socials = extract_social_links(soup, url)
        result.update({
            "Facebook": socials["facebook"],
            "Instagram": socials["instagram"],
            "YouTube": socials["youtube"],
            "LinkedIn": socials["linkedin"]
        })

        # --- Screenshots
        if screenshots:
            os.makedirs(os.path.join(out_dir, "screenshots"), exist_ok=True)
            fname = org.replace(" ", "_").replace("/", "_")
            await page.screenshot(path=os.path.join(out_dir, "screenshots", f"{fname}_homepage.png"), full_page=False)

        result["Status"] = "OK"

    except Exception as e:
        result["Status"] = f"Error: {str(e)[:100]}"

    await browser.close()
    return result

async def main(input_tsv, output_tsv, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    results = []

    with open(input_tsv, newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    async with async_playwright() as p:
        for row in rows:
            org = row.get("Organization") or row.get("Name") or "Unknown"
            url = row.get("URL") or row.get("Website")
            if not url:
                continue
            print(f"Scraping {org} - {url}")
            res = await scrape_org(p, org, url, out_dir)
            results.append(res)

    # Write results
    with open(output_tsv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys(), delimiter="\t")
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", required=True, help="Input TSV file (with Organization and URL columns)")
    parser.add_argument("--outfile", required=True, help="Output TSV file")
    parser.add_argument("--outdir", default="out", help="Output directory for screenshots")
    args = parser.parse_args()

    asyncio.run(main(args.infile, args.outfile, args.outdir))