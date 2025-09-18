#!/usr/bin/env python3
"""
Clean Notion ID suffixes from DCLT directory names
Completes the filename cleaning by also handling directory names
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

class NotionDirectoryCleanerDCLT:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.changes = []
        self.stats = {
            'directories_processed': 0,
            'directories_renamed': 0,
            'errors': 0
        }
    
    def identify_notion_id_pattern(self, dirname):
        """Identify and extract Notion ID patterns from directory name"""
        patterns = [
            r'\s+[a-f0-9]{32}$',           # space + 32 char hex
            r'\s+[A-Fa-f0-9]{32}$',       # space + 32 char hex (mixed case)
            r'\s+[a-zA-Z0-9]{32}$',       # space + 32 char alphanumeric
            r'\s+[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',  # UUID format
            r'\s+\w{32}$',                # space + any 32 word chars
            r'_[a-f0-9]{32}$',            # underscore + 32 char hex
            r'-[a-f0-9]{32}$',            # hyphen + 32 char hex
        ]
        
        for pattern in patterns:
            if re.search(pattern, dirname, re.IGNORECASE):
                clean_name = re.sub(pattern, '', dirname, flags=re.IGNORECASE)
                return clean_name.strip()
        
        return None
    
    def scan_directories_with_notion_ids(self):
        """Scan for directories with Notion ID patterns"""
        print("Scanning for directories with Notion ID suffixes...")
        
        dirs_with_ids = []
        
        # Walk through all directories, process deepest first
        for root, dirs, files in os.walk(self.data_dir, topdown=False):
            for dirname in dirs:
                dir_path = Path(root) / dirname
                clean_name = self.identify_notion_id_pattern(dirname)
                
                if clean_name and clean_name != dirname:
                    dirs_with_ids.append({
                        'path': dir_path,
                        'original_name': dirname,
                        'clean_name': clean_name,
                        'parent_dir': Path(root)
                    })
        
        print(f"Found {len(dirs_with_ids)} directories with Notion ID patterns")
        return dirs_with_ids
    
    def rename_directories(self, dirs_to_clean):
        """Rename directories to remove Notion IDs"""
        print("Renaming directories to remove Notion ID suffixes...")
        
        renamed_dirs = []
        
        for dir_info in dirs_to_clean:
            old_path = dir_info['path']
            old_name = dir_info['original_name']
            clean_name = dir_info['clean_name']
            new_path = old_path.parent / clean_name
            
            try:
                # Check if target already exists
                if new_path.exists() and new_path != old_path:
                    print(f"Warning: Target exists, skipping: {clean_name}")
                    continue
                
                # Rename the directory
                old_path.rename(new_path)
                
                renamed_dirs.append({
                    'old_path': str(old_path),
                    'new_path': str(new_path),
                    'old_name': old_name,
                    'new_name': clean_name
                })
                
                self.stats['directories_renamed'] += 1
                print(f"Renamed directory: {old_name} -> {clean_name}")
                
            except Exception as e:
                print(f"Error renaming directory {old_name}: {e}")
                self.stats['errors'] += 1
        
        return renamed_dirs
    
    def clean_all_directories(self):
        """Execute complete directory cleaning process"""
        print("=== DCLT Directory Name Cleaning ===")
        
        # Scan for directories with Notion IDs
        dirs_with_ids = self.scan_directories_with_notion_ids()
        self.stats['directories_processed'] = len(dirs_with_ids)
        
        if not dirs_with_ids:
            print("No directories with Notion ID patterns found!")
            return []
        
        # Rename directories
        renamed_dirs = self.rename_directories(dirs_with_ids)
        
        print(f"\n=== Directory Cleaning Complete ===")
        print(f"Directories renamed: {self.stats['directories_renamed']}")
        print(f"Errors: {self.stats['errors']}")
        
        return renamed_dirs

def main():
    """Main cleaning function"""
    cleaner = NotionDirectoryCleanerDCLT()
    result = cleaner.clean_all_directories()
    
    if result:
        print(f"\n✅ Directory cleaning complete!")
        print(f"📁 Clean directory names now in: data/dclt/")
    else:
        print(f"\n✨ No Notion IDs found in directory names!")

if __name__ == '__main__':
    main()