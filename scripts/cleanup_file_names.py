#!/usr/bin/env python3
"""
Clean up file names in the DCLT strategic system
- Replace spaces with underscores
- Remove em-dashes and special characters
- Normalize to consistent naming
"""

import os
import re
from pathlib import Path

def clean_filename(filename):
    """Clean up a filename to be system-friendly"""
    # Replace em-dashes and special chars
    cleaned = re.sub(r'[—–]', '-', filename)

    # Replace spaces with underscores
    cleaned = cleaned.replace(' ', '_')

    # Remove or replace other problematic characters
    cleaned = re.sub(r'[🧠]', '', cleaned)  # Remove emoji
    cleaned = re.sub(r'[^\w\-_\.]', '_', cleaned)  # Replace special chars

    # Clean up multiple underscores
    cleaned = re.sub(r'_+', '_', cleaned)

    # Remove leading/trailing underscores
    cleaned = cleaned.strip('_')

    return cleaned

def rename_files_recursive(directory):
    """Recursively rename files in directory"""
    renamed_files = []

    for root, dirs, files in os.walk(directory, topdown=False):
        # Rename files first
        for file in files:
            if ' ' in file or '—' in file or '🧠' in file:
                old_path = os.path.join(root, file)
                new_filename = clean_filename(file)
                new_path = os.path.join(root, new_filename)

                if old_path != new_path:
                    try:
                        os.rename(old_path, new_path)
                        renamed_files.append((old_path, new_path))
                        print(f"Renamed: {file} -> {new_filename}")
                    except Exception as e:
                        print(f"Error renaming {old_path}: {e}")

        # Rename directories
        for dir_name in dirs:
            if ' ' in dir_name or '—' in dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_name = clean_filename(dir_name)
                new_dir_path = os.path.join(root, new_dir_name)

                if old_dir_path != new_dir_path:
                    try:
                        os.rename(old_dir_path, new_dir_path)
                        renamed_files.append((old_dir_path, new_dir_path))
                        print(f"Renamed directory: {dir_name} -> {new_dir_name}")
                    except Exception as e:
                        print(f"Error renaming directory {old_dir_path}: {e}")

    return renamed_files

if __name__ == "__main__":
    projects_dir = "data/dclt/02_EXECUTION/10_Projects"

    print("Cleaning up file and directory names...")
    renamed = rename_files_recursive(projects_dir)

    print(f"\nRenamed {len(renamed)} files/directories total")

    # Save log
    with open("output/cleanup_rename_log.txt", "w") as f:
        f.write("File Rename Log\n")
        f.write("================\n\n")
        for old, new in renamed:
            f.write(f"{old} -> {new}\n")

    print("Rename log saved to output/cleanup_rename_log.txt")