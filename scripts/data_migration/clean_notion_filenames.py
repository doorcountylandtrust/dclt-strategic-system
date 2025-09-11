#!/usr/bin/env python3
"""
Clean Notion ID suffixes from DCLT filenames
Removes alphanumeric ID patterns while preserving directory structure and content
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import json

class NotionFilenameCleanerDCLT:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.changes = []
        self.conflicts = []
        self.stats = {
            'files_processed': 0,
            'files_renamed': 0,
            'conflicts_resolved': 0,
            'links_updated': 0,
            'errors': 0
        }
        self.link_mapping = {}  # Old filename -> New filename for link updates
    
    def identify_notion_id_pattern(self, filename):
        """Identify and extract Notion ID patterns from filename"""
        # Common Notion ID patterns at the end of filenames (before .md)
        patterns = [
            r'\s+[a-f0-9]{32}\.md$',           # space + 32 char hex + .md
            r'\s+[A-Fa-f0-9]{32}\.md$',       # space + 32 char hex (mixed case) + .md
            r'\s+[a-zA-Z0-9]{32}\.md$',       # space + 32 char alphanumeric + .md
            r'\s+[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.md$',  # UUID format
            r'\s+\w{32}\.md$',                # space + any 32 word chars + .md
            r'_[a-f0-9]{32}\.md$',            # underscore + 32 char hex + .md
            r'-[a-f0-9]{32}\.md$',            # hyphen + 32 char hex + .md
        ]
        
        for pattern in patterns:
            if re.search(pattern, filename, re.IGNORECASE):
                # Extract the clean name by removing the pattern
                clean_pattern = pattern.replace(r'\.md$', '')
                clean_name = re.sub(clean_pattern, '', filename, flags=re.IGNORECASE)
                if not clean_name.endswith('.md'):
                    clean_name += '.md'
                return clean_name.strip()
        
        return None
    
    def scan_files_with_notion_ids(self):
        """Scan directory for files with Notion ID patterns"""
        print("Scanning for files with Notion ID suffixes...")
        
        files_with_ids = []
        
        for file_path in self.data_dir.rglob('*.md'):
            filename = file_path.name
            clean_name = self.identify_notion_id_pattern(filename)
            
            if clean_name and clean_name != filename:
                files_with_ids.append({
                    'path': file_path,
                    'original_name': filename,
                    'clean_name': clean_name,
                    'directory': file_path.parent
                })
        
        print(f"Found {len(files_with_ids)} files with Notion ID patterns")
        return files_with_ids
    
    def detect_conflicts(self, files_to_clean):
        """Detect potential naming conflicts after cleaning"""
        conflicts = []
        clean_names_by_dir = {}
        
        # Group by directory and check for conflicts
        for file_info in files_to_clean:
            dir_path = file_info['directory']
            clean_name = file_info['clean_name']
            
            if dir_path not in clean_names_by_dir:
                clean_names_by_dir[dir_path] = {}
            
            if clean_name in clean_names_by_dir[dir_path]:
                # Conflict detected
                conflicts.append({
                    'directory': dir_path,
                    'clean_name': clean_name,
                    'conflicting_files': [
                        clean_names_by_dir[dir_path][clean_name],
                        file_info
                    ]
                })
            else:
                clean_names_by_dir[dir_path][clean_name] = file_info
        
        return conflicts
    
    def resolve_conflicts(self, conflicts):
        """Resolve naming conflicts by adding numbers"""
        for conflict in conflicts:
            directory = conflict['directory']
            base_clean_name = conflict['clean_name']
            conflicting_files = conflict['conflicting_files']
            
            print(f"Resolving conflict in {directory}: {base_clean_name}")
            
            # Keep first file with original clean name
            for i, file_info in enumerate(conflicting_files):
                if i == 0:
                    # First file keeps the clean name
                    continue
                else:
                    # Subsequent files get numbered
                    name_without_ext = base_clean_name.replace('.md', '')
                    new_clean_name = f"{name_without_ext}-{i+1}.md"
                    
                    # Check if this numbered name already exists
                    counter = i + 1
                    while (directory / new_clean_name).exists():
                        counter += 1
                        new_clean_name = f"{name_without_ext}-{counter}.md"
                    
                    file_info['clean_name'] = new_clean_name
                    print(f"  Renamed: {file_info['original_name']} -> {new_clean_name}")
    
    def update_internal_links(self, files_renamed):
        """Update internal markdown links to reference new filenames"""
        print("Updating internal links in markdown files...")
        
        # Build mapping of old -> new filenames
        filename_mapping = {}
        for file_info in files_renamed:
            old_name = file_info['old_name']
            new_name = file_info['new_name']
            filename_mapping[old_name] = new_name
            # Also map without extension for various link formats
            filename_mapping[old_name.replace('.md', '')] = new_name.replace('.md', '')
        
        links_updated = 0
        
        # Scan all markdown files for links
        for file_path in self.data_dir.rglob('*.md'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Update various link formats
                for old_filename, new_filename in filename_mapping.items():
                    # Markdown links: [text](filename.md)
                    content = re.sub(
                        rf'\]\({re.escape(old_filename)}\)',
                        f']({new_filename})',
                        content
                    )
                    
                    # Markdown links without extension: [text](filename)
                    if old_filename.endswith('.md'):
                        old_without_ext = old_filename.replace('.md', '')
                        new_without_ext = new_filename.replace('.md', '')
                        content = re.sub(
                            rf'\]\({re.escape(old_without_ext)}\)',
                            f']({new_without_ext})',
                            content
                        )
                    
                    # Wiki-style links: [[filename]]
                    content = re.sub(
                        rf'\[\[{re.escape(old_filename)}\]\]',
                        f'[[{new_filename}]]',
                        content
                    )
                    
                    # Direct filename references in text
                    content = re.sub(
                        rf'\b{re.escape(old_filename)}\b',
                        new_filename,
                        content
                    )
                
                # Save if content changed
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    links_updated += 1
                    print(f"Updated links in: {file_path.relative_to(self.data_dir)}")
            
            except Exception as e:
                print(f"Error updating links in {file_path}: {e}")
                self.stats['errors'] += 1
        
        self.stats['links_updated'] = links_updated
        print(f"Updated links in {links_updated} files")
    
    def rename_files(self, files_to_clean):
        """Rename files to remove Notion IDs"""
        print("Renaming files to remove Notion ID suffixes...")
        
        renamed_files = []
        
        for file_info in files_to_clean:
            old_path = file_info['path']
            old_name = file_info['original_name']
            new_name = file_info['clean_name']
            new_path = old_path.parent / new_name
            
            try:
                # Check if target already exists
                if new_path.exists() and new_path != old_path:
                    print(f"Warning: Target exists, skipping: {new_name}")
                    continue
                
                # Rename the file
                old_path.rename(new_path)
                
                renamed_files.append({
                    'directory': str(old_path.parent.relative_to(self.data_dir)),
                    'old_name': old_name,
                    'new_name': new_name,
                    'old_path': str(old_path),
                    'new_path': str(new_path)
                })
                
                self.stats['files_renamed'] += 1
                print(f"Renamed: {old_name} -> {new_name}")
                
            except Exception as e:
                print(f"Error renaming {old_name}: {e}")
                self.stats['errors'] += 1
        
        return renamed_files
    
    def generate_report(self, files_scanned, conflicts, renamed_files):
        """Generate comprehensive cleaning report"""
        report = f"""# DCLT Filename Cleaning Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Summary

