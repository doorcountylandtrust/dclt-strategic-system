#!/usr/bin/env python3
"""
DCLT Strategic System - Frontmatter Parser
Scans all markdown files and extracts YAML frontmatter for analysis.
"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime
import json

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML frontmatter
        if content.startswith('---'):
            # Find the closing ---
            end_marker = content.find('---', 3)
            if end_marker != -1:
                yaml_content = content[3:end_marker].strip()
                try:
                    metadata = yaml.safe_load(yaml_content)
                    return metadata
                except yaml.YAMLError as e:
                    print(f"YAML error in {file_path}: {e}")
                    return None
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def scan_files(base_path, scan_paths):
    """Scan specified paths for markdown files"""
    all_files = []
    
    for scan_path in scan_paths:
        full_path = Path(base_path) / scan_path
        if full_path.exists():
            for md_file in full_path.rglob('*.md'):
                all_files.append(md_file)
    
    return all_files

def main():
    """Main parsing function"""
    # Load configuration
    try:
        with open('config/settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found. Run setup script first.")
        return
    
    # Scan for markdown files
    base_path = Path('.')
    scan_paths = config.get('scan_paths', ['data'])
    
    markdown_files = scan_files(base_path, scan_paths)
    print(f"Found {len(markdown_files)} markdown files")
    
    # Extract frontmatter from all files
    all_metadata = []
    for file_path in markdown_files:
        metadata = extract_frontmatter(file_path)
        if metadata:
            metadata['file_path'] = str(file_path)
            metadata['last_modified'] = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat()
            all_metadata.append(metadata)
    
    # Save extracted metadata
    output_path = Path('output/reports/extracted_metadata.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_metadata, f, indent=2, default=str)
    
    print(f"Extracted metadata from {len(all_metadata)} files")
    print(f"Results saved to {output_path}")
    
    # Print summary
    types = {}
    statuses = {}
    for item in all_metadata:
        item_type = item.get('type', 'unknown')
        item_status = item.get('status', 'unknown')
        types[item_type] = types.get(item_type, 0) + 1
        statuses[item_status] = statuses.get(item_status, 0) + 1
    
    print("\nSummary by type:")
    for type_name, count in types.items():
        print(f"  {type_name}: {count}")
    
    print("\nSummary by status:")
    for status_name, count in statuses.items():
        print(f"  {status_name}: {count}")

if __name__ == "__main__":
    main()
