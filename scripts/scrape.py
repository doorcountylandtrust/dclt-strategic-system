import argparse, asyncio, csv, json, re, time
from urllib.parse import urljoin, urlparse
import aiohttp
from aiolimiter import AsyncLimiter
from bs4 import BeautifulSoup
import pandas as pd
import tldextract

FIELD_SCHEMA = [
    "State","Organization","URL","Status","Title","MetaDescription",
    "H1s","PrimaryNavCTAs","DonateURL","VolunteerURL","LandownerURL",
    "EmailCapture","Socials","CMSHints","AnalyticsHints"
]

ROBOT_AGENT = "LandTrustAuditBot/1.0 (+https://example.org/bot-info)"

def norm_url(u: str) -> str:
    if not u:
        return ""
    if not u.startswith(("http://","https://")):
        return "https://" + u
    return u

def extract_texts(el_list):
    return [re.sub(r"\s+"," ",el.get_text(strip=True)) for el in el_list if el]

def find_first_link(soup, keywords):
    for a in soup.select("a[href]"):
        text = (a.get_text() or "").strip().lower()
        href = a["href"]
        for kw in keywords:
            if kw in text:
                return href
    return None

def detect_email_capture(soup):
    # crude heuristic: newsletter/email inputs + submit
    forms = soup.find_all("form")
    for f in forms:
        inputs = " ".join([i.get("type","") for i in f.find_all("input")])
        placeholders = " ".join([i.get("placeholder","").lower() for i in f.find_all("input")])
        if "email" in inputs or "email" in placeholders:
            return True
    return False

def detect_socials(soup, base):
    socials = {}
    for a in soup.select("a[href]"):
        href = a["href"]
        if any(s in href for s in ["facebook.com","instagram.com","x.com","twitter.com","youtube.com","linkedin.com","tiktok.com","vimeo.com"]):
            socials[tldextract.extract(href).domain] = href
    return socials

def cms_hints(html):
    hints = []
    if "wp-content" in html or "wp-json" in html:
        hints.append("WordPress")
    if "drupal" in html:
        hints.append("Drupal")
    if "shopify" in html:
        hints.append("Shopify")
    if "squarespace" in html:
        hints.append("Squarespace")
    if "webflow" in html:
        hints.append("Webflow")
    return list(sorted(set(hints)))

def analytics_hints(html):
    hints = []
    if "googletagmanager.com" in html or "gtag(" in html or "analytics.js" in html:
        hints.append("Google Analytics/Tag Manager")
    if "plausible.io/js" in html:
        hints.append("Plausible")
    if "umami.is" in html:
        hints.append("Umami")
    if "hotjar.com" in html:
        hints.append("Hotjar")
    return list(sorted(set(hints)))

async def fetch(session, url):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=20)) as r:
            text = await r.text(errors="ignore")
            return r.status, text, str(r.url)
    except Exception as e:
        return None, f"ERROR: {e}", url

async def process_row(session, limiter, state, org, url):
    url = norm_url(url)
    await limiter.acquire()
    status, html, final_url = await fetch(session, url)
    if status is None or not html or (isinstance(html, str) and html.startswith("ERROR:")):
        return [state, org, url, f"FetchError:{html}", "", "", "", "", "", "", "", "", "", "",""]

    soup = BeautifulSoup(html, "lxml")

    title = (soup.title.get_text(strip=True) if soup.title else "")[:300]
    meta_desc = ""
    md = soup.find("meta", attrs={"name":"description"})
    if not md:
        md = soup.find("meta", attrs={"property":"og:description"})
    if md:
        meta_desc = md.get("content","")[:500]

    h1s = extract_texts(soup.find_all("h1"))[:3]

    # primary nav CTAs (top-level <nav> anchors, first 10)
    nav = soup.find("nav")
    nav_ctas = []
    if nav:
        nav_ctas = extract_texts(nav.find_all("a"))[:10]

    donate_href = find_first_link(soup, ["donate","give","donation"])
    volunteer_href = find_first_link(soup, ["volunteer","volunteering"])
    landowner_href = find_first_link(soup, ["landowner","protect your land","conserve your land","land protection","conservation options"])

    # absolutize
    def abs_url(h):
        if not h: return ""
        return urljoin(final_url, h)

    donate_url = abs_url(donate_href)
    volunteer_url = abs_url(volunteer_href)
    landowner_url = abs_url(landowner_href)

    email_capture = detect_email_capture(soup)
    socials = detect_socials(soup, final_url)

    cms = cms_hints(html)
    analytics = analytics_hints(html)

    return [
        state, org, final_url, status, title, meta_desc,
        "|".join(h1s), "|".join(nav_ctas), donate_url, volunteer_url, landowner_url,
        "Yes" if email_capture else "No", json.dumps(socials), "|".join(cms), "|".join(analytics)
    ]

async def main(args):
    df = pd.read_csv(args.input, sep="\t")
    if args.state:
        wanted = set([s.strip() for s in args.state.split(",")])
        df = df[df["State"].isin(wanted)]
    os.makedirs(args.out, exist_ok=True)

    connector = aiohttp.TCPConnector(limit_per_host=3)
    headers = {"User-Agent": "Mozilla/5.0 (compatible; LandTrustAuditBot/1.0)"}
    limiter = AsyncLimiter(3, 1)  # 3 req/sec
    tasks = []
    rows = []

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for _, row in df.iterrows():
            tasks.append(process_row(session, limiter, row["State"], row["Organization"], row["URL"]))
        for chunk_start in range(0, len(tasks), 50):
            chunk = tasks[chunk_start:chunk_start+50]
            results = await asyncio.gather(*chunk)
            rows.extend(results)
            # simple pacing
            await asyncio.sleep(1)

    out_csv = f"{args.out}/scrape.csv"
    out_jsonl = f"{args.out}/scrape.jsonl"
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(FIELD_SCHEMA)
        for r in rows:
            w.writerow(r)
    with open(out_jsonl, "w", encoding="utf-8") as f:
        for r in rows:
            obj = dict(zip(FIELD_SCHEMA, r))
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    print("Wrote:", out_csv, out_jsonl)

if __name__ == "__main__":
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument("--in", dest="input", required=True, help="Input TSV (State, Organization, URL)")
    parser.add_argument("--out", dest="out", default="out/scrape", help="Output folder")
    parser.add_argument("--state", dest="state", help="Comma-separated States to limit")
    args = parser.parse_args()
    asyncio.run(main(args))
