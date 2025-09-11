#!/usr/bin/env python3
"""
Analyze Notion export files for DCLT strategic planning system
"""
import os
import re
from pathlib import Path
from collections import defaultdict
import json

def extract_hash_id(filename):
    """Extract hash ID from filename if present"""
    match = re.search(r'\s([a-f0-9]{32})\.(md|csv)$', filename)
    return match.group(1) if match else None

def clean_filename(filename):
    """Clean filename by removing hash ID and emojis"""
    # Remove hash ID
    cleaned = re.sub(r'\s[a-f0-9]{32}\.(md|csv)$', r'.\1', filename)
    # Remove emojis at start of name
    cleaned = re.sub(r'^[^\w\s-]+\s*', '', cleaned)
    # Clean up spaces and special chars
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def analyze_content_for_category(filepath):
    """Analyze file content to determine appropriate category"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        # Strategy indicators
        strategy_keywords = [
            'strategic', 'strategy', 'plan', 'goals', 'objectives', 
            'mission', 'vision', 'values', 'roadmap', 'framework',
            'alignment', 'initiative', 'priorities'
        ]
        
        # Execution indicators  
        execution_keywords = [
            'campaign', 'brand', 'website', 'content', 'marketing',
            'execution', 'implementation', 'task', 'project',
            'deliverable', 'timeline', 'milestone', 'progress'
        ]
        
        # Reference indicators
        reference_keywords = [
            'research', 'analysis', 'data', 'metrics', 'insights',
            'reference', 'tools', 'templates', 'examples',
            'lessons learned', 'best practices'
        ]
        
        strategy_score = sum(1 for kw in strategy_keywords if kw in content)
        execution_score = sum(1 for kw in execution_keywords if kw in content)
        reference_score = sum(1 for kw in reference_keywords if kw in content)
        
        if strategy_score >= execution_score and strategy_score >= reference_score:
            return 'strategy'
        elif execution_score >= reference_score:
            return 'execution'
        else:
            return 'reference'
            
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}")
        return 'unknown'

def main():
    """Main analysis function"""
    data_dir = Path('data')
    
    # Find all markdown files
    md_files = list(data_dir.rglob('*.md'))
    csv_files = list(data_dir.rglob('*.csv'))
    
    print(f"Found {len(md_files)} markdown files and {len(csv_files)} CSV files")
    
    # Analyze file patterns
    file_analysis = {
        'total_files': len(md_files) + len(csv_files),
        'markdown_files': len(md_files),
        'csv_files': len(csv_files),
        'files_with_hashes': 0,
        'files_with_emojis': 0,
        'category_distribution': defaultdict(int),
        'current_structure': defaultdict(list),
        'files_to_process': []
    }
    
    for filepath in md_files + csv_files:
        filename = filepath.name
        relative_path = str(filepath.relative_to(data_dir))
        
        # Check for hash IDs
        if extract_hash_id(filename):
            file_analysis['files_with_hashes'] += 1
            
        # Check for emojis
        if re.match(r'^[^\w\s-]', filename):
            file_analysis['files_with_emojis'] += 1
            
        # Categorize content (only for MD files)
        if filepath.suffix == '.md':
            category = analyze_content_for_category(filepath)
            file_analysis['category_distribution'][category] += 1
        
        # Track current structure
        current_dir = '/'.join(relative_path.split('/')[:-1]) if '/' in relative_path else 'root'
        file_analysis['current_structure'][current_dir].append(filename)
        
        # Add to processing list
        clean_name = clean_filename(filename)
        file_analysis['files_to_process'].append({
            'original_path': str(filepath),
            'original_name': filename,
            'clean_name': clean_name,
            'category': category if filepath.suffix == '.md' else 'data',
            'has_hash': bool(extract_hash_id(filename)),
            'has_emoji': bool(re.match(r'^[^\w\s-]', filename))
        })
    
    # Generate report
    print("\n=== NOTION EXPORT ANALYSIS ===")
    print(f"Total files: {file_analysis['total_files']}")
    print(f"Files with hash IDs: {file_analysis['files_with_hashes']}")
    print(f"Files with emojis: {file_analysis['files_with_emojis']}")
    print(f"\nCategory distribution:")
    for category, count in file_analysis['category_distribution'].items():
        print(f"  {category}: {count}")
    
    print(f"\nCurrent directory structure:")
    for directory, files in sorted(file_analysis['current_structure'].items()):
        print(f"  {directory}: {len(files)} files")
    
    # Save detailed analysis
    os.makedirs('output/reports', exist_ok=True)
    with open('output/reports/notion_export_analysis.json', 'w') as f:
        json.dump(file_analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed analysis saved to output/reports/notion_export_analysis.json")

if __name__ == '__main__':
    main()