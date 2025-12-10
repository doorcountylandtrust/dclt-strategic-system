import os
import re

# Set your local docs directory path
DOCS_DIR = "docs"

# Regex pattern to capture Markdown links like [text](link.md)
link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

# Collect broken links
broken_links = []

for root, _, files in os.walk(DOCS_DIR):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            rel_filepath = os.path.relpath(filepath, DOCS_DIR)

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            for match in link_pattern.finditer(content):
                label, target = match.groups()

                # Skip external links and anchors
                if target.startswith("http") or target.startswith("#"):
                    continue

                # Resolve the relative target path
                normalized = os.path.normpath(os.path.join(root, target))

                # Check existence
                if not os.path.exists(normalized):
                    broken_links.append((rel_filepath, target))

# Print results
if broken_links:
    print("\n🚨 Broken links found:\n")
    for source, target in broken_links:
        print(f"- In `{source}` → `{target}` not found")
else:
    print("✅ No broken internal .md links found.")