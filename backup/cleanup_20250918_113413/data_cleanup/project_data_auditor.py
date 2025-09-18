#!/usr/bin/env python3
"""
Project Data Quality Auditor
Identifies and reports data quality issues in DCLT project files
"""

import os
import yaml
import json
from pathlib import Path
import re
from collections import defaultdict, Counter
from datetime import datetime

class ProjectDataAuditor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.issues = defaultdict(list)
        self.stats = defaultdict(int)
        self.projects = []
        
    def audit_all_files(self):
        """Run comprehensive audit of all project files"""
        print("🔍 Starting comprehensive project data audit...")
        
        self.find_all_files()
        self.check_test_files()
        self.check_naming_conventions()
        self.check_frontmatter_quality()
        self.check_duplicate_content()
        self.check_text_formatting()
        self.generate_cleanup_report()
        
        return self.issues
    
    def find_all_files(self):
        """Find and categorize all markdown files"""
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self.projects.append({
                        'file_path': file_path,
                        'filename': file,
                        'relative_path': os.path.relpath(file_path, self.data_dir)
                    })
        
        self.stats['total_files'] = len(self.projects)
        print(f"📊 Found {len(self.projects)} markdown files")
    
    def check_test_files(self):
        """Identify test files and temporary content"""
        test_patterns = [
            r'test',
            r'TEST',
            r'Test',
            r'example',
            r'Example',
            r'EXAMPLE',
            r'temp',
            r'temporary',
            r'draft',
            r'untitled'
        ]
        
        test_files = []
        for project in self.projects:
            filepath = project['file_path']
            filename = project['filename']
            
            # Check filename
            for pattern in test_patterns:
                if re.search(pattern, filename, re.IGNORECASE):
                    test_files.append({
                        'file': filepath,
                        'reason': f'Filename contains "{pattern}"',
                        'type': 'test_file'
                    })
                    break
            
            # Check file content for test indicators
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(r'title.*test|test.*project|example.*project', content, re.IGNORECASE):
                        test_files.append({
                            'file': filepath,
                            'reason': 'Contains test content in title/content',
                            'type': 'test_content'
                        })
            except:
                pass
        
        self.issues['test_files'] = test_files
        self.stats['test_files'] = len(test_files)
        print(f"🧪 Found {len(test_files)} test/example files")
    
    def check_naming_conventions(self):
        """Check for naming convention issues"""
        naming_issues = []
        
        for project in self.projects:
            filename = project['filename']
            filepath = project['file_path']
            
            issues_found = []
            
            # Check for special characters that might cause issues
            if re.search(r'[<>:"|?*]', filename):
                issues_found.append('Contains invalid filename characters')
            
            # Check for very long filenames
            if len(filename) > 100:
                issues_found.append(f'Filename too long ({len(filename)} chars)')
            
            # Check for inconsistent dash/underscore usage
            if '—' in filename:  # Em dash
                issues_found.append('Uses em-dash instead of regular dash')
            
            # Check for emoji in filenames (can cause encoding issues)
            if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', filename):
                issues_found.append('Contains emoji in filename')
            
            # Check for multiple consecutive spaces or special chars
            if re.search(r'\s{2,}|--+|__+', filename):
                issues_found.append('Contains multiple consecutive spaces or dashes')
            
            if issues_found:
                naming_issues.append({
                    'file': filepath,
                    'filename': filename,
                    'issues': issues_found
                })
        
        self.issues['naming_issues'] = naming_issues
        self.stats['naming_issues'] = len(naming_issues)
        print(f"📝 Found {len(naming_issues)} naming convention issues")
    
    def check_frontmatter_quality(self):
        """Check frontmatter consistency and quality"""
        frontmatter_issues = []
        title_analysis = defaultdict(list)
        
        for project in self.projects:
            filepath = project['file_path']
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter
                frontmatter = self.extract_frontmatter(content)
                
                if not frontmatter:
                    frontmatter_issues.append({
                        'file': filepath,
                        'issue': 'No frontmatter found',
                        'severity': 'low'
                    })
                    continue
                
                # Check for missing essential fields
                essential_fields = ['title']
                missing_fields = []
                for field in essential_fields:
                    if field not in frontmatter:
                        missing_fields.append(field)
                
                if missing_fields:
                    frontmatter_issues.append({
                        'file': filepath,
                        'issue': f'Missing essential fields: {", ".join(missing_fields)}',
                        'severity': 'medium'
                    })
                
                # Check title consistency
                title = frontmatter.get('title', '')
                if title:
                    title_analysis[title].append(filepath)
                
                # Check for inconsistent date formats
                date_fields = ['start_date', 'end_date', 'created_date', 'last_updated']
                for field in date_fields:
                    if field in frontmatter:
                        date_value = frontmatter[field]
                        if isinstance(date_value, str) and not re.match(r'\\d{4}-\\d{2}-\\d{2}', date_value):
                            frontmatter_issues.append({
                                'file': filepath,
                                'issue': f'Inconsistent date format in {field}: {date_value}',
                                'severity': 'low'
                            })
                
            except Exception as e:
                frontmatter_issues.append({
                    'file': filepath,
                    'issue': f'Error reading file: {str(e)}',
                    'severity': 'high'
                })
        
        # Check for duplicate titles
        duplicate_titles = {title: files for title, files in title_analysis.items() if len(files) > 1}
        for title, files in duplicate_titles.items():
            frontmatter_issues.append({
                'file': 'multiple',
                'files': files,
                'issue': f'Duplicate title: "{title}"',
                'severity': 'medium'
            })
        
        self.issues['frontmatter_issues'] = frontmatter_issues
        self.issues['duplicate_titles'] = duplicate_titles
        self.stats['frontmatter_issues'] = len(frontmatter_issues)
        self.stats['duplicate_titles'] = len(duplicate_titles)
        print(f"📋 Found {len(frontmatter_issues)} frontmatter issues")
        print(f"🔄 Found {len(duplicate_titles)} duplicate titles")
    
    def check_duplicate_content(self):
        """Check for duplicate or very similar content"""
        content_analysis = defaultdict(list)
        duplicate_content = []
        
        for project in self.projects:
            filepath = project['file_path']
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Create content hash for similarity detection
                content_clean = re.sub(r'\\s+', ' ', content.lower().strip())
                content_hash = hash(content_clean[:500])  # First 500 chars
                content_analysis[content_hash].append(filepath)
                
            except:
                pass
        
        # Find duplicates
        for content_hash, files in content_analysis.items():
            if len(files) > 1:
                duplicate_content.append({
                    'files': files,
                    'count': len(files)
                })
        
        self.issues['duplicate_content'] = duplicate_content
        self.stats['duplicate_content'] = len(duplicate_content)
        print(f"📄 Found {len(duplicate_content)} sets of duplicate content")
    
    def check_text_formatting(self):
        """Check for text formatting issues that could cause display problems"""
        formatting_issues = []
        
        for project in self.projects:
            filepath = project['file_path']
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                issues_found = []
                
                # Check for very long lines that could cause display issues
                lines = content.split('\\n')
                long_lines = [i for i, line in enumerate(lines, 1) if len(line) > 200]
                if long_lines:
                    issues_found.append(f'Long lines that may cause display issues: {len(long_lines)} lines')
                
                # Check for special Unicode characters that might render poorly
                if re.search(r'[\\u2013\\u2014\\u2018\\u2019\\u201C\\u201D]', content):
                    issues_found.append('Contains smart quotes or special dashes')
                
                # Check for inconsistent markdown heading structure
                headings = re.findall(r'^(#{1,6})\\s', content, re.MULTILINE)
                if headings:
                    heading_levels = [len(h) for h in headings]
                    if heading_levels and max(heading_levels) - min(heading_levels) > 3:
                        issues_found.append('Inconsistent heading hierarchy')
                
                # Check for potential text overlap issues (multiple titles, etc.)
                title_count = len(re.findall(r'^#\\s', content, re.MULTILINE))
                if title_count > 3:
                    issues_found.append(f'Multiple H1 headings ({title_count}) may cause visual conflicts')
                
                if issues_found:
                    formatting_issues.append({
                        'file': filepath,
                        'issues': issues_found
                    })
                
            except:
                pass
        
        self.issues['formatting_issues'] = formatting_issues
        self.stats['formatting_issues'] = len(formatting_issues)
        print(f"📝 Found {len(formatting_issues)} text formatting issues")
    
    def extract_frontmatter(self, content):
        """Extract YAML frontmatter from content"""
        if not content.startswith('---'):
            return {}
        
        try:
            end_index = content.find('---', 3)
            if end_index == -1:
                return {}
            
            frontmatter_content = content[3:end_index].strip()
            return yaml.safe_load(frontmatter_content) or {}
        except:
            return {}
    
    def generate_cleanup_report(self):
        """Generate comprehensive cleanup report"""
        print("\\n📊 === PROJECT DATA QUALITY AUDIT REPORT ===")
        print(f"Total files analyzed: {self.stats['total_files']}")
        print(f"Test files found: {self.stats['test_files']}")
        print(f"Naming issues: {self.stats['naming_issues']}")
        print(f"Frontmatter issues: {self.stats['frontmatter_issues']}")
        print(f"Duplicate titles: {self.stats['duplicate_titles']}")
        print(f"Duplicate content: {self.stats['duplicate_content']}")
        print(f"Formatting issues: {self.stats['formatting_issues']}")
        
        # Calculate overall health score
        total_issues = sum([
            self.stats['test_files'],
            self.stats['naming_issues'], 
            self.stats['frontmatter_issues'],
            self.stats['duplicate_content'],
            self.stats['formatting_issues']
        ])
        
        health_score = max(0, 100 - (total_issues / self.stats['total_files'] * 100))
        print(f"\\n🎯 Overall Data Health Score: {health_score:.1f}/100")
        
        if health_score >= 90:
            print("✅ Excellent data quality")
        elif health_score >= 75:
            print("⚠️ Good data quality with minor issues")  
        elif health_score >= 60:
            print("🔶 Fair data quality - cleanup recommended")
        else:
            print("🔴 Poor data quality - cleanup required")
    
    def save_audit_report(self, output_file="output/reports/data_quality_audit.json"):
        """Save detailed audit report"""
        audit_report = {
            'timestamp': str(datetime.now()),
            'stats': dict(self.stats),
            'issues': dict(self.issues),
            'recommendations': self.generate_recommendations()
        }
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(audit_report, f, indent=2, default=str)
        
        print(f"📄 Detailed audit report saved to: {output_file}")
    
    def generate_recommendations(self):
        """Generate cleanup recommendations based on findings"""
        recommendations = []
        
        if self.stats['test_files'] > 0:
            recommendations.append({
                'priority': 'high',
                'action': 'Remove test files',
                'description': f'Delete or rename {self.stats["test_files"]} test/example files'
            })
        
        if self.stats['duplicate_titles'] > 0:
            recommendations.append({
                'priority': 'high', 
                'action': 'Resolve duplicate titles',
                'description': f'Rename or consolidate {self.stats["duplicate_titles"]} duplicate titles'
            })
        
        if self.stats['naming_issues'] > 0:
            recommendations.append({
                'priority': 'medium',
                'action': 'Fix naming conventions',
                'description': f'Standardize {self.stats["naming_issues"]} file names'
            })
        
        if self.stats['formatting_issues'] > 0:
            recommendations.append({
                'priority': 'medium',
                'action': 'Fix formatting issues', 
                'description': f'Resolve {self.stats["formatting_issues"]} text formatting problems'
            })
        
        return recommendations

def main():
    from datetime import datetime
    
    auditor = ProjectDataAuditor()
    issues = auditor.audit_all_files()
    auditor.save_audit_report()
    
    return issues

if __name__ == "__main__":
    main()