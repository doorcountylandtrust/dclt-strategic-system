#!/usr/bin/env python3
"""
Automated Project Data Cleanup
Fixes data quality issues identified in the audit
"""

import os
import yaml
import json
import shutil
from pathlib import Path
import re
from datetime import datetime

class ProjectDataCleaner:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.backup_dir = f"backup/cleanup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.cleanup_log = []
        
    def run_automated_cleanup(self, audit_file="output/reports/data_quality_audit.json"):
        """Run automated cleanup based on audit results"""
        print("🧹 Starting automated data cleanup...")
        
        # Load audit results
        with open(audit_file, 'r') as f:
            audit_data = json.load(f)
        
        # Create backup
        self.create_backup()
        
        # Run cleanup tasks
        self.remove_test_files(audit_data['issues']['test_files'])
        self.fix_naming_issues(audit_data['issues']['naming_issues'])
        self.standardize_frontmatter(audit_data['issues']['frontmatter_issues'])
        self.fix_formatting_issues(audit_data['issues']['formatting_issues'])
        
        # Generate cleanup report
        self.generate_cleanup_report()
        
        print("✅ Automated cleanup completed!")
        return self.cleanup_log
    
    def create_backup(self):
        """Create backup of data directory before cleanup"""
        print("💾 Creating backup...")
        
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copytree(self.data_dir, f"{self.backup_dir}/data", dirs_exist_ok=True)
            print(f"✅ Backup created at: {self.backup_dir}")
            self.cleanup_log.append({
                'action': 'backup_created',
                'location': self.backup_dir,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            raise
    
    def remove_test_files(self, test_files):
        """Remove or rename test files"""
        print("🧪 Cleaning up test files...")
        
        actual_test_files = []
        legitimate_files = []
        
        for test_file in test_files:
            filepath = test_file['file']
            reason = test_file['reason']
            
            # Distinguish between actual test files and legitimate content
            filename = os.path.basename(filepath)
            
            # Definitely test files
            if any(pattern in filename.upper() for pattern in ['TEST', 'EXAMPLE']) and not any(word in filepath.lower() for word in ['template', 'messaging', 'communication']):
                actual_test_files.append(filepath)
            # Legitimate files that contain test-like words
            elif any(word in filepath.lower() for word in ['template', 'draft', 'design']):
                legitimate_files.append(filepath)
        
        # Remove actual test files
        for filepath in actual_test_files:
            if os.path.exists(filepath):
                print(f"  🗑️ Removing: {filepath}")
                os.remove(filepath)
                self.cleanup_log.append({
                    'action': 'removed_test_file',
                    'file': filepath,
                    'timestamp': datetime.now().isoformat()
                })
        
        print(f"✅ Removed {len(actual_test_files)} test files")
        print(f"ℹ️ Kept {len(legitimate_files)} legitimate files with test-like names")
    
    def fix_naming_issues(self, naming_issues):
        """Fix file naming convention issues"""
        print("📝 Fixing naming convention issues...")
        
        for issue in naming_issues[:20]:  # Limit to first 20 to avoid overwhelming
            filepath = issue['file']
            filename = issue['filename']
            issues_found = issue['issues']
            
            if not os.path.exists(filepath):
                continue
            
            new_filename = self.standardize_filename(filename)
            
            if new_filename != filename:
                new_filepath = os.path.join(os.path.dirname(filepath), new_filename)
                
                # Avoid overwriting existing files
                counter = 1
                while os.path.exists(new_filepath):
                    name, ext = os.path.splitext(new_filename)
                    new_filepath = os.path.join(os.path.dirname(filepath), f"{name}_{counter}{ext}")
                    counter += 1
                
                print(f"  📝 Renaming: {filename} → {os.path.basename(new_filepath)}")
                os.rename(filepath, new_filepath)
                
                self.cleanup_log.append({
                    'action': 'renamed_file',
                    'old_path': filepath,
                    'new_path': new_filepath,
                    'issues_fixed': issues_found,
                    'timestamp': datetime.now().isoformat()
                })
        
        print(f"✅ Fixed naming issues for {min(len(naming_issues), 20)} files")
    
    def standardize_filename(self, filename):
        """Standardize a filename according to conventions"""
        name, ext = os.path.splitext(filename)
        
        # Replace em-dashes with regular dashes
        name = re.sub(r'[—–]', '-', name)
        
        # Remove invalid characters
        name = re.sub(r'[<>:"|?*]', '', name)
        
        # Replace multiple spaces/dashes with single ones
        name = re.sub(r'\\s{2,}', ' ', name)
        name = re.sub(r'-{2,}', '-', name)
        name = re.sub(r'_{2,}', '_', name)
        
        # Trim and clean
        name = name.strip(' -_')
        
        # Limit length
        if len(name) > 80:
            name = name[:80].strip(' -_')
        
        return name + ext
    
    def standardize_frontmatter(self, frontmatter_issues):
        """Fix frontmatter consistency issues"""
        print("📋 Standardizing frontmatter...")
        
        files_processed = set()
        
        for issue in frontmatter_issues:
            if issue.get('file') == 'multiple':  # Skip duplicate title issues for now
                continue
                
            filepath = issue['file']
            if filepath in files_processed or not os.path.exists(filepath):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add minimal frontmatter if missing
                if not content.startswith('---'):
                    filename_title = os.path.basename(filepath).replace('.md', '')
                    minimal_frontmatter = f"""---
title: "{filename_title}"
created_date: '{datetime.now().strftime('%Y-%m-%d')}'
last_updated: '{datetime.now().strftime('%Y-%m-%d')}'
---

"""
                    new_content = minimal_frontmatter + content
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    files_processed.add(filepath)
                    self.cleanup_log.append({
                        'action': 'added_frontmatter',
                        'file': filepath,
                        'timestamp': datetime.now().isoformat()
                    })
                
            except Exception as e:
                print(f"❌ Error processing {filepath}: {e}")
        
        print(f"✅ Standardized frontmatter for {len(files_processed)} files")
    
    def fix_formatting_issues(self, formatting_issues):
        """Fix text formatting issues"""
        print("📄 Fixing formatting issues...")
        
        for issue in formatting_issues[:50]:  # Limit to prevent overwhelming changes
            filepath = issue['file']
            issues_found = issue['issues']
            
            if not os.path.exists(filepath):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Fix smart quotes and dashes
                content = re.sub(r'["""]', '"', content)
                content = re.sub(r"['']", "'", content)
                content = re.sub(r'[–—]', '-', content)
                
                # Fix multiple consecutive empty lines
                content = re.sub(r'\\n{3,}', '\\n\\n', content)
                
                # Only save if changes were made
                if content != original_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.cleanup_log.append({
                        'action': 'fixed_formatting',
                        'file': filepath,
                        'issues_fixed': issues_found,
                        'timestamp': datetime.now().isoformat()
                    })
                
            except Exception as e:
                print(f"❌ Error fixing formatting in {filepath}: {e}")
        
        print(f"✅ Fixed formatting issues in {min(len(formatting_issues), 50)} files")
    
    def generate_cleanup_report(self):
        """Generate comprehensive cleanup report"""
        report = {
            'cleanup_timestamp': datetime.now().isoformat(),
            'backup_location': self.backup_dir,
            'actions_taken': len(self.cleanup_log),
            'cleanup_log': self.cleanup_log,
            'summary': {
                'files_removed': len([log for log in self.cleanup_log if log['action'] == 'removed_test_file']),
                'files_renamed': len([log for log in self.cleanup_log if log['action'] == 'renamed_file']),
                'frontmatter_added': len([log for log in self.cleanup_log if log['action'] == 'added_frontmatter']),
                'formatting_fixed': len([log for log in self.cleanup_log if log['action'] == 'fixed_formatting'])
            }
        }
        
        report_file = "output/reports/cleanup_report.json"
        Path(report_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\\n📊 === CLEANUP SUMMARY ===")
        print(f"Files removed: {report['summary']['files_removed']}")
        print(f"Files renamed: {report['summary']['files_renamed']}")
        print(f"Frontmatter added: {report['summary']['frontmatter_added']}")
        print(f"Formatting fixed: {report['summary']['formatting_fixed']}")
        print(f"Total actions: {report['actions_taken']}")
        print(f"Backup location: {self.backup_dir}")
        print(f"📄 Full report: {report_file}")

def main():
    cleaner = ProjectDataCleaner()
    cleaner.run_automated_cleanup()

if __name__ == "__main__":
    main()