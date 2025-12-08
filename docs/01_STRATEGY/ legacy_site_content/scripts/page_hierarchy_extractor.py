#!/usr/bin/env python3

from pathlib import Path
import re
import json
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
INPUT_FILE = "pages_working.xml"

class PageNode:
    def __init__(self, page_id, title, slug, parent_id=0, menu_order=0):
        self.page_id = int(page_id) if page_id else 0
        self.title = title or "Untitled"
        self.slug = slug or ""
        self.parent_id = int(parent_id) if parent_id else 0
        self.menu_order = int(menu_order) if menu_order else 0
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        # Sort children by menu order
        self.children.sort(key=lambda x: x.menu_order)

    def to_dict(self):
        return {
            "id": self.page_id,
            "title": self.title,
            "slug": self.slug,
            "parent_id": self.parent_id,
            "menu_order": self.menu_order,
            "children": [child.to_dict() for child in self.children]
        }

    def print_tree(self, indent=0):
        prefix = "  " * indent
        order_info = f" (order: {self.menu_order})" if self.menu_order > 0 else ""
        print(f"{prefix}- {self.title} [ID: {self.page_id}, Slug: {self.slug}]{order_info}")
        for child in self.children:
            child.print_tree(indent + 1)

def safe_find_text(element, xpath, namespaces=None):
    """Safely find text content from XML element"""
    try:
        if namespaces:
            found = element.find(xpath, namespaces)
        else:
            found = element.find(xpath)
        return found.text if found is not None and found.text else ""
    except:
        return ""

def extract_pages_from_xml(xml_file_path):
    """Extract all pages from WordPress XML export"""
    pages = {}

    try:
        if LXML_AVAILABLE:
            parser = ET.XMLParser(recover=True, strip_cdata=False)
            tree = ET.parse(xml_file_path, parser)
        else:
            tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except Exception as e:
        print(f"❌ Error parsing XML: {e}")
        print("🔧 Trying to create a truncated version...")

        # Try to work with truncated version
        try:
            with open(xml_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Find last complete </item> before issues
            lines = content.split('\n')
            truncate_line = 130000  # Start looking from here to capture pages
            for i in range(130000, min(len(lines), 195000)):
                if '</item>' in lines[i]:
                    truncate_line = i + 1
                    break
                if i > 140000:  # Don't search too far
                    break

            # Create truncated content
            truncated_content = '\n'.join(lines[:truncate_line]) + '\n</channel>\n</rss>'

            # Write and parse truncated file
            temp_file = xml_file_path + '.temp_truncated'
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(truncated_content)

            if LXML_AVAILABLE:
                parser = ET.XMLParser(recover=True, strip_cdata=False)
                tree = ET.parse(temp_file, parser)
            else:
                tree = ET.parse(temp_file)
            root = tree.getroot()

            # Clean up temp file
            Path(temp_file).unlink()
            print("✅ Successfully parsed truncated XML")

        except Exception as e2:
            print(f"❌ Failed to parse even truncated XML: {e2}")
            return pages

    # Define namespaces
    namespaces = {
        'wp': 'http://wordpress.org/export/1.2/',
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    items = root.findall('.//item')
    print(f"📊 Found {len(items)} total items in XML")

    page_count = 0
    for item in items:
        # Check if this is a page
        post_type = safe_find_text(item, 'wp:post_type', namespaces)
        if post_type != 'page':
            continue

        # Extract page data
        page_id = safe_find_text(item, 'wp:post_id', namespaces)
        title = safe_find_text(item, 'title')
        slug = safe_find_text(item, 'wp:post_name', namespaces)
        parent_id = safe_find_text(item, 'wp:post_parent', namespaces)
        menu_order = safe_find_text(item, 'wp:menu_order', namespaces)
        status = safe_find_text(item, 'wp:status', namespaces)

        # Skip if missing essential data or not published
        if not page_id or not title:
            continue

        # Convert to integers with defaults
        try:
            page_id = int(page_id)
            parent_id = int(parent_id) if parent_id else 0
            menu_order = int(menu_order) if menu_order else 0
        except ValueError:
            continue

        # Skip duplicates
        if page_id in pages:
            continue

        # Create page node
        page = PageNode(page_id, title, slug, parent_id, menu_order)
        pages[page_id] = page
        page_count += 1

        print(f"  📄 {title} [ID: {page_id}, Parent: {parent_id}, Order: {menu_order}]")

    print(f"✅ Extracted {page_count} pages")
    return pages

def build_page_tree(pages):
    """Build hierarchical tree from flat page list"""
    root_pages = []

    # First pass: identify root pages and build parent-child relationships
    for page_id, page in pages.items():
        if page.parent_id == 0:
            root_pages.append(page)
        else:
            # Find parent and add this page as child
            parent = pages.get(page.parent_id)
            if parent:
                parent.add_child(page)
            else:
                # Parent not found, treat as root
                print(f"⚠️  Parent {page.parent_id} not found for page '{page.title}' (ID: {page_id})")
                root_pages.append(page)

    # Sort root pages by menu order
    root_pages.sort(key=lambda x: x.menu_order)

    return root_pages

def print_page_hierarchy(root_pages):
    """Print the page hierarchy with indentation"""
    print("\n📋 PAGE HIERARCHY:")
    print("=" * 50)

    if not root_pages:
        print("No pages found.")
        return

    for page in root_pages:
        page.print_tree()

def export_hierarchy_json(root_pages, output_file="page_hierarchy.json"):
    """Export hierarchy as JSON"""
    hierarchy = [page.to_dict() for page in root_pages]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hierarchy, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Hierarchy exported to {output_file}")

def main():
    print("🚀 Starting WordPress Page Hierarchy Extraction...")
    print(f"📂 Input file: {INPUT_FILE}")

    # Extract pages from XML
    pages = extract_pages_from_xml(INPUT_FILE)

    if not pages:
        print("❌ No pages found!")
        return

    # Build hierarchy tree
    root_pages = build_page_tree(pages)

    # Print hierarchy
    print_page_hierarchy(root_pages)

    # Export as JSON
    export_hierarchy_json(root_pages)

    # Print summary statistics
    print(f"\n📊 SUMMARY:")
    print(f"   Total pages: {len(pages)}")
    print(f"   Root pages: {len(root_pages)}")

    # Count total children
    def count_children(page):
        return len(page.children) + sum(count_children(child) for child in page.children)

    total_children = sum(count_children(page) for page in root_pages)
    print(f"   Child pages: {total_children}")

if __name__ == "__main__":
    main()