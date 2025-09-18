import os
import csv
import re
import argparse
from lxml import etree as ET
from markdownify import markdownify as md

# ---------- Helpers ----------

def slugify(value):
    """Make a filesystem-friendly slug"""
    value = value.lower().strip()
    value = re.sub(r"[^\w\s-]", "", value)  # remove non-word chars
    value = re.sub(r"[\s_-]+", "-", value)  # collapse whitespace and dashes
    return value.strip("-") or "untitled"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def clean_html(html):
    """Remove builder junk/shortcodes before markdownify"""
    if not html:
        return ""
    # strip Beaver Builder shortcodes and similar
    html = re.sub(r"\[(\/?)(et_pb|fl_builder)[^\]]*\]", "", html)
    return html

# ---------- Main Exporter ----------

def export_wxr(xml_file, out_dir, allowed_types=("page", "post")):
    print(f"Parsing {xml_file}...")
    ns = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
        "dc": "http://purl.org/dc/elements/1.1/",
    }

    parser = ET.XMLParser(recover=True, encoding="utf-8")
    tree = ET.parse(xml_file, parser)
    root = tree.getroot()

    items = root.find("channel").findall("item")

    posts = {}
    for item in items:
        post_type = item.find("wp:post_type", ns).text
        status = item.find("wp:status", ns).text

        if post_type not in allowed_types:
            continue
        if status != "publish":
            continue

        post_id = item.find("wp:post_id", ns).text
        parent = item.find("wp:post_parent", ns).text

        title = item.find("title").text or "Untitled"
        slug = item.find("wp:post_name", ns).text
        if not slug:
            slug = slugify(title)

        content_html = item.find("content:encoded", ns).text or ""
        content_html = clean_html(content_html)
        content_md = md(content_html, heading_style="ATX")

        posts[post_id] = {
            "id": post_id,
            "title": title,
            "slug": slug,
            "type": post_type,
            "parent": parent,
            "date": item.find("wp:post_date", ns).text,
            "author": item.find("dc:creator", ns).text,
            "link": item.find("link").text,
            "content_md": content_md,
        }

    # recursive path builder for hierarchy
    def get_path(post_id):
        post = posts[post_id]
        if post["type"] == "page" and post["parent"] != "0" and post["parent"] in posts:
            return os.path.join(get_path(post["parent"]), slugify(post["slug"]))
        else:
            return os.path.join(out_dir, post["type"], slugify(post["slug"]))

    # Write Markdown files
    for post_id, post in posts.items():
        folder = os.path.dirname(get_path(post_id))
        ensure_dir(folder)
        filename = f"{post['slug']}.md"
        filepath = os.path.join(folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# {post['title']}\n\n")
            f.write(f"*Date:* {post['date']}\n")
            f.write(f"*Author:* {post['author']}\n")
            f.write(f"*Link:* {post['link']}\n\n")
            f.write(post["content_md"])

    print(f"Exported {len(posts)} posts/pages to {out_dir}")

    # Write CSV index
    csv_path = os.path.join(out_dir, "index.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "slug", "type", "parent", "date", "author", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([{k: v for k, v in post.items() if k in fieldnames} for post in posts.values()])

    print(f"CSV index written to {csv_path}")


# ---------- CLI ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert WordPress WXR export to Markdown + CSV (content only, with hierarchy)")
    parser.add_argument(
        "xml_file",
        nargs="?",
        default="doorcountylandtrust.WordPress.2025-09-11.xml",
        help="Path to the WordPress XML export (WXR) file"
    )
    parser.add_argument(
        "out_dir",
        nargs="?",
        default="./wp-clean-output",
        help="Directory to write Markdown and CSV files"
    )
    args = parser.parse_args()

    export_wxr(args.xml_file, args.out_dir)