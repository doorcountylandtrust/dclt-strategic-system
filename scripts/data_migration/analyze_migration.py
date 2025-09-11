#!/usr/bin/env python3
"""
DCLT Strategic System Migration Analysis

This script performs comprehensive analysis comparing a cleaned Notion export 
against existing files in the DCLT Strategic System and creates a detailed migration plan.
"""

import os
import re
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import difflib
import json


def calculate_file_hash(file_path):
    """Calculate MD5 hash of file content for comparison."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return hashlib.md5(content.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    if content.startswith('---\n'):
        end_marker = content.find('\n---\n', 4)
        if end_marker != -1:
            frontmatter = content[4:end_marker]
            body = content[end_marker + 5:]
            return frontmatter, body
    return None, content


def get_file_metadata(file_path):
    """Get comprehensive metadata for a file."""
    try:
        stat = file_path.stat()
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, body = extract_frontmatter(content)
        
        # Calculate various metrics
        word_count = len(body.split())
        line_count = len(body.splitlines())
        char_count = len(body)
        
        # Extract key phrases (first 100 words)
        key_phrases = ' '.join(body.split()[:100])
        
        return {
            'path': str(file_path),
            'name': file_path.name,
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'content_hash': calculate_file_hash(file_path),
            'frontmatter': frontmatter,
            'body': body,
            'word_count': word_count,
            'line_count': line_count,
            'char_count': char_count,
            'key_phrases': key_phrases,
            'has_frontmatter': frontmatter is not None
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return None


def scan_directory_files(directory):
    """Scan directory for all markdown files and return metadata."""
    files_data = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                metadata = get_file_metadata(file_path)
                if metadata:
                    relative_path = file_path.relative_to(directory)
                    files_data[str(relative_path)] = metadata
    
    return files_data


def calculate_similarity(text1, text2):
    """Calculate text similarity using SequenceMatcher."""
    return difflib.SequenceMatcher(None, text1, text2).ratio()


def find_potential_matches(new_file, existing_files, threshold=0.3):
    """Find potential matches for a new file in existing files."""
    matches = []
    
    for existing_path, existing_data in existing_files.items():
        # Compare by filename similarity
        name_similarity = calculate_similarity(
            new_file['name'].lower(), 
            existing_data['name'].lower()
        )
        
        # Compare by content similarity (key phrases)
        content_similarity = calculate_similarity(
            new_file['key_phrases'].lower(),
            existing_data['key_phrases'].lower()
        )
        
        # Calculate overall similarity
        overall_similarity = (name_similarity * 0.3) + (content_similarity * 0.7)
        
        if overall_similarity >= threshold:
            matches.append({
                'path': existing_path,
                'data': existing_data,
                'name_similarity': name_similarity,
                'content_similarity': content_similarity,
                'overall_similarity': overall_similarity
            })
    
    # Sort by overall similarity (highest first)
    matches.sort(key=lambda x: x['overall_similarity'], reverse=True)
    return matches


def classify_files(notion_files, existing_files):
    """Classify files into categories: New, Updated, Unchanged, Obsolete."""
    classification = {
        'new_files': [],
        'updated_files': [],
        'unchanged_files': [],
        'obsolete_files': [],
        'matched_pairs': {}
    }
    
    processed_existing = set()
    
    for notion_path, notion_data in notion_files.items():
        matches = find_potential_matches(notion_data, existing_files)
        
        if not matches:
            # No matches found - this is a new file
            classification['new_files'].append({
                'path': notion_path,
                'data': notion_data
            })
        else:
            best_match = matches[0]
            existing_path = best_match['path']
            existing_data = best_match['data']
            
            # Mark this existing file as processed
            processed_existing.add(existing_path)
            
            # Store the match
            classification['matched_pairs'][notion_path] = existing_path
            
            # Check if files are essentially the same
            if notion_data['content_hash'] == existing_data['content_hash']:
                classification['unchanged_files'].append({
                    'notion_path': notion_path,
                    'existing_path': existing_path,
                    'notion_data': notion_data,
                    'existing_data': existing_data,
                    'similarity': best_match['overall_similarity']
                })
            else:
                # Content differs - this is an update
                classification['updated_files'].append({
                    'notion_path': notion_path,
                    'existing_path': existing_path,
                    'notion_data': notion_data,
                    'existing_data': existing_data,
                    'similarity': best_match['overall_similarity'],
                    'word_count_change': notion_data['word_count'] - existing_data['word_count'],
                    'char_count_change': notion_data['char_count'] - existing_data['char_count']
                })
    
    # Find obsolete files (existing files that weren't matched)
    for existing_path, existing_data in existing_files.items():
        if existing_path not in processed_existing:
            classification['obsolete_files'].append({
                'path': existing_path,
                'data': existing_data
            })
    
    return classification


def analyze_frontmatter_strategy(notion_files, existing_files, classification):
    """Analyze frontmatter patterns and suggest strategy."""
    frontmatter_analysis = {
        'existing_with_frontmatter': 0,
        'existing_without_frontmatter': 0,
        'notion_with_frontmatter': 0,
        'notion_without_frontmatter': 0,
        'common_frontmatter_fields': defaultdict(int),
        'recommendations': []
    }
    
    # Analyze existing files
    for data in existing_files.values():
        if data['has_frontmatter']:
            frontmatter_analysis['existing_with_frontmatter'] += 1
            # Parse frontmatter fields (simplified)
            if data['frontmatter']:
                lines = data['frontmatter'].split('\n')
                for line in lines:
                    if ':' in line:
                        field = line.split(':')[0].strip()
                        frontmatter_analysis['common_frontmatter_fields'][field] += 1
        else:
            frontmatter_analysis['existing_without_frontmatter'] += 1
    
    # Analyze notion files
    for data in notion_files.values():
        if data['has_frontmatter']:
            frontmatter_analysis['notion_with_frontmatter'] += 1
        else:
            frontmatter_analysis['notion_without_frontmatter'] += 1
    
    # Generate recommendations
    total_existing = len(existing_files)
    if frontmatter_analysis['existing_with_frontmatter'] > total_existing * 0.5:
        frontmatter_analysis['recommendations'].append(
            "Preserve existing frontmatter for updated files"
        )
        frontmatter_analysis['recommendations'].append(
            "Add minimal frontmatter to new files based on common patterns"
        )
    else:
        frontmatter_analysis['recommendations'].append(
            "Frontmatter usage is inconsistent - consider standardizing"
        )
    
    return frontmatter_analysis


def generate_migration_report(classification, frontmatter_analysis, notion_files, existing_files):
    """Generate comprehensive migration report."""
    report = []
    
    # Header
    report.append("# DCLT Strategic System - Notion Migration Analysis")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append(f"- **Total Notion Files**: {len(notion_files)}")
    report.append(f"- **Total Existing Files**: {len(existing_files)}")
    report.append(f"- **New Files**: {len(classification['new_files'])}")
    report.append(f"- **Updated Files**: {len(classification['updated_files'])}")
    report.append(f"- **Unchanged Files**: {len(classification['unchanged_files'])}")
    report.append(f"- **Obsolete Files**: {len(classification['obsolete_files'])}")
    report.append("")
    
    # New Files Section
    if classification['new_files']:
        report.append("## New Files (Not in Current System)")
        report.append("")
        report.append("These files are completely new and should be added to the system:")
        report.append("")
        
        for item in classification['new_files']:
            file_data = item['data']
            report.append(f"### `{item['path']}`")
            report.append(f"- **Word Count**: {file_data['word_count']}")
            report.append(f"- **Has Frontmatter**: {file_data['has_frontmatter']}")
            if file_data['key_phrases']:
                preview = file_data['key_phrases'][:100] + "..." if len(file_data['key_phrases']) > 100 else file_data['key_phrases']
                report.append(f"- **Content Preview**: {preview}")
            report.append("")
    
    # Updated Files Section
    if classification['updated_files']:
        report.append("## Updated Files (Content Changes)")
        report.append("")
        report.append("These files have content changes and should be reviewed for updates:")
        report.append("")
        
        for item in classification['updated_files']:
            notion_data = item['notion_data']
            existing_data = item['existing_data']
            report.append(f"### `{item['notion_path']}` → `{item['existing_path']}`")
            report.append(f"- **Similarity**: {item['similarity']:.2%}")
            report.append(f"- **Word Count Change**: {item['word_count_change']:+d}")
            report.append(f"- **Existing Has Frontmatter**: {existing_data['has_frontmatter']}")
            report.append(f"- **Notion Has Frontmatter**: {notion_data['has_frontmatter']}")
            if existing_data['has_frontmatter'] and not notion_data['has_frontmatter']:
                report.append("- **⚠️ Action**: Preserve existing frontmatter when updating")
            report.append("")
    
    # Unchanged Files Section
    if classification['unchanged_files']:
        report.append("## Unchanged Files (Identical Content)")
        report.append("")
        report.append("These files appear to be identical and require no action:")
        report.append("")
        
        for item in classification['unchanged_files']:
            report.append(f"- `{item['notion_path']}` → `{item['existing_path']}` (similarity: {item['similarity']:.2%})")
        report.append("")
    
    # Obsolete Files Section
    if classification['obsolete_files']:
        report.append("## Obsolete Files (Not in Notion Export)")
        report.append("")
        report.append("These files exist in the current system but not in the new Notion export:")
        report.append("")
        
        for item in classification['obsolete_files']:
            file_data = item['data']
            report.append(f"### `{item['path']}`")
            report.append(f"- **Last Modified**: {file_data['modified'].strftime('%Y-%m-%d')}")
            report.append(f"- **Word Count**: {file_data['word_count']}")
            report.append(f"- **Has Frontmatter**: {file_data['has_frontmatter']}")
            report.append("- **⚠️ Review**: Determine if this content should be preserved or archived")
            report.append("")
    
    # Frontmatter Strategy Section
    report.append("## Frontmatter Strategy")
    report.append("")
    report.append(f"- **Existing files with frontmatter**: {frontmatter_analysis['existing_with_frontmatter']}")
    report.append(f"- **Existing files without frontmatter**: {frontmatter_analysis['existing_without_frontmatter']}")
    report.append(f"- **Notion files with frontmatter**: {frontmatter_analysis['notion_with_frontmatter']}")
    report.append(f"- **Notion files without frontmatter**: {frontmatter_analysis['notion_without_frontmatter']}")
    report.append("")
    
    if frontmatter_analysis['common_frontmatter_fields']:
        report.append("### Common Frontmatter Fields")
        for field, count in sorted(frontmatter_analysis['common_frontmatter_fields'].items(), key=lambda x: x[1], reverse=True):
            report.append(f"- `{field}`: {count} files")
        report.append("")
    
    report.append("### Recommendations")
    for rec in frontmatter_analysis['recommendations']:
        report.append(f"- {rec}")
    report.append("")
    
    # Migration Steps Section
    report.append("## Migration Implementation Steps")
    report.append("")
    report.append("1. **Backup Current System**")
    report.append("   - Create backup of entire data/ directory")
    report.append("   - Document current state")
    report.append("")
    
    report.append("2. **Add New Files**")
    if classification['new_files']:
        report.append(f"   - Copy {len(classification['new_files'])} new files to appropriate locations")
        report.append("   - Add frontmatter where needed based on content analysis")
    else:
        report.append("   - No new files to add")
    report.append("")
    
    report.append("3. **Update Modified Files**")
    if classification['updated_files']:
        report.append(f"   - Review and update {len(classification['updated_files'])} modified files")
        report.append("   - Preserve existing frontmatter where present")
        report.append("   - Check for strategic planning impact of changes")
    else:
        report.append("   - No files require content updates")
    report.append("")
    
    report.append("4. **Handle Obsolete Files**")
    if classification['obsolete_files']:
        report.append(f"   - Review {len(classification['obsolete_files'])} obsolete files")
        report.append("   - Archive or preserve files with strategic value")
        report.append("   - Remove files that are no longer relevant")
    else:
        report.append("   - No obsolete files to handle")
    report.append("")
    
    report.append("5. **Quality Assurance**")
    report.append("   - Validate all internal links")
    report.append("   - Check folder structure relationships")
    report.append("   - Ensure no critical content is lost")
    report.append("")
    
    # Statistics Section
    report.append("## Statistics")
    report.append("")
    
    total_files = len(notion_files)
    if total_files > 0:
        new_pct = len(classification['new_files']) / total_files * 100
        updated_pct = len(classification['updated_files']) / total_files * 100
        unchanged_pct = len(classification['unchanged_files']) / total_files * 100
        
        report.append(f"- **New content**: {new_pct:.1f}% of files")
        report.append(f"- **Modified content**: {updated_pct:.1f}% of files")
        report.append(f"- **Unchanged content**: {unchanged_pct:.1f}% of files")
    
    if classification['obsolete_files']:
        obsolete_pct = len(classification['obsolete_files']) / len(existing_files) * 100
        report.append(f"- **Obsolete content**: {obsolete_pct:.1f}% of existing files")
    
    report.append("")
    report.append("---")
    report.append("*Generated by DCLT Strategic System Migration Analysis Tool*")
    
    return "\n".join(report)


def main():
    # Define paths
    notion_dir = Path("input/notion-export-latest")
    existing_dir = Path("data")
    output_dir = Path("output/reports")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("DCLT Strategic System Migration Analysis")
    print("=" * 50)
    
    # Scan files
    print("Scanning Notion export files...")
    notion_files = scan_directory_files(notion_dir)
    print(f"Found {len(notion_files)} Notion files")
    
    print("Scanning existing system files...")
    existing_files = scan_directory_files(existing_dir)
    print(f"Found {len(existing_files)} existing files")
    
    # Perform classification
    print("Classifying files...")
    classification = classify_files(notion_files, existing_files)
    
    # Analyze frontmatter
    print("Analyzing frontmatter strategy...")
    frontmatter_analysis = analyze_frontmatter_strategy(notion_files, existing_files, classification)
    
    # Generate report
    print("Generating migration report...")
    report = generate_migration_report(classification, frontmatter_analysis, notion_files, existing_files)
    
    # Write report
    report_path = output_dir / "notion_migration_analysis.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Migration report generated: {report_path}")
    
    # Print summary
    print("\nSummary:")
    print(f"- New files: {len(classification['new_files'])}")
    print(f"- Updated files: {len(classification['updated_files'])}")
    print(f"- Unchanged files: {len(classification['unchanged_files'])}")
    print(f"- Obsolete files: {len(classification['obsolete_files'])}")


if __name__ == "__main__":
    main()