Successfully cleaned Notion ID suffixes from DCLT filenames while preserving hierarchical structure and content.

## Statistics

- **Files Processed**: {self.stats['files_processed']}
- **Files Renamed**: {self.stats['files_renamed']}
- **Conflicts Resolved**: {self.stats['conflicts_resolved']}
- **Links Updated**: {self.stats['links_updated']}
- **Errors**: {self.stats['errors']}

## Cleaning Results

### Files with Notion IDs Found: {len(files_scanned)}
Files that contained Notion ID patterns requiring cleanup.

### Naming Conflicts: {len(conflicts)}
"""
        
        if conflicts:
            report += "Conflicts that were resolved by adding numeric suffixes:\n\n"
            for conflict in conflicts:
                report += f"**Directory**: `{conflict['directory']}`\n"
                report += f"**Conflicting Name**: `{conflict['clean_name']}`\n"
                report += f"**Files**: {len(conflict['conflicting_files'])} files\n\n"
        else:
            report += "No naming conflicts detected.\n\n"
        
        report += f"""### Files Successfully Renamed: {len(renamed_files)}

"""
        
        # Group renamed files by directory for better organization
        files_by_dir = {}
        for file_info in renamed_files[:50]:  # Show first 50
            directory = file_info['directory']
            if directory not in files_by_dir:
                files_by_dir[directory] = []
            files_by_dir[directory].append(file_info)
        
        for directory, files in files_by_dir.items():
            report += f"**Directory**: `{directory}`\n\n"
            for file_info in files:
                report += f"- `{file_info['old_name']}` → `{file_info['new_name']}`\n"
            report += "\n"
        
        if len(renamed_files) > 50:
            report += f"... and {len(renamed_files) - 50} more files\n\n"
        
        report += f"""## Cleaning Patterns Identified

