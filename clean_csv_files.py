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
    # Also remove _all suffix commonly added by Notion
    cleaned_stem = re.sub(r'_all$', '', cleaned_stem)
    
    return cleaned_stem + suffix

def remove_problematic_characters(text):
    """Remove characters that can cause filesystem or webserver issues."""
    # Characters that are problematic for filesystems and web servers:
    # < > : " | ? * \ / (Windows/NTFS issues)
    # # % & + space (URL encoding issues)
    # ; = , (query parameter issues)
    # [ ] { } (bracket issues)
    # Non-ASCII characters (encoding issues)
    
    stem = Path(text).stem
    suffix = Path(text).suffix
    
    # Remove or replace problematic characters
    # First handle special cases
    stem = re.sub(r'&', 'and', stem)  # Replace & with 'and'
    stem = re.sub(r'#', 'number', stem)  # Replace # with 'number'
    stem = re.sub(r'%', 'percent', stem)  # Replace % with 'percent'
    
    # Remove other problematic characters
    stem = re.sub(r'[<>:"|?*\\/#+;=,\[\]{}]', '', stem)
    
    # Remove non-ASCII characters (keep only ASCII alphanumeric, hyphens, underscores, parentheses, periods)
    stem = re.sub(r'[^\x00-\x7F]', '', stem)
    
    # Remove any remaining special characters except safe ones
    stem = re.sub(r'[^a-zA-Z0-9\-_().]+', '', stem)
    
    return stem + suffix

def to_kebab_case(text):
    """Convert text to kebab-case."""
    stem = Path(text).stem
    suffix = Path(text).suffix
    
    # Replace spaces and underscores with hyphens
    kebab = re.sub(r'[\s_]+', '-', stem)
    
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
    print(f"  Decoded: '{original_filename}' -> '{decoded}'")
    
    # Step 2: Remove hash ID and _all suffix
    no_hash = remove_hash_id(decoded)
    print(f"  Removed hash: '{decoded}' -> '{no_hash}'")
    
    # Step 3: Remove problematic characters
    safe_chars = remove_problematic_characters(no_hash)
    print(f"  Safe chars: '{no_hash}' -> '{safe_chars}'")
    
    # Step 4: Convert to kebab-case
    kebab = to_kebab_case(safe_chars)
    print(f"  Kebab-case: '{safe_chars}' -> '{kebab}'")
    
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

def scan_csv_files():
    """Scan for all CSV files in the project."""
    csv_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.lower().endswith('.csv'):
                csv_files.append(Path(root) / file)
    return csv_files

def build_csv_mapping():
    """Build mapping of old CSV filenames to new filenames."""
    csv_files = scan_csv_files()
    file_mapping = {}
    existing_names_per_dir = defaultdict(set)
    
    print(f"Found {len(csv_files)} CSV files")
    
    for file_path in csv_files:
        original_filename = file_path.name
        directory = file_path.parent
        
        print(f"\nProcessing: {original_filename}")
        
        # Generate clean filename
        clean_filename = generate_clean_filename(original_filename)
        
        # Handle collisions within the same directory
        dir_key = str(directory)
        final_filename = handle_filename_collision(clean_filename, directory, existing_names_per_dir[dir_key])
        
        # Store mapping
        old_path = str(file_path)
        new_path = str(directory / final_filename)
        
        file_mapping[old_path] = new_path
        
        if original_filename != final_filename:
            print(f"  FINAL: '{original_filename}' -> '{final_filename}'")
        else:
            print(f"  UNCHANGED: '{original_filename}'")
    
    return file_mapping

def update_references_to_csv(file_mapping):
    """Update any references to renamed CSV files in markdown files."""
    # Get all markdown files
    md_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith('.md'):
                md_files.append(Path(root) / file)
    
    updated_count = 0
    old_to_new_filenames = {}
    
    # Build filename mapping (not full paths)
    for old_path, new_path in file_mapping.items():
        old_filename = Path(old_path).name
        new_filename = Path(new_path).name
        if old_filename != new_filename:
            old_to_new_filenames[old_filename] = new_filename
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Update references to CSV files
            for old_filename, new_filename in old_to_new_filenames.items():
                # Look for various ways CSV files might be referenced
                patterns = [
                    re.escape(old_filename),  # Direct filename reference
                    re.escape(old_filename.replace(' ', '%20')),  # URL-encoded reference
                ]
                
                for pattern in patterns:
                    content = re.sub(pattern, new_filename, content, flags=re.IGNORECASE)
            
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated CSV references in: {md_file}")
                updated_count += 1
        
        except Exception as e:
            print(f"Error updating {md_file}: {e}")
    
    print(f"Updated CSV references in {updated_count} files")

def rename_csv_files(file_mapping):
    """Rename CSV files according to the mapping."""
    renamed_count = 0
    
    for old_path, new_path in file_mapping.items():
        if old_path == new_path:
            continue
            
        old_file = Path(old_path)
        new_file = Path(new_path)
        
        if not old_file.exists():
            print(f"Warning: Source file not found: {old_path}")
            continue
        
        if new_file.exists():
            print(f"Warning: Target file already exists: {new_path}")
            continue
        
        try:
            shutil.move(str(old_file), str(new_file))
            print(f"Renamed: {old_file.name} -> {new_file.name}")
            renamed_count += 1
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
    
    print(f"Renamed {renamed_count} CSV files")

def generate_report(file_mapping):
    """Generate a summary report of changes."""
    total_files = len(file_mapping)
    renamed_files = len([1 for old, new in file_mapping.items() if old != new])
    
    print("\n" + "="*60)
    print("CSV FILENAME CLEANUP REPORT")
    print("="*60)
    print(f"Total CSV files processed: {total_files}")
    print(f"Files renamed: {renamed_files}")
    print(f"Files unchanged: {total_files - renamed_files}")
    
    if renamed_files > 0:
        print(f"\nRenamed files:")
        for old_path, new_path in file_mapping.items():
            if old_path != new_path:
                old_name = Path(old_path).name
                new_name = Path(new_path).name
                print(f"  {old_name} -> {new_name}")
    
    print("="*60)

def main():
    print("Starting CSV filename cleanup...")
    print("This will clean up CSV filenames by:")
    print("1. Removing URL encoding")
    print("2. Stripping Notion hash IDs and _all suffixes")
    print("3. Removing filesystem/webserver problematic characters")
    print("4. Converting to kebab-case")
    print("5. Handling filename collisions")
    print("6. Updating references in markdown files")
    print()
    
    # Build file mapping
    file_mapping = build_csv_mapping()
    
    # Rename files
    rename_csv_files(file_mapping)
    
    # Update references
    update_references_to_csv(file_mapping)
    
    # Generate report
    generate_report(file_mapping)
    
    print("CSV filename cleanup complete!")

if __name__ == "__main__":
    main()