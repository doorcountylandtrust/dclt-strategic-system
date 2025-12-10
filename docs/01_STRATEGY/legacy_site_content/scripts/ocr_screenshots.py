#!/usr/bin/env python3

import os
import re
from pathlib import Path
from collections import defaultdict

# Configuration
SCREENSHOTS_DIR = Path("/Users/landtrust/Projects/dclt-wordpress/current-site-screenshots")
OUTPUT_DIR = Path("/Users/landtrust/Projects/dclt-wordpress/export/ocr-content")

def parse_filename(filename):
    """Parse screenshot filename to extract section info"""
    # Remove .png extension
    name = filename.replace('.png', '')

    # Extract parts
    parts = name.split('-')

    # Get section number and name
    section_num = parts[0]
    section_name = '-'.join(parts[1:])

    return {
        'filename': filename,
        'section_num': section_num,
        'section_name': section_name,
        'full_name': name
    }

def create_structure_summary():
    """Create a summary of the site structure from filenames"""
    screenshots = sorted(SCREENSHOTS_DIR.glob("*.png"))

    structure = defaultdict(list)

    for screenshot in screenshots:
        info = parse_filename(screenshot.name)
        section_num = info['section_num']
        structure[section_num].append(info)

    # Create summary markdown
    summary = "# Door County Land Trust - Site Structure Summary\n\n"
    summary += f"Based on {len(screenshots)} screenshots\n\n"
    summary += "## Site Hierarchy\n\n"

    for section_num in sorted(structure.keys()):
        pages = structure[section_num]

        # Determine section name from first page
        if section_num == '00':
            summary += "### Homepage\n"
        elif section_num == '01':
            summary += "### 01. About Us\n"
        elif section_num == '02':
            summary += "### 02. How We Save Land\n"
        elif section_num == '03':
            summary += "### 03. Preserves to Explore\n"
        elif section_num == '04':
            summary += "### 04. Upcoming Events\n"
        elif section_num == '05':
            summary += "### 05. Give Generously\n"
        elif section_num == '06':
            summary += "### 06. Gift Shop\n"

        for page in pages:
            summary += f"- {page['section_name']} (`{page['filename']}`)\n"

        summary += "\n"

    return summary

def main():
    print("🚀 Starting OCR Screenshot Processing...")
    print(f"📂 Screenshots directory: {SCREENSHOTS_DIR}")
    print(f"📂 Output directory: {OUTPUT_DIR}")

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create structure summary
    summary = create_structure_summary()

    # Write structure summary
    summary_file = OUTPUT_DIR / "00-structure-summary.md"
    with open(summary_file, 'w') as f:
        f.write(summary)

    print(f"✅ Created structure summary: {summary_file}")

    # Get list of screenshots
    screenshots = sorted(SCREENSHOTS_DIR.glob("*.png"))
    print(f"📊 Found {len(screenshots)} screenshots to process")

    # Create a manifest file for Claude to process
    manifest = "# OCR Processing Manifest\n\n"
    manifest += "The following images need to be processed with OCR:\n\n"

    for screenshot in screenshots:
        info = parse_filename(screenshot.name)
        manifest += f"## {info['full_name']}\n"
        manifest += f"- File: `{screenshot}`\n"
        manifest += f"- Output: `{OUTPUT_DIR / (info['full_name'] + '.md')}`\n"
        manifest += f"- Section: {info['section_num']}\n\n"

    manifest_file = OUTPUT_DIR / "processing-manifest.md"
    with open(manifest_file, 'w') as f:
        f.write(manifest)

    print(f"✅ Created processing manifest: {manifest_file}")
    print(f"\n📝 Next: Use Claude's Read tool to OCR each image and extract content")
    print(f"   Images are located in: {SCREENSHOTS_DIR}")
    print(f"   Output markdown files to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()