#!/usr/bin/env python3
import os
import re
import urllib.parse
import shutil
from pathlib import Path
from collections import defaultdict

def decode_url_encoding(text):
    """Decode URL-encoded characters in filenames."""
    return urllib.parse.unquote(text)

def remove_hash_id(filename):
    """Remove trailing hash IDs from Notion export filenames."""
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    
    # Remove hash pattern: space followed by 32 hex characters
    cleaned_stem = re.sub(r'\s+[a-f0-9]{32}$', '', stem)
    return cleaned_stem + suffix

def to_kebab_case(text):
    """Convert text to kebab-case."""
    stem = Path(text).stem
    suffix = Path(text).suffix
    
    # Replace spaces and underscores with hyphens
    kebab = re.sub(r'[\s_]+', '-', stem)
    
    # Remove special characters except hyphens and alphanumeric and parentheses
    kebab = re.sub(r'[^a-zA-Z0-9\-()]', '', kebab)
    
    # Convert to lowercase
    kebab = kebab.lower()
    
    # Remove multiple consecutive hyphens
    kebab = re.sub(r'-+', '-', kebab)
    
    # Remove leading/trailing hyphens
    kebab = kebab.strip('-')
    
    return kebab + suffix

def generate_clean_filename(original_filename):
    """Generate a clean filename from a Notion export filename."""
    # Step 1: Decode URL encoding
    decoded = decode_url_encoding(original_filename)
    
    # Step 2: Remove hash ID
    no_hash = remove_hash_id(decoded)
    
    # Step 3: Convert to kebab-case
    kebab = to_kebab_case(no_hash)
    
    return kebab

def handle_filename_collision(desired_filename, directory, existing_names):
    """Handle filename collisions by adding numeric suffixes."""
    stem = Path(desired_filename).stem
    suffix = Path(desired_filename).suffix
    
    counter = 1
    final_filename = desired_filename
    
    while final_filename in existing_names or (directory / final_filename).exists():
        final_filename = f"{stem}-{counter}{suffix}"
        counter += 1
    
    existing_names.add(final_filename)
    return final_filename

def scan_markdown_files(data_dir):
    """Scan for all markdown files in the data directory."""
    md_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    return md_files

def build_file_mapping(data_dir):
    """Build mapping of old filenames to new filenames."""
    md_files = scan_markdown_files(data_dir)
    file_mapping = {}
    link_mapping = {}
    existing_names = set()
    
    print(f"Found {len(md_files)} markdown files")
    
    for file_path in md_files:
        original_filename = file_path.name
        directory = file_path.parent
        
        # Generate clean filename
        clean_filename = generate_clean_filename(original_filename)
        
        # Handle collisions
        final_filename = handle_filename_collision(clean_filename, directory, existing_names)
        
        # Store mappings
        old_path = str(file_path)
        new_path = str(directory / final_filename)
        
        file_mapping[old_path] = new_path
        link_mapping[original_filename] = final_filename
        
        if original_filename != final_filename:
            print(f"'{original_filename}' -> '{final_filename}'")
    
    return file_mapping, link_mapping

def update_markdown_links(content, link_mapping):
    """Update markdown links to use new filenames."""
    def replace_link(match):
        link_text = match.group(1)
        link_target = match.group(2)
        
        # Decode the link target
        decoded_target = decode_url_encoding(link_target)
        
        # Check if we have a mapping for this file
        if decoded_target in link_mapping:
            new_target = link_mapping[decoded_target]
            return f"[{link_text}]({new_target})"
        
        return match.group(0)
    
    # Pattern to match markdown links
    pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
    updated_content = re.sub(pattern, replace_link, content)
    
    return updated_content

def rename_files(file_mapping):
    """Rename files according to the mapping."""
    renamed_count = 0
    
    for old_path, new_path in file_mapping.items():
        if old_path == new_path:
            continue
            
        old_file = Path(old_path)
        new_file = Path(new_path)
        
        if not old_file.exists():
            print(f"Warning: Source file not found: {old_path}")
            continue
        
        try:
            shutil.move(str(old_file), str(new_file))
            print(f"Renamed: {old_file.name} -> {new_file.name}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
    
    print(f"Renamed {renamed_count} files")

def update_file_contents(file_mapping, link_mapping):
    """Update markdown links in all files."""
    updated_count = 0
    
    for old_path, new_path in file_mapping.items():
        file_path = Path(new_path)
        
        if not file_path.exists():
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = update_markdown_links(content, link_mapping)
            
            if content != updated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"Updated links in: {file_path.name}")
                updated_count += 1
        
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
    
    print(f"Updated {updated_count} files")

def main():
    data_dir = "data"
    
    if not Path(data_dir).exists():
        print(f"Error: Data directory not found: {data_dir}")
        return
    
    print("Starting Notion filename cleanup...")
    
    # Build file mapping
    file_mapping, link_mapping = build_file_mapping(data_dir)
    
    # Rename files
    rename_files(file_mapping)
    
    # Update file contents
    update_file_contents(file_mapping, link_mapping)
    
    print("Filename cleanup complete!")

if __name__ == "__main__":
    main()