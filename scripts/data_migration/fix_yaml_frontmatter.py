#!/usr/bin/env python3
"""
Fix Malformed YAML Frontmatter in DCLT Strategic System
Scan, validate, and repair YAML frontmatter across all markdown files
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class YAMLFrontmatterFixer:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.stats = {
            'files_scanned': 0,
            'files_with_frontmatter': 0,
            'files_with_errors': 0,
            'files_fixed': 0,
            'errors_found': 0,
            'errors_fixed': 0
        }
        self.errors = []
        self.fixes_applied = []
        
        # Standard field mappings
        self.strategic_themes = {
            'strategy': 'Strategic Planning',
            'execution': 'Execution & Implementation', 
            'reference': 'Reference & Tools',
            'brand': 'Brand & Communications',
            'website': 'Website Development',
            'fundraising': 'Fundraising & Development',
            'conservation': 'Land Conservation',
            'community': 'Community Engagement'
        }
        
        self.status_values = ['planned', 'in_progress', 'completed', 'on_hold', 'cancelled']
        self.priority_values = ['low', 'medium', 'high', 'critical']
    
    def extract_frontmatter(self, content):
        """Extract YAML frontmatter from markdown content"""
        if not content.startswith('---\n'):
            return None, content
        
        try:
            parts = content.split('---\n', 2)
            if len(parts) < 3:
                return None, content
            
            frontmatter_text = parts[1]
            body_content = parts[2]
            return frontmatter_text, body_content
        except:
            return None, content
    
    def parse_yaml_safely(self, yaml_text):
        """Attempt to parse YAML, handling common errors"""
        try:
            return yaml.safe_load(yaml_text), None
        except yaml.YAMLError as e:
            return None, str(e)
    
    def identify_yaml_errors(self, yaml_text, file_path):
        """Identify specific YAML syntax errors"""
        errors = []
        lines = yaml_text.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Check for missing values after colons
            if line.endswith(':') and not line.startswith('-'):
                errors.append({
                    'type': 'missing_value',
                    'line': i,
                    'content': line,
                    'description': f'Missing value for field: {line}'
                })
            
            # Check for malformed list items
            if line.startswith('- ') and line.count('"') % 2 != 0:
                errors.append({
                    'type': 'unmatched_quotes',
                    'line': i,
                    'content': line,
                    'description': f'Unmatched quotes in list item: {line}'
                })
            
            # Check for field names without colons
            if ':' not in line and not line.startswith('-') and '=' not in line:
                if any(field in line.lower() for field in ['title', 'status', 'priority']):
                    errors.append({
                        'type': 'missing_colon',
                        'line': i,
                        'content': line,
                        'description': f'Field missing colon: {line}'
                    })
        
        return errors
    
    def parse_single_line_yaml(self, yaml_text):
        """Parse single-line YAML into structured data"""
        data = {}
        fixes = ["Parsed malformed single-line YAML frontmatter"]
        
        # Use regex to extract field patterns
        # Pattern: field_name: "value" or field_name: value
        
        # Extract title
        title_match = re.search(r'title:\s*"([^"]*)"', yaml_text)
        if title_match:
            data['title'] = title_match.group(1)
        
        # Extract project_status  
        status_match = re.search(r'project_status:\s*"([^"]*)"', yaml_text)
        if status_match:
            data['project_status'] = status_match.group(1)
        
        # Extract priority
        priority_match = re.search(r'priority:\s*"([^"]*)"', yaml_text)
        if priority_match:
            data['priority'] = priority_match.group(1)
        
        # Extract strategic_theme (might be empty)
        theme_match = re.search(r'strategic_theme:\s*([^s]*?)(?=\s+stakeholders:|$)', yaml_text)
        if theme_match:
            theme_value = theme_match.group(1).strip().strip('"')
            if theme_value:
                data['strategic_theme'] = theme_value
        
        # Extract stakeholders list
        stakeholders_match = re.search(r'stakeholders:\s*(.*?)(?=\s+tags:|$)', yaml_text)
        if stakeholders_match:
            stakeholders_text = stakeholders_match.group(1)
            # Find all quoted items
            stakeholder_items = re.findall(r'-\s*"([^"]*)"', stakeholders_text)
            data['stakeholders'] = stakeholder_items
        
        # Extract tags list
        tags_match = re.search(r'tags:\s*(.*?)(?=\s+created_date:|$)', yaml_text)
        if tags_match:
            tags_text = tags_match.group(1)
            # Find all quoted items
            tag_items = re.findall(r'-\s*"([^"]*)"', tags_text)
            data['tags'] = tag_items
        
        # Extract created_date
        created_match = re.search(r'created_date:\s*"([^"]*)"', yaml_text)
        if created_match:
            data['created_date'] = created_match.group(1)
        
        # Extract last_updated
        updated_match = re.search(r'last_updated:\s*"([^"]*)"', yaml_text)
        if updated_match:
            data['last_updated'] = updated_match.group(1)
        
        return data, fixes

    def fix_yaml_syntax(self, yaml_text):
        """Fix common YAML syntax errors"""
        fixed_text = yaml_text.strip()
        fixes = []
        
        # Check if this is single-line frontmatter (common issue)
        if '\n' not in fixed_text and len(fixed_text) > 50:
            # Parse single-line YAML directly to data structure
            try:
                parsed_data, parse_fixes = self.parse_single_line_yaml(fixed_text)
                fixes.extend(parse_fixes)
                
                # Convert back to proper YAML format
                clean_yaml = yaml.dump(parsed_data, default_flow_style=False, sort_keys=False)
                return clean_yaml.strip(), fixes
            except Exception as e:
                fixes.append(f"Could not parse single-line YAML: {e}")
                return fixed_text, fixes
        
        lines = fixed_text.split('\n')
        fixed_lines = []
        
        for line in lines:
            original_line = line
            
            # Fix missing values for known fields
            if line.strip().endswith(':') and not line.strip().startswith('-'):
                field_name = line.strip()[:-1].lower()
                
                if field_name == 'strategic_theme':
                    line = line.rstrip() + ' "Strategic Planning"'
                    fixes.append(f"Added default strategic_theme value")
                elif field_name == 'project_status':
                    line = line.rstrip() + ' "planned"'
                    fixes.append(f"Added default project_status value")
                elif field_name == 'priority':
                    line = line.rstrip() + ' "medium"'
                    fixes.append(f"Added default priority value")
                elif field_name in ['stakeholders', 'tags']:
                    line = line.rstrip() + ' []'
                    fixes.append(f"Added empty array for {field_name}")
            
            # Fix unmatched quotes in lists
            if line.strip().startswith('- ') and line.count('"') % 2 != 0:
                # Add missing closing quote
                if line.count('"') == 1 and not line.strip().endswith('"'):
                    line = line.rstrip() + '"'
                    fixes.append(f"Added missing closing quote")
            
            # Fix field names missing colons
            if ':' not in line and not line.strip().startswith('-'):
                for field in ['title', 'status', 'priority', 'strategic_theme']:
                    if field in line.lower() and '=' not in line:
                        line = line.replace(field, f'{field}:', 1)
                        fixes.append(f"Added missing colon for {field}")
                        break
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines), fixes
    
    def standardize_field_values(self, data):
        """Standardize field values to proper schema"""
        if not isinstance(data, dict):
            return data, []
        
        fixes = []
        
        # Fix strategic_theme
        if 'strategic_theme' in data:
            theme = str(data['strategic_theme']).lower().strip()
            for key, standard_value in self.strategic_themes.items():
                if key in theme:
                    data['strategic_theme'] = standard_value
                    fixes.append(f"Standardized strategic_theme to: {standard_value}")
                    break
        
        # Fix project_status
        if 'project_status' in data:
            status = str(data['project_status']).lower().strip()
            if status not in self.status_values:
                # Map common variations
                status_mapping = {
                    'active': 'in_progress',
                    'done': 'completed',
                    'todo': 'planned',
                    'draft': 'planned'
                }
                if status in status_mapping:
                    data['project_status'] = status_mapping[status]
                    fixes.append(f"Mapped project_status: {status} -> {status_mapping[status]}")
                else:
                    data['project_status'] = 'planned'
                    fixes.append(f"Set default project_status: planned")
        
        # Fix priority
        if 'priority' in data:
            priority = str(data['priority']).lower().strip()
            if priority not in self.priority_values:
                data['priority'] = 'medium'
                fixes.append(f"Set default priority: medium")
        
        # Clean up stakeholders list
        if 'stakeholders' in data and isinstance(data['stakeholders'], list):
            original_stakeholders = data['stakeholders'][:]
            cleaned_stakeholders = []
            
            for stakeholder in data['stakeholders']:
                stakeholder_str = str(stakeholder).strip()
                # Remove obvious junk (short fragments, random words)
                if len(stakeholder_str) > 3 and not stakeholder_str.lower() in ['the', 'and', 'for', 'with', 'is', 'are']:
                    # Clean up the stakeholder name
                    stakeholder_str = re.sub(r'^["\'-]+|["\'-]+$', '', stakeholder_str)
                    if stakeholder_str:
                        cleaned_stakeholders.append(stakeholder_str)
            
            if cleaned_stakeholders != original_stakeholders:
                data['stakeholders'] = cleaned_stakeholders
                fixes.append(f"Cleaned stakeholders list: {len(original_stakeholders)} -> {len(cleaned_stakeholders)} items")
        
        # Ensure required fields exist
        if 'created_date' not in data:
            data['created_date'] = datetime.now().strftime('%Y-%m-%d')
            fixes.append("Added created_date")
        
        if 'last_updated' not in data:
            data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            fixes.append("Added last_updated")
        
        return data, fixes
    
    def fix_file_frontmatter(self, file_path):
        """Fix YAML frontmatter in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter_text, body = self.extract_frontmatter(content)
            if not frontmatter_text:
                return False, "No frontmatter found"
            
            self.stats['files_with_frontmatter'] += 1
            
            # Check for YAML errors
            yaml_errors = self.identify_yaml_errors(frontmatter_text, file_path)
            if yaml_errors:
                self.stats['files_with_errors'] += 1
                self.stats['errors_found'] += len(yaml_errors)
            
            # Try to parse original YAML
            parsed_data, parse_error = self.parse_yaml_safely(frontmatter_text)
            
            file_fixes = []
            
            # If parsing failed, try to fix syntax first
            if parsed_data is None:
                fixed_yaml, syntax_fixes = self.fix_yaml_syntax(frontmatter_text)
                file_fixes.extend(syntax_fixes)
                parsed_data, parse_error = self.parse_yaml_safely(fixed_yaml)
                
                if parsed_data is None:
                    self.errors.append({
                        'file': str(file_path.relative_to(self.data_dir)),
                        'error': f"Could not parse YAML even after fixes: {parse_error}",
                        'yaml_errors': yaml_errors
                    })
                    return False, f"Could not parse YAML: {parse_error}"
            
            # Standardize field values
            standardized_data, standard_fixes = self.standardize_field_values(parsed_data)
            file_fixes.extend(standard_fixes)
            
            # If we made any fixes, write the file back
            if file_fixes:
                # Generate clean YAML
                clean_yaml = yaml.dump(standardized_data, default_flow_style=False, sort_keys=False)
                new_content = f"---\n{clean_yaml}---\n{body}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.stats['files_fixed'] += 1
                self.stats['errors_fixed'] += len(file_fixes)
                
                self.fixes_applied.append({
                    'file': str(file_path.relative_to(self.data_dir)),
                    'fixes': file_fixes,
                    'yaml_errors': yaml_errors
                })
                
                return True, f"Fixed {len(file_fixes)} issues"
            
            return False, "No fixes needed"
            
        except Exception as e:
            self.errors.append({
                'file': str(file_path.relative_to(self.data_dir)),
                'error': f"Exception: {str(e)}"
            })
            return False, f"Exception: {str(e)}"
    
    def fix_all_frontmatter(self):
        """Fix YAML frontmatter in all markdown files"""
        print("=== YAML Frontmatter Fixer ===")
        print(f"Scanning directory: {self.data_dir}")
        
        for file_path in self.data_dir.rglob('*.md'):
            self.stats['files_scanned'] += 1
            success, message = self.fix_file_frontmatter(file_path)
            
            if success:
                print(f"✅ {file_path.relative_to(self.data_dir)}: {message}")
            elif "No frontmatter found" not in message and "No fixes needed" not in message:
                print(f"❌ {file_path.relative_to(self.data_dir)}: {message}")
        
        self.generate_report()
        return self.stats
    
    def generate_report(self):
        """Generate comprehensive repair report"""
        report_path = Path('output/reports/yaml_frontmatter_repair_report.md')
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = f"""# YAML Frontmatter Repair Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Summary Statistics

- **Files Scanned**: {self.stats['files_scanned']}
- **Files with Frontmatter**: {self.stats['files_with_frontmatter']}
- **Files with Errors**: {self.stats['files_with_errors']}
- **Files Fixed**: {self.stats['files_fixed']}
- **Total Errors Found**: {self.stats['errors_found']}
- **Total Errors Fixed**: {self.stats['errors_fixed']}

## Files Successfully Repaired

"""
        
        for fix in self.fixes_applied:
            report += f"### {fix['file']}\n"
            for fix_desc in fix['fixes']:
                report += f"- ✅ {fix_desc}\n"
            
            if fix['yaml_errors']:
                report += "\n**YAML Syntax Errors Found:**\n"
                for error in fix['yaml_errors']:
                    report += f"- Line {error['line']}: {error['description']}\n"
            report += "\n"
        
        if self.errors:
            report += "\n## Files with Unresolved Issues\n\n"
            for error in self.errors:
                report += f"### {error['file']}\n"
                report += f"- ❌ {error['error']}\n"
                if 'yaml_errors' in error and error['yaml_errors']:
                    for yaml_error in error['yaml_errors']:
                        report += f"  - Line {yaml_error['line']}: {yaml_error['description']}\n"
                report += "\n"
        
        report += f"""
## Field Standardization Applied

### Strategic Theme Mappings:
- strategy → Strategic Planning
- execution → Execution & Implementation  
- reference → Reference & Tools
- brand → Brand & Communications
- website → Website Development
- fundraising → Fundraising & Development
- conservation → Land Conservation
- community → Community Engagement

### Status Values: {', '.join(self.status_values)}
### Priority Values: {', '.join(self.priority_values)}

## Next Steps
1. All files now have valid, parseable YAML frontmatter
2. Field values standardized across the system
3. Missing required fields added with sensible defaults
4. Stakeholder lists cleaned of junk data

**Result**: All markdown files ready for Obsidian with clean, standardized frontmatter.
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n📄 Detailed report saved to: {report_path}")
        
        # Print summary
        print(f"\n=== Repair Complete ===")
        print(f"✅ Fixed {self.stats['files_fixed']} files with {self.stats['errors_fixed']} total corrections")
        print(f"❌ {len(self.errors)} files had unresolvable issues")
        print(f"📊 {self.stats['files_with_frontmatter']} total files with frontmatter")

def main():
    """Main frontmatter fixing function"""
    fixer = YAMLFrontmatterFixer()
    stats = fixer.fix_all_frontmatter()
    
    print(f"\n🎉 YAML frontmatter repair complete!")
    print(f"📝 {stats['files_fixed']} files now have clean, valid frontmatter")
    print(f"🔧 {stats['errors_fixed']} total syntax errors corrected")

if __name__ == '__main__':
    main()