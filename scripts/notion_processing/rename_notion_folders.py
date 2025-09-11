#!/usr/bin/env python3
import os
import re
import urllib.parse
import shutil
from pathlib import Path
from collections import defaultdict

def decode_url_encoding(text):
    """Decode URL-encoded characters in folder names."""
    return urllib.parse.unquote(text)

def remove_hash_id(foldername):
    """Remove trailing hash IDs from Notion export folder names."""
    # Remove hash pattern: space followed by 32 hex characters
    cleaned_name = re.sub(r'\s+[a-f0-9]{32}$', '', foldername)
    return cleaned_name

def to_kebab_case(text):
    """Convert text to kebab-case."""
    # Replace spaces and underscores with hyphens
    kebab = re.sub(r'[\s_]+', '-', text)
    
    # Remove special characters except hyphens and alphanumeric and parentheses
    kebab = re.sub(r'[^a-zA-Z0-9\-()]', '', kebab)
    
    # Convert to lowercase
    kebab = kebab.lower()
    
    # Remove multiple consecutive hyphens
    kebab = re.sub(r'-+', '-', kebab)
    
    # Remove leading/trailing hyphens
    kebab = kebab.strip('-')
    
    return kebab

def generate_clean_foldername(original_foldername):
    """Generate a clean folder name from a Notion export folder name."""
    # Step 1: Decode URL encoding
    decoded = decode_url_encoding(original_foldername)
    
    # Step 2: Remove hash ID
    no_hash = remove_hash_id(decoded)
    
    # Step 3: Convert to kebab-case
    kebab = to_kebab_case(no_hash)
    
    return kebab

def handle_foldername_collision(desired_foldername, parent_dir, existing_names):
    """Handle folder name collisions by adding numeric suffixes."""
    counter = 1
    final_foldername = desired_foldername
    
    while final_foldername in existing_names or (parent_dir / final_foldername).exists():
        final_foldername = f"{desired_foldername}-{counter}"
        counter += 1
    
    existing_names.add(final_foldername)
    return final_foldername

def get_all_directories(data_dir):
    """Get all directories in the data directory, sorted by depth (deepest first)."""
    directories = []
    for root, dirs, files in os.walk(data_dir):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            directories.append(dir_path)
    
    # Sort by depth (deepest first) to avoid path conflicts during renaming
    directories.sort(key=lambda x: len(x.parts), reverse=True)
    return directories

def build_folder_mapping(data_dir):
    """Build mapping of old folder paths to new folder paths."""
    directories = get_all_directories(data_dir)
    folder_mapping = {}
    existing_names_per_parent = defaultdict(set)
    
    print(f"Found {len(directories)} directories")
    
    for dir_path in directories:
        original_foldername = dir_path.name
        parent_dir = dir_path.parent
        
        # Skip the main data directories (1-strategy, 2-execution, 3-reference-tools)
        if str(parent_dir) == data_dir and original_foldername in ['1-strategy', '2-execution', '3-reference-tools']:
            folder_mapping[str(dir_path)] = str(dir_path)
            continue
        
        # Generate clean folder name
        clean_foldername = generate_clean_foldername(original_foldername)
        
        # Handle collisions within the same parent directory
        parent_key = str(parent_dir)
        final_foldername = handle_foldername_collision(clean_foldername, parent_dir, existing_names_per_parent[parent_key])
        
        # Store mapping
        old_path = str(dir_path)
        new_path = str(parent_dir / final_foldername)
        
        folder_mapping[old_path] = new_path
        
        if original_foldername != final_foldername:
            print(f"'{original_foldername}' -> '{final_foldername}'")
    
    return folder_mapping

def update_markdown_links_for_folders(content, folder_mapping):
    """Update markdown links to account for renamed folders."""
    def replace_folder_link(match):
        link_text = match.group(1)
        link_target = match.group(2)
        
        # Decode the link target
        decoded_target = decode_url_encoding(link_target)
        
        # Check if any folder in the path has been renamed
        updated_target = decoded_target
        for old_folder_path, new_folder_path in folder_mapping.items():
            old_folder_name = Path(old_folder_path).name
            new_folder_name = Path(new_folder_path).name
            
            if old_folder_name != new_folder_name and old_folder_name in updated_target:
                # Replace the folder name in the path
                updated_target = updated_target.replace(old_folder_name, new_folder_name)
        
        if updated_target != decoded_target:
            return f"[{link_text}]({updated_target})"
        
        return match.group(0)
    
    # Pattern to match markdown links with paths
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    updated_content = re.sub(pattern, replace_folder_link, content)
    
    return updated_content

def rename_folders(folder_mapping):
    """Rename folders according to the mapping."""
    renamed_count = 0
    
    for old_path, new_path in folder_mapping.items():
        if old_path == new_path:
            continue
            
        old_dir = Path(old_path)
        new_dir = Path(new_path)
        
        if not old_dir.exists():
            print(f"Warning: Source directory not found: {old_path}")
            continue
        
        if new_dir.exists():
            print(f"Warning: Target directory already exists: {new_path}")
            continue
        
        try:
            shutil.move(str(old_dir), str(new_dir))
            print(f"Renamed: {old_dir.name} -> {new_dir.name}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
    
    print(f"Renamed {renamed_count} folders")

def update_markdown_files_for_folders(data_dir, folder_mapping):
    """Update markdown links in all files to account for renamed folders."""
    updated_count = 0
    
    # Get all markdown files after folder renaming
    md_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = update_markdown_links_for_folders(content, folder_mapping)
            
            if content != updated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"Updated folder links in: {file_path.name}")
                updated_count += 1
        
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
    
    print(f"Updated folder links in {updated_count} files")

def main():
    data_dir = "data"
    
    if not Path(data_dir).exists():
        print(f"Error: Data directory not found: {data_dir}")
        return
    
    print("Starting Notion folder cleanup...")
    
    # Build folder mapping
    folder_mapping = build_folder_mapping(data_dir)
    
    # Rename folders
    rename_folders(folder_mapping)
    
    # Update file contents to reflect folder changes
    update_markdown_files_for_folders(data_dir, folder_mapping)
    
    print("Folder cleanup complete!")

if __name__ == "__main__":
    main()