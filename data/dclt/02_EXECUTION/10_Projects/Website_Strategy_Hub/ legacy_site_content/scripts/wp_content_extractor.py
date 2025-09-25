from pathlib import Path
import re
from collections import defaultdict

# Try to use lxml for better XML recovery if available
try:
    from lxml import etree as ET
    LXML_AVAILABLE = True
    print("✅ Using lxml with recovery parser")
except ImportError:
    import xml.etree.ElementTree as ET
    LXML_AVAILABLE = False
    print("⚠️  lxml not available - using standard XML parser")

# === CONFIGURATION ===
INPUT_FILE = "clean_pages_working.xml"  # Replace with your actual file name
OUTPUT_DIR = Path("markdown-content")
LIMIT = None  # Optional: Set to a number for partial run, or None for full

# === HELPERS ===
def sanitize_filename(name):
    return re.sub(r'[^\w\-]+', '-', name.lower()).strip('-')

def clean_html_content(html):
    html = re.sub(r'\[.*?\]', '', html)  # Remove WordPress shortcodes
    html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
    return html.strip()

def write_markdown_file(title, slug, pub_date, content, post_type, categories, index):
    content = clean_html_content(content)
    frontmatter = f"""---
title: "{title.strip()}"
slug: "{slug}"
date: "{pub_date.strip()}"
tags: {categories}
type: "{post_type}"
---
"""
    markdown_content = frontmatter + "\n" + content

    output_path = OUTPUT_DIR / post_type
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"{slug}.md"
    filepath = output_path / filename
    if filepath.exists():
        filename = f"{slug}-{index}.md"
        filepath = output_path / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)

# === MAIN FUNCTION ===
def parse_wordpress_xml(xml_file_path, limit=None):
    if LXML_AVAILABLE:
        parser = ET.XMLParser(recover=True)
        tree = ET.parse(xml_file_path, parser=parser)
    else:
        tree = ET.parse(xml_file_path)
    root = tree.getroot()
    items = root.findall("./channel/item")

    success_count = 0
    failure_log = []
    post_type_counter = defaultdict(int)

    for i, item in enumerate(items):
        if limit and i >= limit:
            break
        try:
            title = item.findtext("title") or f"untitled-{i}"
            slug = sanitize_filename(title)
            pub_date = item.findtext("pubDate") or ""
            content_encoded = item.findtext("{http://purl.org/rss/1.0/modules/content/}encoded") or ""
            post_type = item.findtext("{http://wordpress.org/export/1.2/}post_type") or "post"
            categories = [cat.text for cat in item.findall("category") if cat.text]

            print(f"[{i}] Processing '{title}' ({post_type})")
            write_markdown_file(title, slug, pub_date, content_encoded, post_type, categories, i)
            success_count += 1
            post_type_counter[post_type] += 1
        except Exception as e:
            failure_log.append(f"Item {i}: {e}")

    print("\n✅ Done!")
    print(f"✅ Success: {success_count} items written")
    print(f"⚠️ Errors: {len(failure_log)} (showing first 5):")
    for err in failure_log[:5]:
        print("  •", err)
    print(f"📊 Post Type Summary:")
    for pt, count in post_type_counter.items():
        print(f"  - {pt}: {count} items")

# === ENTRY POINT ===
if __name__ == "__main__":
    parse_wordpress_xml(INPUT_FILE, limit=LIMIT)