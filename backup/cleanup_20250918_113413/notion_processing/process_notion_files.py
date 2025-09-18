#!/usr/bin/env python3
"""
Process and organize Notion export files for DCLT strategic planning system
"""
import os
import re
import shutil
from pathlib import Path
from datetime import datetime
import json

class NotionFileProcessor:
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
        self.processed_files = []
        self.errors = []
        self.stats = {
            'total_processed': 0,
            'files_renamed': 0,
            'files_moved': 0,
            'frontmatter_added': 0,
            'errors': 0
        }
        
    def extract_hash_id(self, filename):
        """Extract hash ID from filename if present"""
        match = re.search(r'\s([a-f0-9]{32})\.(md|csv)$', filename)
        return match.group(1) if match else None

    def clean_filename(self, filename):
        """Clean filename by removing hash ID and emojis, converting to kebab-case"""
        # Extract extension first
        name, ext = os.path.splitext(filename)
        
        # Remove hash ID
        cleaned = re.sub(r'\s[a-f0-9]{32}$', '', name)
        
        # Remove emojis and special characters at start
        cleaned = re.sub(r'^[^\w\s-]+\s*', '', cleaned)
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        cleaned = re.sub(r'[^\w\s-]', '', cleaned.lower())
        cleaned = re.sub(r'[-\s]+', '-', cleaned).strip('-')
        
        # Ensure we don't end up with empty filename
        if not cleaned:
            cleaned = 'untitled'
            
        return cleaned + ext

    def determine_target_directory(self, file_path, content_category):
        """Determine target directory based on content analysis and current location"""
        current_path = str(file_path.relative_to(self.data_dir))
        
        # If already in dclt structure, preserve that categorization with refinement
        if 'dclt/' in current_path:
            if '1-strategy' in current_path:
                return 'dclt/1-strategy'
            elif '2-execution' in current_path:
                return 'dclt/2-execution'
            elif '3-reference-tools' in current_path:
                return 'dclt/3-reference-tools'
        
        # Use content-based categorization for new files
        category_map = {
            'strategy': 'dclt/1-strategy',
            'execution': 'dclt/2-execution',
            'reference': 'dclt/3-reference-tools'
        }
        
        return category_map.get(content_category, 'dclt/3-reference-tools')

    def analyze_content_category(self, file_path):
        """Analyze file content to determine category"""
        if file_path.suffix != '.md':
            return 'reference'  # CSV files go to reference
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            # Strategy indicators (high-level planning)
            strategy_keywords = [
                'strategic plan', 'strategy', 'mission', 'vision', 'values',
                'goals', 'objectives', 'framework', 'alignment', 'initiative',
                'priorities', 'roadmap', 'north star'
            ]
            
            # Execution indicators (implementation work)
            execution_keywords = [
                'campaign', 'brand', 'website', 'content', 'marketing',
                'implementation', 'task', 'project', 'deliverable',
                'timeline', 'milestone', 'progress', 'tracker'
            ]
            
            # Reference indicators (research, tools, templates)
            reference_keywords = [
                'research', 'analysis', 'data', 'metrics', 'insights',
                'reference', 'tools', 'template', 'example',
                'lessons learned', 'best practice', 'survey'
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
            self.errors.append(f"Error analyzing {file_path}: {e}")
            return 'reference'

    def extract_strategic_metadata(self, file_path, content):
        """Extract strategic metadata from content for frontmatter"""
        metadata = {
            'title': '',
            'project_status': 'in_progress',
            'priority': 'medium',
            'strategic_theme': '',
            'stakeholders': [],
            'tags': [],
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Extract title from filename or first heading
        filename_title = file_path.stem.replace('-', ' ').title()
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        metadata['title'] = h1_match.group(1) if h1_match else filename_title
        
        # Detect priority indicators
        if any(word in content.lower() for word in ['urgent', 'critical', 'immediate']):
            metadata['priority'] = 'high'
        elif any(word in content.lower() for word in ['low priority', 'nice to have', 'future']):
            metadata['priority'] = 'low'
            
        # Detect status indicators
        if any(word in content.lower() for word in ['completed', 'done', 'finished']):
            metadata['project_status'] = 'completed'
        elif any(word in content.lower() for word in ['planned', 'upcoming', 'future']):
            metadata['project_status'] = 'planned'
        elif any(word in content.lower() for word in ['in progress', 'working on', 'ongoing']):
            metadata['project_status'] = 'in_progress'
            
        # Extract potential stakeholders
        stakeholder_patterns = [
            r'(@\w+)',  # @mentions
            r'([A-Z][a-z]+ [A-Z][a-z]+)',  # Names like "John Smith"
            r'(team|department|staff|board|director|manager)',
        ]
        
        for pattern in stakeholder_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            metadata['stakeholders'].extend(matches[:5])  # Limit to 5
            
        # Generate tags based on content
        tag_keywords = {
            'brand': ['brand', 'branding', 'identity', 'logo'],
            'website': ['website', 'web', 'digital', 'online'],
            'communication': ['communication', 'messaging', 'outreach'],
            'strategy': ['strategy', 'strategic', 'planning', 'plan'],
            'fundraising': ['fundraising', 'development', 'donor'],
            'conservation': ['conservation', 'land', 'preserve', 'stewardship']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in content.lower() for kw in keywords):
                metadata['tags'].append(tag)
                
        return metadata

    def add_frontmatter(self, file_path):
        """Add YAML frontmatter to markdown files"""
        if file_path.suffix != '.md':
            return False
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Skip if frontmatter already exists
            if content.startswith('---'):
                return False
                
            metadata = self.extract_strategic_metadata(file_path, content)
            
            # Create YAML frontmatter
            frontmatter_lines = ['---']
            for key, value in metadata.items():
                if isinstance(value, list):
                    if value:  # Only add non-empty lists
                        frontmatter_lines.append(f'{key}:')
                        for item in value[:5]:  # Limit list items
                            if isinstance(item, str) and item.strip():
                                clean_item = item.strip().replace('"', '\\"')
                                frontmatter_lines.append(f'  - "{clean_item}"')
                elif isinstance(value, str) and value.strip():
                    clean_value = value.strip().replace('"', '\\"')
                    frontmatter_lines.append(f'{key}: "{clean_value}"')
                else:
                    frontmatter_lines.append(f'{key}: {value}')
            frontmatter_lines.append('---')
            frontmatter_lines.append('')  # Empty line after frontmatter
            
            # Write back with frontmatter
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(frontmatter_lines))
                f.write(content)
                
            return True
            
        except Exception as e:
            self.errors.append(f"Error adding frontmatter to {file_path}: {e}")
            return False

    def process_file(self, file_path):
        """Process a single file: clean name, move to correct location, add frontmatter"""
        try:
            original_name = file_path.name
            clean_name = self.clean_filename(original_name)
            
            # Determine content category and target directory
            content_category = self.analyze_content_category(file_path)
            target_dir = self.determine_target_directory(file_path, content_category)
            
            # Create target directory path
            target_path = self.data_dir / target_dir
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Determine final file path
            final_path = target_path / clean_name
            
            # Handle name conflicts
            counter = 1
            while final_path.exists() and final_path != file_path:
                name_parts = clean_name.rsplit('.', 1)
                if len(name_parts) == 2:
                    new_name = f"{name_parts[0]}-{counter}.{name_parts[1]}"
                else:
                    new_name = f"{clean_name}-{counter}"
                final_path = target_path / new_name
                counter += 1
            
            # Process the file
            renamed = original_name != clean_name
            moved = file_path != final_path
            frontmatter_added = False
            
            # Move/rename if needed
            if moved:
                shutil.move(str(file_path), str(final_path))
                self.stats['files_moved'] += 1
                
            if renamed:
                self.stats['files_renamed'] += 1
                
            # Add frontmatter
            if final_path.suffix == '.md':
                frontmatter_added = self.add_frontmatter(final_path)
                if frontmatter_added:
                    self.stats['frontmatter_added'] += 1
            
            # Record processing result
            self.processed_files.append({
                'original_path': str(file_path),
                'final_path': str(final_path),
                'original_name': original_name,
                'clean_name': clean_name,
                'category': content_category,
                'target_directory': target_dir,
                'renamed': renamed,
                'moved': moved,
                'frontmatter_added': frontmatter_added
            })
            
            self.stats['total_processed'] += 1
            
        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")
            self.stats['errors'] += 1

    def process_all_files(self):
        """Process all markdown and CSV files"""
        print("Starting file processing...")
        
        # Get all files to process
        md_files = list(self.data_dir.rglob('*.md'))
        csv_files = list(self.data_dir.rglob('*.csv'))
        all_files = md_files + csv_files
        
        print(f"Found {len(all_files)} files to process")
        
        # Process each file
        for i, file_path in enumerate(all_files, 1):
            print(f"Processing {i}/{len(all_files)}: {file_path.name}")
            self.process_file(file_path)
            
        # Generate report
        self.generate_report()
        
    def generate_report(self):
        """Generate processing report"""
        report = {
            'processing_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_files_processed': self.stats['total_processed'],
                'files_renamed': self.stats['files_renamed'],
                'files_moved': self.stats['files_moved'],
                'frontmatter_added': self.stats['frontmatter_added'],
                'errors_encountered': self.stats['errors']
            },
            'file_details': self.processed_files,
            'errors': self.errors,
            'category_distribution': {}
        }
        
        # Calculate category distribution
        for file_info in self.processed_files:
            category = file_info['category']
            if category not in report['category_distribution']:
                report['category_distribution'][category] = 0
            report['category_distribution'][category] += 1
        
        # Save report
        os.makedirs('output/reports', exist_ok=True)
        report_path = 'output/reports/notion_processing_report.json'
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n=== PROCESSING COMPLETE ===")
        print(f"Total files processed: {self.stats['total_processed']}")
        print(f"Files renamed: {self.stats['files_renamed']}")
        print(f"Files moved: {self.stats['files_moved']}")
        print(f"Frontmatter added: {self.stats['frontmatter_added']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"\nDetailed report saved to: {report_path}")
        
        if self.errors:
            print(f"\nErrors encountered:")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  - {error}")

def main():
    """Main processing function"""
    processor = NotionFileProcessor()
    processor.process_all_files()

if __name__ == '__main__':
    main()