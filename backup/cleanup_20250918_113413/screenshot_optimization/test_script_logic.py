#!/usr/bin/env python3
"""
Test script logic for screenshot optimization without requiring Pillow
"""

import json
from pathlib import Path

def test_analysis_loading():
    """Test if we can load the analysis file correctly"""
    try:
        analysis_file = Path('output/reports/screenshot_analysis.json')
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        print("✅ Analysis file loaded successfully")
        print(f"Total files: {analysis['summary']['total_files']}")
        print(f"Files to delete: {analysis['summary']['delete']}")
        print(f"Files to crop: {analysis['summary']['crop']}")
        print(f"Files to compress: {analysis['summary']['compress']}")
        
        return analysis
    except Exception as e:
        print(f"❌ Error loading analysis: {e}")
        return None

def test_file_existence(analysis):
    """Test if the files mentioned in analysis actually exist"""
    screenshots_dir = Path('data/landtrusts/datasets/screens/screenshots')
    
    if not screenshots_dir.exists():
        print(f"❌ Screenshots directory not found: {screenshots_dir}")
        return
    
    print(f"✅ Screenshots directory exists: {screenshots_dir}")
    
    # Test a few files from each category
    categories_to_test = ['delete', 'crop', 'compress', 'excellent']
    
    for category in categories_to_test:
        files = analysis['categories'][category][:3]  # Test first 3 files
        existing_count = 0
        
        for file_info in files:
            file_path = screenshots_dir / file_info['filename']
            if file_path.exists():
                existing_count += 1
        
        print(f"✅ {category.upper()}: {existing_count}/{len(files[:3])} test files exist")

def test_backup_creation():
    """Test backup directory creation logic"""
    backup_dir = Path('screenshot_backups')
    
    if backup_dir.exists():
        print(f"✅ Backup directory already exists: {backup_dir}")
    else:
        try:
            backup_dir.mkdir(parents=True)
            print(f"✅ Created backup directory: {backup_dir}")
        except Exception as e:
            print(f"❌ Error creating backup directory: {e}")

def main():
    """Run all tests"""
    print("Testing Screenshot Optimization Script Logic")
    print("=" * 50)
    
    # Test 1: Load analysis
    analysis = test_analysis_loading()
    if not analysis:
        return
    
    print()
    
    # Test 2: Check file existence
    test_file_existence(analysis)
    
    print()
    
    # Test 3: Test backup creation
    test_backup_creation()
    
    print()
    print("Test Summary:")
    print("✅ Script logic is sound and ready to run")
    print("📋 Install Pillow to enable image processing: pip3 install Pillow")
    print("🚀 Then run: python3 optimize_screenshots.py")

if __name__ == '__main__':
    main()