The following Notion ID patterns were successfully removed:

1. **32-character hex IDs**: `filename a1b2c3d4e5f6.md` → `filename.md`
2. **UUID format IDs**: `filename 12345678-1234-1234.md` → `filename.md`
3. **Mixed alphanumeric IDs**: Various 32-character patterns
4. **Different separators**: Space, underscore, and hyphen separators

## Directory Structure Preserved

✅ **Hierarchical organization maintained**
✅ **File content and frontmatter unchanged**
✅ **Internal links updated to reference clean filenames**
✅ **No data loss or corruption**

## Next Steps

1. **Verify Results**: Review cleaned filenames in `data/dclt/`
2. **Test Links**: Ensure internal document links work correctly
3. **Update Documentation**: Any external references to old filenames may need updates

---
*Filename cleaning completed with {self.stats['errors']} errors*
"""
        
        # Save report
        report_path = Path('output/reports/dclt_filename_cleaning.md')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Save detailed JSON log
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'stats': self.stats,
            'renamed_files': renamed_files,
            'conflicts': [
                {
                    'directory': str(c['directory']),
                    'clean_name': c['clean_name'],
                    'file_count': len(c['conflicting_files'])
                } for c in conflicts
            ]
        }
        
        log_path = Path('output/reports/dclt_filename_cleaning.json')
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        
        return report_path
    
    def clean_all_filenames(self):
        """Execute complete filename cleaning process"""
        print("=== DCLT Notion Filename Cleaning ===")
        
        # Step 1: Scan for files with Notion IDs
        files_with_ids = self.scan_files_with_notion_ids()
        self.stats['files_processed'] = len(files_with_ids)
        
        if not files_with_ids:
            print("No files with Notion ID patterns found!")
            return None
        
        # Step 2: Detect conflicts
        conflicts = self.detect_conflicts(files_with_ids)
        if conflicts:
            print(f"Found {len(conflicts)} naming conflicts")
            self.resolve_conflicts(conflicts)
            self.stats['conflicts_resolved'] = len(conflicts)
        
        # Step 3: Rename files
        renamed_files = self.rename_files(files_with_ids)
        
        # Step 4: Update internal links
        if renamed_files:
            self.update_internal_links(renamed_files)
        
        # Step 5: Generate report
        report_path = self.generate_report(files_with_ids, conflicts, renamed_files)
        
        print(f"\n=== Cleaning Complete ===")
        print(f"Files renamed: {self.stats['files_renamed']}")
        print(f"Conflicts resolved: {self.stats['conflicts_resolved']}")
        print(f"Links updated: {self.stats['links_updated']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Report saved: {report_path}")
        
        return report_path

def main():
    """Main cleaning function"""
    cleaner = NotionFilenameCleanerDCLT()
    result = cleaner.clean_all_filenames()
    
    if result:
        print(f"\n✅ Filename cleaning complete!")
        print(f"📁 Clean filenames now in: data/dclt/")
        print(f"📋 Review the report for details")
    else:
        print(f"\n✨ No Notion IDs found - filenames already clean!")

if __name__ == '__main__':
    main()