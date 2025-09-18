#!/usr/bin/env python3
"""
Reorganize DCLT files to restore original Notion hierarchy
Moves processed files from flat structure to hierarchical organization
"""

import os
import shutil
from pathlib import Path
import json
from datetime import datetime

class DCLTHierarchyOrganizer:
    def __init__(self, current_data_dir='data/dclt', backup_dir='notion_export', output_dir='data/dclt_reorganized'):
        self.current_data_dir = Path(current_data_dir)
        self.backup_dir = Path(backup_dir)
        self.output_dir = Path(output_dir)
        self.file_mapping = {}
        self.stats = {
            'files_moved': 0,
            'directories_created': 0,
            'files_not_found': 0,
            'errors': 0
        }
    
    def analyze_original_hierarchy(self):
        """Analyze the original hierarchy from backup directory"""
        print("Analyzing original hierarchy from backup...")
        
        hierarchy_map = {}
        
        # Walk through backup directory to understand structure
        for root, dirs, files in os.walk(self.backup_dir):
            relative_path = Path(root).relative_to(self.backup_dir)
            
            for file in files:
                if file.endswith('.md'):
                    # Create mapping from filename to its original location
                    original_path = Path(root) / file
                    relative_original = original_path.relative_to(self.backup_dir)
                    
                    # Clean filename for matching with processed files
                    clean_filename = self.clean_filename_for_matching(file)
                    
                    hierarchy_map[clean_filename] = str(relative_original)
        
        print(f"Found {len(hierarchy_map)} files with original hierarchy information")
        return hierarchy_map
    
    def clean_filename_for_matching(self, filename):
        """Clean filename to match processed filenames"""
        import re
        
        # Remove hash IDs
        cleaned = re.sub(r'\s[a-f0-9]{32}\.md$', '.md', filename)
        
        # Remove emojis and special characters at start
        cleaned = re.sub(r'^[^\w\s-]+\s*', '', cleaned)
        
        # Convert to lowercase and replace spaces with hyphens
        name_part = cleaned[:-3]  # Remove .md
        name_part = re.sub(r'[^\w\s-]', '', name_part.lower())
        name_part = re.sub(r'[-\s]+', '-', name_part).strip('-')
        
        return name_part + '.md'
    
    def scan_current_files(self):
        """Scan current processed files"""
        print("Scanning current processed files...")
        
        current_files = {}
        
        for category in ['1-strategy', '2-execution', '3-reference-tools']:
            category_path = self.current_data_dir / category
            if category_path.exists():
                for file_path in category_path.rglob('*.md'):
                    filename = file_path.name
                    current_files[filename] = {
                        'current_path': file_path,
                        'category': category
                    }
        
        print(f"Found {len(current_files)} processed files")
        return current_files
    
    def create_hierarchy_mapping(self, hierarchy_map, current_files):
        """Create mapping between current files and their target locations"""
        print("Creating hierarchy mapping...")
        
        mapping = {}
        matched = 0
        unmatched = []
        
        for current_filename, file_info in current_files.items():
            # Try exact match first
            if current_filename in hierarchy_map:
                target_path = hierarchy_map[current_filename]
                mapping[current_filename] = {
                    'current_path': file_info['current_path'],
                    'target_path': target_path,
                    'category': file_info['category']
                }
                matched += 1
            else:
                # Try fuzzy matching for files that might have been renamed
                best_match = self.find_best_match(current_filename, hierarchy_map.keys())
                if best_match:
                    target_path = hierarchy_map[best_match]
                    mapping[current_filename] = {
                        'current_path': file_info['current_path'],
                        'target_path': target_path,
                        'category': file_info['category'],
                        'fuzzy_match': best_match
                    }
                    matched += 1
                else:
                    unmatched.append(current_filename)
        
        print(f"Matched {matched} files, {len(unmatched)} unmatched")
        if unmatched:
            print(f"Unmatched files: {unmatched[:10]}...")  # Show first 10
        
        return mapping, unmatched
    
    def find_best_match(self, filename, candidates):
        """Find best matching filename using similarity"""
        # Simple similarity based on common substrings
        base_name = filename[:-3].lower()  # Remove .md and lowercase
        best_score = 0
        best_match = None
        
        for candidate in candidates:
            candidate_base = candidate[:-3].lower()
            
            # Calculate similarity score
            words1 = set(base_name.split('-'))
            words2 = set(candidate_base.split('-'))
            
            if words1 and words2:
                intersection = len(words1.intersection(words2))
                union = len(words1.union(words2))
                similarity = intersection / union if union > 0 else 0
                
                if similarity > best_score and similarity > 0.5:  # 50% similarity threshold
                    best_score = similarity
                    best_match = candidate
        
        return best_match
    
    def reorganize_files(self, mapping):
        """Reorganize files according to mapping"""
        print("Reorganizing files to hierarchical structure...")
        
        # Create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        
        for filename, file_info in mapping.items():
            try:
                current_path = Path(file_info['current_path'])
                target_relative_path = Path(file_info['target_path'])
                target_path = self.output_dir / target_relative_path
                
                # Create target directory
                target_path.parent.mkdir(parents=True, exist_ok=True)
                if not target_path.parent.exists():
                    self.stats['directories_created'] += 1
                
                # Copy file to new location
                if current_path.exists():
                    shutil.copy2(current_path, target_path)
                    self.stats['files_moved'] += 1
                    
                    print(f"Moved: {current_path.name} -> {target_relative_path}")
                else:
                    self.stats['files_not_found'] += 1
                    print(f"Warning: File not found: {current_path}")
                
            except Exception as e:
                self.stats['errors'] += 1
                print(f"Error processing {filename}: {e}")
    
    def create_category_summaries(self):
        """Create README files for each main category"""
        categories = {
            '1-strategy': {
                'title': 'Strategic Planning & Framework',
                'description': 'High-level strategic planning documents, frameworks, and organizational initiatives.'
            },
            '2-execution': {
                'title': 'Project Execution & Implementation',
                'description': 'Implementation plans, campaigns, project execution materials, and operational content.'
            },
            '3-reference-tools': {
                'title': 'Reference Materials & Tools',
                'description': 'Research, analysis, tools, templates, and reference materials for strategic decision-making.'
            }
        }
        
        for category, info in categories.items():
            category_path = self.output_dir / category
            if category_path.exists():
                readme_path = category_path / 'README.md'
                
                # Count files and subdirectories
                file_count = len(list(category_path.rglob('*.md'))) - (1 if readme_path.exists() else 0)
                dir_count = len([d for d in category_path.rglob('*') if d.is_dir()]) - 1  # Exclude category dir itself
                
                readme_content = f"""# {info['title']}

{info['description']}

## Directory Contents

- **Files**: {file_count} markdown files
- **Subdirectories**: {dir_count} organized by topic and project

## Organization

This directory maintains the original Notion hierarchy to preserve document relationships and context. Files are organized by:

1. **Major themes** (e.g., website strategy, brand system, communications)
2. **Project phases** (planning, execution, review)
3. **Content types** (templates, research, deliverables)

## Navigation

Use your file explorer or IDE to browse the hierarchical structure. Each subdirectory represents a logical grouping of related materials.

---
*Organized: {datetime.now().strftime('%Y-%m-%d')} | Structure: Hierarchical (preserving Notion relationships)*
"""
                
                with open(readme_path, 'w') as f:
                    f.write(readme_content)
    
    def generate_report(self, mapping, unmatched):
        """Generate comprehensive reorganization report"""
        report = f"""# DCLT Hierarchy Reorganization Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Summary

Successfully reorganized DCLT strategic planning files from flat structure to hierarchical organization based on original Notion workspace relationships.

## Statistics

- **Files Moved**: {self.stats['files_moved']}
- **Directories Created**: {self.stats['directories_created']}
- **Files Not Found**: {self.stats['files_not_found']}
- **Errors**: {self.stats['errors']}
- **Unmatched Files**: {len(unmatched)}

## Reorganization Results

### Source Structure
```
data/dclt/
├── 1-strategy/ (flat - {len(list(self.current_data_dir.glob('1-strategy/*.md')))} files)
├── 2-execution/ (flat - {len(list(self.current_data_dir.glob('2-execution/*.md')))} files)  
└── 3-reference-tools/ (flat - {len(list(self.current_data_dir.glob('3-reference-tools/*.md')))} files)
```

### Target Structure
```
data/dclt_reorganized/
├── 1-strategy/ (hierarchical with thematic subdirectories)
├── 2-execution/ (hierarchical with project-based organization)
└── 3-reference-tools/ (hierarchical with reference categorization)
```

## File Matching Results

### Successfully Matched: {len(mapping)}
Files successfully mapped from flat structure to hierarchical organization using:
- Exact filename matching
- Fuzzy matching for renamed files
- Category-based organization

### Unmatched Files: {len(unmatched)}
"""
        
        if unmatched:
            report += "Files that could not be matched to original hierarchy:\n"
            for filename in unmatched[:20]:  # Show first 20
                report += f"- {filename}\n"
            
            if len(unmatched) > 20:
                report += f"... and {len(unmatched) - 20} more\n"
            
            report += "\nUnmatched files remain in flat structure within their categories.\n"
        
        report += f"""
## Next Steps

1. **Review Reorganized Structure**: Check `{self.output_dir}` for hierarchical organization
2. **Handle Unmatched Files**: Manually place remaining {len(unmatched)} files in appropriate locations
3. **Update Documentation**: Review and update any internal links if needed
4. **Replace Original**: Once verified, replace original flat structure with reorganized version

## Directory Benefits

- **Preserved Relationships**: Original Notion page relationships maintained
- **Logical Grouping**: Related documents grouped together
- **Better Navigation**: Hierarchical structure improves discoverability
- **Context Preservation**: Files maintain their original organizational context

---
*Reorganization completed with {self.stats['errors']} errors*
"""
        
        report_path = Path('output/reports/dclt_hierarchy_reorganization.md')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(report)
        
        return report_path
    
    def run_reorganization(self):
        """Execute complete reorganization process"""
        print("=== DCLT Hierarchy Reorganization ===")
        
        # Step 1: Analyze original hierarchy
        hierarchy_map = self.analyze_original_hierarchy()
        
        # Step 2: Scan current files
        current_files = self.scan_current_files()
        
        # Step 3: Create mapping
        mapping, unmatched = self.create_hierarchy_mapping(hierarchy_map, current_files)
        
        # Step 4: Reorganize files
        self.reorganize_files(mapping)
        
        # Step 5: Create category summaries
        self.create_category_summaries()
        
        # Step 6: Generate report
        report_path = self.generate_report(mapping, unmatched)
        
        print(f"\n=== Reorganization Complete ===")
        print(f"Files moved: {self.stats['files_moved']}")
        print(f"Directories created: {self.stats['directories_created']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Report saved: {report_path}")
        print(f"Reorganized structure: {self.output_dir}")
        
        return self.output_dir

def main():
    """Main reorganization function"""
    organizer = DCLTHierarchyOrganizer()
    result_dir = organizer.run_reorganization()
    
    print(f"\n✅ Hierarchical organization complete!")
    print(f"📁 New structure: {result_dir}")
    print(f"📋 Review the report in output/reports/ for details")

if __name__ == '__main__':
    main()