#!/usr/bin/env python3
"""
Quality Check for DCLT Migration

Performs final quality analysis including link validation and structural checks.
"""

import os
import re
from pathlib import Path
from collections import defaultdict


def extract_markdown_links(content):
    """Extract all markdown links from content."""
    # Pattern for markdown links: [text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, content)


def validate_internal_links(file_path, content, all_files):
    """Validate internal markdown links in a file."""
    links = extract_markdown_links(content)
    issues = []
    
    for link_text, link_url in links:
        # Skip external links
        if link_url.startswith(('http://', 'https://', 'mailto:')):
            continue
        
        # Skip anchor links
        if link_url.startswith('#'):
            continue
        
        # Decode URL encoding
        import urllib.parse
        decoded_url = urllib.parse.unquote(link_url)
        
        # Check if the linked file exists
        if decoded_url.endswith('.md'):
            # Try to find the file
            found = False
            
            # Check relative to current file
            current_dir = file_path.parent
            target_path = current_dir / decoded_url
            
            if target_path.name in all_files:
                found = True
            else:
                # Check if any file matches the name
                target_name = Path(decoded_url).name
                if target_name in all_files:
                    found = True
            
            if not found:
                issues.append({
                    'type': 'broken_link',
                    'text': link_text,
                    'url': link_url,
                    'decoded_url': decoded_url
                })
    
    return issues


def analyze_structure(notion_dir):
    """Analyze the structure and organization of files."""
    structure_analysis = {
        'total_files': 0,
        'total_directories': 0,
        'depth_distribution': defaultdict(int),
        'file_type_distribution': defaultdict(int),
        'largest_files': [],
        'orphaned_files': [],
        'link_issues': []
    }
    
    all_files = set()
    
    # First pass: collect all file names
    for root, dirs, files in os.walk(notion_dir):
        for file in files:
            if file.endswith('.md'):
                all_files.add(file)
    
    # Second pass: analyze structure and links
    for root, dirs, files in os.walk(notion_dir):
        root_path = Path(root)
        depth = len(root_path.relative_to(notion_dir).parts)
        
        structure_analysis['depth_distribution'][depth] += len(files)
        structure_analysis['total_directories'] += len(dirs)
        
        for file in files:
            if file.endswith('.md'):
                file_path = root_path / file
                structure_analysis['total_files'] += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check file size
                    word_count = len(content.split())
                    structure_analysis['largest_files'].append({
                        'path': str(file_path.relative_to(notion_dir)),
                        'word_count': word_count,
                        'size': len(content)
                    })
                    
                    # Check for link issues
                    link_issues = validate_internal_links(file_path, content, all_files)
                    if link_issues:
                        structure_analysis['link_issues'].extend([
                            {
                                'file': str(file_path.relative_to(notion_dir)),
                                **issue
                            } for issue in link_issues
                        ])
                
                except Exception as e:
                    print(f"Error analyzing {file_path}: {e}")
    
    # Sort largest files
    structure_analysis['largest_files'].sort(key=lambda x: x['word_count'], reverse=True)
    structure_analysis['largest_files'] = structure_analysis['largest_files'][:10]
    
    return structure_analysis


def generate_quality_report(structure_analysis):
    """Generate quality analysis report."""
    report = []
    
    report.append("# Quality Analysis Report - Notion Export")
    report.append("")
    
    # Structure Analysis
    report.append("## Structure Analysis")
    report.append("")
    report.append(f"- **Total Files**: {structure_analysis['total_files']}")
    report.append(f"- **Total Directories**: {structure_analysis['total_directories']}")
    report.append("")
    
    report.append("### Directory Depth Distribution")
    for depth, count in sorted(structure_analysis['depth_distribution'].items()):
        report.append(f"- **Depth {depth}**: {count} files")
    report.append("")
    
    # Largest Files
    if structure_analysis['largest_files']:
        report.append("### Largest Files (Top 10)")
        for file_info in structure_analysis['largest_files']:
            report.append(f"- `{file_info['path']}`: {file_info['word_count']} words")
        report.append("")
    
    # Link Issues
    if structure_analysis['link_issues']:
        report.append("## Link Validation Issues")
        report.append("")
        report.append(f"Found {len(structure_analysis['link_issues'])} broken internal links:")
        report.append("")
        
        for issue in structure_analysis['link_issues'][:20]:  # Show first 20
            report.append(f"### `{issue['file']}`")
            report.append(f"- **Broken Link**: `{issue['text']}` → `{issue['url']}`")
            report.append(f"- **Decoded URL**: `{issue['decoded_url']}`")
            report.append("")
        
        if len(structure_analysis['link_issues']) > 20:
            report.append(f"... and {len(structure_analysis['link_issues']) - 20} more issues")
            report.append("")
    else:
        report.append("## Link Validation")
        report.append("")
        report.append("✅ No broken internal links found!")
        report.append("")
    
    # Recommendations
    report.append("## Quality Recommendations")
    report.append("")
    
    if structure_analysis['link_issues']:
        report.append("1. **Fix Broken Links**: Update internal links to use cleaned filenames")
        report.append("2. **Link Validation**: Implement automated link checking in the future")
    else:
        report.append("1. **Links**: All internal links appear to be valid")
    
    if structure_analysis['depth_distribution'].get(0, 0) > 0:
        report.append("3. **Structure**: Some files are at root level - consider organizing into subdirectories")
    
    if any(file_info['word_count'] > 5000 for file_info in structure_analysis['largest_files']):
        report.append("4. **Large Files**: Consider breaking down very large files for better navigation")
    
    report.append("5. **Consistency**: Ensure consistent frontmatter across similar file types")
    report.append("")
    
    return "\n".join(report)


def main():
    notion_dir = Path("input/notion-export-latest")
    output_dir = Path("output/reports")
    
    print("Performing quality analysis...")
    
    # Analyze structure
    structure_analysis = analyze_structure(notion_dir)
    
    # Generate report
    quality_report = generate_quality_report(structure_analysis)
    
    # Append to existing migration report
    migration_report_path = output_dir / "notion_migration_analysis.md"
    
    with open(migration_report_path, 'a', encoding='utf-8') as f:
        f.write("\n\n")
        f.write(quality_report)
    
    print(f"Quality analysis appended to: {migration_report_path}")
    print(f"Found {len(structure_analysis['link_issues'])} link issues")


if __name__ == "__main__":
    main()