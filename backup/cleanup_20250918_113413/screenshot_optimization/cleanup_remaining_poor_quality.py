#!/usr/bin/env python3
"""
Additional cleanup for remaining poor-quality screenshots
Targets files that should have been deleted but weren't caught in the first pass
"""

import os
from pathlib import Path
import shutil
from datetime import datetime

def identify_additional_poor_quality_files():
    """Find remaining files that should be deleted based on size and content indicators"""
    screenshots_dir = Path('data/landtrusts/datasets/screens/screenshots')
    
    if not screenshots_dir.exists():
        print(f"Directory not found: {screenshots_dir}")
        return []
    
    poor_quality_files = []
    
    # Get all PNG files with their sizes
    for png_file in screenshots_dir.glob('*.png'):
        file_size = png_file.stat().st_size
        file_size_kb = file_size / 1024
        
        # Flag files under 100KB as likely poor quality
        if file_size_kb < 100:
            reason = "Very small file size (likely error/incomplete page)"
            poor_quality_files.append({
                'path': png_file,
                'size_kb': round(file_size_kb, 1),
                'reason': reason
            })
    
    return poor_quality_files

def create_additional_backup(files_to_delete):
    """Create backup of files before deletion"""
    backup_dir = Path('additional_cleanup_backup')
    backup_dir.mkdir(exist_ok=True)
    
    for file_info in files_to_delete:
        file_path = file_info['path']
        backup_path = backup_dir / file_path.name
        
        # Handle name conflicts
        counter = 1
        original_backup_path = backup_path
        while backup_path.exists():
            name_parts = original_backup_path.stem, original_backup_path.suffix
            backup_path = backup_dir / f"{name_parts[0]}_backup_{counter}{name_parts[1]}"
            counter += 1
        
        shutil.copy2(file_path, backup_path)
        print(f"Backed up: {file_path.name} -> {backup_path.name}")

def main():
    """Main cleanup function"""
    print("Identifying Additional Poor Quality Screenshots")
    print("=" * 50)
    
    # Find problematic files
    poor_quality_files = identify_additional_poor_quality_files()
    
    if not poor_quality_files:
        print("✅ No additional poor quality files found!")
        return
    
    print(f"Found {len(poor_quality_files)} additional poor quality files:\n")
    
    # Display files to be deleted
    for file_info in poor_quality_files:
        print(f"DELETE: {file_info['path'].name} ({file_info['size_kb']} KB) - {file_info['reason']}")
    
    print(f"\nTotal storage to be freed: {sum(f['size_kb'] for f in poor_quality_files):.1f} KB")
    
    # Ask for confirmation
    print(f"\nProceed with deleting these {len(poor_quality_files)} files? (y/N): ", end="")
    response = input().strip().lower()
    
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Create backups
    print("\nCreating backups...")
    create_additional_backup(poor_quality_files)
    
    # Delete files
    print("\nDeleting poor quality files...")
    deleted_count = 0
    total_size_freed = 0
    
    for file_info in poor_quality_files:
        try:
            file_path = file_info['path']
            file_path.unlink()
            print(f"✅ DELETED: {file_path.name}")
            deleted_count += 1
            total_size_freed += file_info['size_kb']
        except Exception as e:
            print(f"❌ Error deleting {file_path.name}: {e}")
    
    print(f"\n=== Cleanup Complete ===")
    print(f"Files deleted: {deleted_count}")
    print(f"Storage freed: {total_size_freed:.1f} KB ({total_size_freed/1024:.1f} MB)")
    print(f"Backups saved to: additional_cleanup_backup/")
    
    # Final count
    remaining_files = len(list(Path('data/landtrusts/datasets/screens/screenshots').glob('*.png')))
    print(f"Screenshots remaining: {remaining_files}")

if __name__ == '__main__':
    main()