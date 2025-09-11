import os
import csv
import argparse
from lxml import etree as ET
from markdownify import markdownify as md

# ---------- Helpers ----------

def slugify(value):
    """Make a filesystem-friendly slug"""
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in value.lower()).strip("_")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# ---------- Main Exporter ----------

def export_wxr(xml_file, out_dir):
    print(f"Parsing {xml_file}...")
    ns = {
        "content": "http://purl.org/rss/1.0/modules/content/",
        "wp": "http://wordpress.org/export/1.2/",
        "dc": "http://purl.org/dc/elements/1.1/",
    }

    # Parse with forgiving XML parser
    parser = ET.XMLParser(recover=True, encoding="utf-8")
    tree = ET.parse(xml_file, parser)
    root = tree.getroot()

    items = root.find("channel").findall("item")

    # Collect metadata
    posts = {}
    for item in items:
        post_id = item.find("wp:post_id", ns).text
        title = item.find("title").text or "Untitled"
        slug = item.find("wp:post_name", ns).text or slugify(title)
        post_type = item.find("wp:post_type", ns).text
        parent = item.find("wp:post_parent", ns).text
        content_html = item.find("content:encoded", ns).text or ""
        content_md = md(content_html, heading_style="ATX")

        posts[post_id] = {
            "id": post_id,
            "title": title,
            "slug": slug,
            "type": post_type,
            "parent": parent,
            "content_md": content_md,
            "date": item.find("wp:post_date", ns).text,
            "author": item.find("dc:creator", ns).text,
            "status": item.find("wp:status", ns).text,
            "link": item.find("link").text,
        }

    # Recursive path builder for hierarchy
    def get_path(post_id):
        post = posts[post_id]
        if post["parent"] != "0" and post["parent"] in posts:
            return os.path.join(get_path(post["parent"]), slugify(post["slug"]))
        else:
            return os.path.join(out_dir, post["type"], slugify(post["slug"]))

    # Write Markdown files
    for post_id, post in posts.items():
        if post["status"] != "publish":
            continue  # skip drafts/trash

        folder = os.path.dirname(get_path(post_id))
        ensure_dir(folder)
        file_path = f"{get_path(post_id)}.md"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {post['title']}\n\n")
            f.write(f"*Date:* {post['date']}\n")
            f.write(f"*Author:* {post['author']}\n")
            f.write(f"*Link:* {post['link']}\n\n")
            f.write(post["content_md"])

    print("Markdown export complete.")

    # Write CSV index
    csv_path = os.path.join(out_dir, "index.csv")
    ensure_dir(out_dir)
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "slug", "type", "parent", "date", "author", "status", "link"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for post in posts.values():
            writer.writerow({k: v for k, v in post.items() if k in fieldnames})

    print(f"CSV index written to {csv_path}")


# ---------- CLI ----------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert WordPress WXR export to Markdown + CSV")
    parser.add_argument(
        "xml_file",
        nargs="?",
        default="doorcountylandtrust.WordPress.2025-09-11.xml",
        help="Path to the WordPress XML export (WXR) file"
    )
    parser.add_argument(
        "out_dir",
        nargs="?",
        default="./wp-output",
        help="Directory to write Markdown and CSV files"
    )
    args = parser.parse_args()

    export_wxr(args.xml_file, args.out_dir)