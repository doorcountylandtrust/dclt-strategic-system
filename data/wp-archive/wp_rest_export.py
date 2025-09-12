import os
import csv
import requests
from markdownify import markdownify as md

SITE_URL = "https://doorcountylandtrust.org"   # <-- change if needed
OUTPUT_DIR = "./wp-rest-output"
PER_PAGE = 100  # WP REST max allowed

# ---------- Helpers ----------

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def fetch_all(endpoint):
    """Fetch all pages/posts from WP REST API with pagination"""
    items = []
    page = 1
    while True:
        url = f"{SITE_URL}/wp-json/wp/v2/{endpoint}?per_page={PER_PAGE}&page={page}&status=publish"
        r = requests.get(url)
        if r.status_code != 200:
            break
        batch = r.json()
        if not batch:
            break
        items.extend(batch)
        page += 1
    return items

def save_markdown(item, post_type):
    slug = item.get("slug") or "untitled"
    title = item.get("title", {}).get("rendered", "Untitled")
    date = item.get("date", "")
    link = item.get("link", "")
    content_html = item.get("content", {}).get("rendered", "")
    content_md = md(content_html, heading_style="ATX")

    folder = os.path.join(OUTPUT_DIR, post_type)
    ensure_dir(folder)
    filepath = os.path.join(folder, f"{slug}.md")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"*Date:* {date}\n")
        f.write(f"*Link:* {link}\n\n")
        f.write(content_md)

    return {
        "id": item.get("id"),
        "title": title,
        "slug": slug,
        "type": post_type,
        "date": date,
        "link": link,
        "word_count": len(content_md.split()),
        "snippet": content_md[:200].replace("\n", " ") + "..."
    }

# ---------- Main ----------

def main():
    ensure_dir(OUTPUT_DIR)

    all_items = []
    for endpoint in ["pages", "posts"]:
        print(f"Fetching {endpoint}...")
        items = fetch_all(endpoint)
        for item in items:
            row = save_markdown(item, endpoint)
            all_items.append(row)

    # Write CSV audit
    csv_path = os.path.join(OUTPUT_DIR, "audit.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "slug", "type", "date", "link", "word_count", "snippet"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_items)

    print(f"Export complete. {len(all_items)} items saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()