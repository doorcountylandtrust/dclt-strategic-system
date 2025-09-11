#!/usr/bin/env python3
"""
Notion Export Cleaner for DCLT Strategic System

This script cleans filenames in the input/notion-export-latest directory by:
1. Decoding URL encoding (%20 -> spaces, etc.)
2. Removing trailing hash IDs (32-character hex strings)
3. Converting to kebab-case (lowercase with hyphens)
4. Handling filename conflicts with numbered suffixes
5. Updating internal markdown links to match new filenames
"""

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


def generate_clean_dirname(original_dirname):
    """Generate a clean directory name from a Notion export directory name."""
    # Step 1: Decode URL encoding
    decoded = decode_url_encoding(original_dirname)
    
    # Step 2: Remove hash ID
    no_hash = re.sub(r'\s+[a-f0-9]{32}$', '', decoded)
    
    # Step 3: Convert to kebab-case
    kebab = re.sub(r'[\s_]+', '-', no_hash)
    kebab = re.sub(r'[^a-zA-Z0-9\-()]', '', kebab)
    kebab = kebab.lower()
    kebab = re.sub(r'-+', '-', kebab)
    kebab = kebab.strip('-')
    
    return kebab


def handle_name_collision(desired_name, parent_directory, existing_names, is_dir=False):
    """Handle filename/dirname collisions by adding numeric suffixes."""
    if is_dir:
        counter = 1
        final_name = desired_name
        
        while final_name in existing_names or (parent_directory / final_name).exists():
            final_name = f"{desired_name}-{counter}"
            counter += 1
    else:
        stem = Path(desired_name).stem
        suffix = Path(desired_name).suffix
        
        counter = 1
        final_name = desired_name
        
        while final_name in existing_names or (parent_directory / final_name).exists():
            final_name = f"{stem}-{counter}{suffix}"
            counter += 1
    
    existing_names.add(final_name)
    return final_name


def scan_all_files_and_dirs(root_dir):
    """Scan for all files and directories recursively."""
    files_and_dirs = []
    for root, dirs, files in os.walk(root_dir):
        root_path = Path(root)
        
        # Add directories
        for dir_name in dirs:
            dir_path = root_path / dir_name
            files_and_dirs.append(('dir', dir_path))
        
        # Add files
        for file_name in files:
            file_path = root_path / file_name
            files_and_dirs.append(('file', file_path))
    
    return files_and_dirs


def build_renaming_mapping(input_dir):
    """Build mapping of old paths to new paths for all files and directories."""
    all_items = scan_all_files_and_dirs(input_dir)
    
    # Sort by depth (deepest first for directories)
    all_items.sort(key=lambda x: len(x[1].parts), reverse=True)
    
    file_mapping = {}
    link_mapping = {}
    dir_mapping = {}
    existing_names = defaultdict(set)
    
    print(f"Found {len(all_items)} items to process")
    
    for item_type, item_path in all_items:
        original_name = item_path.name
        parent_dir = item_path.parent
        
        if item_type == 'dir':
            # Generate clean directory name
            clean_name = generate_clean_dirname(original_name)
            
            # Handle collisions
            final_name = handle_name_collision(clean_name, parent_dir, existing_names[str(parent_dir)], is_dir=True)
            
            # Store mapping
            old_path = str(item_path)
            new_path = str(parent_dir / final_name)
            
            dir_mapping[old_path] = new_path
            
            if original_name != final_name:
                print(f"DIR: '{original_name}' -> '{final_name}'")
        
        elif item_type == 'file' and item_path.suffix == '.md':
            # Generate clean filename
            clean_name = generate_clean_filename(original_name)
            
            # Handle collisions
            final_name = handle_name_collision(clean_name, parent_dir, existing_names[str(parent_dir)])
            
            # Store mappings
            old_path = str(item_path)
            new_path = str(parent_dir / final_name)
            
            file_mapping[old_path] = new_path
            link_mapping[original_name] = final_name
            
            if original_name != final_name:
                print(f"FILE: '{original_name}' -> '{final_name}'")
    
    return file_mapping, link_mapping, dir_mapping


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


def rename_directories(dir_mapping):
    """Rename directories according to the mapping."""
    renamed_count = 0
    
    # Sort by path length (deepest first)
    sorted_dirs = sorted(dir_mapping.items(), key=lambda x: len(x[0]), reverse=True)
    
    for old_path, new_path in sorted_dirs:
        if old_path == new_path:
            continue
            
        old_dir = Path(old_path)
        new_dir = Path(new_path)
        
        if not old_dir.exists():
            print(f"Warning: Source directory not found: {old_path}")
            continue
        
        try:
            shutil.move(str(old_dir), str(new_dir))
            print(f"Renamed DIR: {old_dir.name} -> {new_dir.name}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming directory {old_path}: {e}")
    
    print(f"Renamed {renamed_count} directories")


def rename_files(file_mapping, dir_mapping):
    """Rename files according to the mapping, accounting for directory changes."""
    renamed_count = 0
    
    for old_path, new_path in file_mapping.items():
        # Update paths based on directory renames
        updated_old_path = old_path
        updated_new_path = new_path
        
        for old_dir, new_dir in dir_mapping.items():
            if old_path.startswith(old_dir):
                updated_old_path = old_path.replace(old_dir, new_dir, 1)
                updated_new_path = new_path.replace(old_dir, new_dir, 1)
                break
        
        if updated_old_path == updated_new_path:
            continue
            
        old_file = Path(updated_old_path)
        new_file = Path(updated_new_path)
        
        if not old_file.exists():
            print(f"Warning: Source file not found: {updated_old_path}")
            continue
        
        try:
            shutil.move(str(old_file), str(new_file))
            print(f"Renamed FILE: {old_file.name} -> {new_file.name}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming file {updated_old_path}: {e}")
    
    print(f"Renamed {renamed_count} files")


def update_file_contents(file_mapping, link_mapping, dir_mapping):
    """Update markdown links in all files."""
    updated_count = 0
    
    for old_path, new_path in file_mapping.items():
        # Update path based on directory renames
        updated_new_path = new_path
        
        for old_dir, new_dir in dir_mapping.items():
            if new_path.startswith(old_dir):
                updated_new_path = new_path.replace(old_dir, new_dir, 1)
                break
        
        file_path = Path(updated_new_path)
        
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
    input_dir = Path("input/notion-export-latest")
    
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return
    
    print("Starting Notion export filename cleanup...")
    print(f"Processing directory: {input_dir}")
    
    # Build renaming mappings
    file_mapping, link_mapping, dir_mapping = build_renaming_mapping(input_dir)
    
    # Rename directories first (deepest first)
    rename_directories(dir_mapping)
    
    # Rename files
    rename_files(file_mapping, dir_mapping)
    
    # Update file contents
    update_file_contents(file_mapping, link_mapping, dir_mapping)
    
    print("Notion export filename cleanup complete!")


if __name__ == "__main__":
    main()