#!/usr/bin/env python3
"""
Rebrand Project Hierarchy Fixer
Applies proper parent-child structure and timeline data to brand projects
"""

import os
import yaml
import json
from pathlib import Path
import re
from datetime import datetime, timedelta

class RebrandHierarchyFixer:
    def __init__(self, data_dir="data/dclt"):
        self.data_dir = data_dir
        self.analysis_file = "output/reports/rebrand_hierarchy_analysis.json"
        self.fixes_applied = []
        
        # Load analysis data
        with open(self.analysis_file, 'r') as f:
            self.analysis = json.load(f)
        
        # Define hierarchy schema
        self.hierarchy_schema = {
            'epic': {
                'project_type': 'epic',
                'start_date': '2025-07-01',
                'end_date': '2026-03-31',
                'duration_days': 273,
                'priority': 'critical'
            },
            'projects': {
                'Creative Direction': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-07-01',
                    'end_date': '2025-08-15',
                    'duration_days': 45,
                    'priority': 'high'
                },
                'Brand Audit Summary': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project', 
                    'start_date': '2025-07-01',
                    'end_date': '2025-07-30',
                    'duration_days': 29,
                    'priority': 'high'
                },
                'Logo & Visual Identity Evaluation Roadmap': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-08-01',
                    'end_date': '2025-10-15',
                    'duration_days': 75,
                    'priority': 'critical'
                },
                'Focus Group Participation & Feedback': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-08-15',
                    'end_date': '2025-09-15',
                    'duration_days': 31,
                    'priority': 'high'
                },
                'Moodboard Exploration': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-07-15',
                    'end_date': '2025-08-30',
                    'duration_days': 46,
                    'priority': 'medium'
                },
                'System Elements': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-09-01',
                    'end_date': '2025-11-15',
                    'duration_days': 75,
                    'priority': 'high'
                },
                'Feedback Rounds': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-09-15',
                    'end_date': '2025-12-01',
                    'duration_days': 77,
                    'priority': 'medium'
                },
                'Brand Delivery Kit': {
                    'parent_project': 'Brand System (2026)',
                    'project_type': 'project',
                    'start_date': '2025-11-15',
                    'end_date': '2026-01-31',
                    'duration_days': 77,
                    'priority': 'high'
                }
            }
        }
    
    def fix_rebrand_hierarchy(self):
        """Apply hierarchical fixes to all brand projects"""
        print("🔧 Fixing rebrand project hierarchy and timelines...")
        
        # Fix epic project first
        self.fix_epic_project()
        
        # Fix major project components
        self.fix_project_components()
        
        # Fix tasks and subtasks  
        self.fix_tasks_and_subtasks()
        
        # Generate summary
        self.generate_fix_summary()
        
        print(f"✅ Applied {len(self.fixes_applied)} hierarchical fixes")
        return self.fixes_applied
    
    def fix_epic_project(self):
        """Fix the main Brand System (2026) epic project"""
        epic_projects = self.analysis['hierarchy_map']['epic_projects']
        
        if epic_projects:
            epic = epic_projects[0]
            file_path = epic['file_path']
            
            print(f"🎯 Fixing epic project: {epic['title']}")
            
            # Update frontmatter
            updates = {
                'project_type': 'epic',
                'start_date': '2025-07-01',
                'end_date': '2026-03-31', 
                'duration_days': 273,
                'priority': 'critical',
                'progress_percent': 35,
                'epic_theme': 'Brand System Modernization',
                'epic_objectives': [
                    'Establish consistent brand identity',
                    'Improve digital presence',
                    'Enhance stakeholder experience'
                ],
                'child_projects': [
                    'Creative Direction',
                    'Brand Audit Summary',
                    'Logo & Visual Identity Evaluation Roadmap',
                    'Focus Group Participation & Feedback',
                    'Moodboard Exploration',
                    'System Elements',
                    'Feedback Rounds',
                    'Brand Delivery Kit'
                ],
                'assigned_to': ['Communications Team', 'External Brand Consultant'],
                'estimated_hours': 1200,
                'resource_type': 'strategic',
                'budget_allocated': 75000,
                'risk_level': 'high',
                'strategic_theme': 'Brand Excellence'
            }
            
            if self.update_file_frontmatter(file_path, updates):
                self.fixes_applied.append({
                    'type': 'epic_fix',
                    'file': file_path,
                    'updates': list(updates.keys())
                })
    
    def fix_project_components(self):
        """Fix major project components"""
        projects = self.analysis['hierarchy_map']['projects']
        
        for project in projects:
            title = project['title']
            file_path = project['file_path']
            
            # Find matching schema
            schema_match = None
            for schema_title, schema_data in self.hierarchy_schema['projects'].items():
                if schema_title.lower() in title.lower() or title.lower() in schema_title.lower():
                    schema_match = schema_data
                    break
            
            if schema_match:
                print(f"🔧 Fixing project: {title}")
                
                # Create updates based on schema
                updates = {
                    'project_type': 'project',
                    'parent_project': 'Brand System (2026)',
                    **schema_match
                }
                
                # Add additional project management fields
                updates.update({
                    'assigned_to': ['Communications Team'],
                    'resource_type': 'creative',
                    'strategic_theme': 'Brand Excellence'
                })
                
                if self.update_file_frontmatter(file_path, updates):
                    self.fixes_applied.append({
                        'type': 'project_fix',
                        'file': file_path,
                        'title': title,
                        'updates': list(updates.keys())
                    })
    
    def fix_tasks_and_subtasks(self):
        """Fix tasks and subtasks with parent relationships"""
        tasks = self.analysis['hierarchy_map']['tasks']
        subtasks = self.analysis['hierarchy_map']['subtasks']
        
        all_tasks = tasks + subtasks
        
        for task in all_tasks:
            title = task['title']
            file_path = task['file_path']
            potential_parent = task['potential_parent']
            level = task['inferred_level']
            
            if potential_parent and potential_parent != 'Brand System (2026)':
                print(f"🔗 Fixing task: {title}")
                
                # Determine timeline based on parent
                task_timeline = self.infer_task_timeline(potential_parent, title)
                
                updates = {
                    'project_type': level,
                    'parent_project': potential_parent,
                    'assigned_to': ['Communications Team'],
                    'resource_type': 'operational',
                    'strategic_theme': 'Brand Excellence'
                }
                
                # Add timeline if available
                if task_timeline:
                    updates.update(task_timeline)
                
                if self.update_file_frontmatter(file_path, updates):
                    self.fixes_applied.append({
                        'type': 'task_fix',
                        'file': file_path,
                        'title': title,
                        'parent': potential_parent,
                        'updates': list(updates.keys())
                    })
    
    def infer_task_timeline(self, parent_name, task_title):
        """Infer task timeline based on parent project"""
        # Find parent timeline
        parent_schema = self.hierarchy_schema['projects'].get(parent_name)
        if not parent_schema:
            return None
        
        parent_start = datetime.strptime(parent_schema['start_date'], '%Y-%m-%d')
        parent_end = datetime.strptime(parent_schema['end_date'], '%Y-%m-%d')
        parent_duration = (parent_end - parent_start).days
        
        # Estimate task timeline based on type
        task_patterns = {
            'kickoff': (0, 7),          # Start immediately, 1 week
            'concept': (7, 21),         # Week 2-3, 2 weeks  
            'evaluation': (21, 35),     # Week 4-5, 2 weeks
            'feedback': (28, 42),       # Week 5-6, 2 weeks
            'final': (parent_duration-14, parent_duration),  # Last 2 weeks
            'notes': (0, parent_duration),  # Span entire project
            'summary': (parent_duration-7, parent_duration),  # Last week
            'analysis': (parent_duration//2, parent_duration//2 + 14)  # Middle 2 weeks
        }
        
        # Find matching pattern
        task_lower = task_title.lower()
        for pattern, (start_offset, end_offset) in task_patterns.items():
            if pattern in task_lower:
                task_start = parent_start + timedelta(days=start_offset)
                task_end = parent_start + timedelta(days=end_offset)
                
                return {
                    'start_date': task_start.strftime('%Y-%m-%d'),
                    'end_date': task_end.strftime('%Y-%m-%d'),
                    'duration_days': (task_end - task_start).days
                }
        
        # Default: spread across parent timeline
        quarter_duration = parent_duration // 4
        task_start = parent_start + timedelta(days=quarter_duration)
        task_end = parent_end - timedelta(days=quarter_duration)
        
        return {
            'start_date': task_start.strftime('%Y-%m-%d'),
            'end_date': task_end.strftime('%Y-%m-%d'),
            'duration_days': (task_end - task_start).days
        }
    
    def update_file_frontmatter(self, file_path, updates):
        """Update file frontmatter with new fields"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract existing frontmatter
            frontmatter, body = self.split_frontmatter(content)
            
            # Update frontmatter
            for key, value in updates.items():
                frontmatter[key] = value
            
            # Update last_updated
            frontmatter['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            
            # Reconstruct file
            new_content = self.reconstruct_file(frontmatter, body)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to update {file_path}: {e}")
            return False
    
    def split_frontmatter(self, content):
        """Split content into frontmatter and body"""
        if not content.startswith('---'):
            return {}, content
        
        try:
            end_index = content.find('---', 3)
            if end_index == -1:
                return {}, content
            
            frontmatter_content = content[3:end_index].strip()
            body = content[end_index + 3:].strip()
            
            frontmatter = yaml.safe_load(frontmatter_content) or {}
            return frontmatter, body
            
        except:
            return {}, content
    
    def reconstruct_file(self, frontmatter, body):
        """Reconstruct file with updated frontmatter"""
        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        return f"---\\n{frontmatter_yaml}---\\n\\n{body}"
    
    def generate_fix_summary(self):
        """Generate summary of fixes applied"""
        summary = {
            'fix_timestamp': datetime.now().isoformat(),
            'total_fixes': len(self.fixes_applied),
            'fix_types': {
                'epic_fix': len([f for f in self.fixes_applied if f['type'] == 'epic_fix']),
                'project_fix': len([f for f in self.fixes_applied if f['type'] == 'project_fix']),
                'task_fix': len([f for f in self.fixes_applied if f['type'] == 'task_fix'])
            },
            'fixes_applied': self.fixes_applied
        }
        
        # Save summary
        summary_file = "output/reports/rebrand_hierarchy_fixes.json"
        Path(summary_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Fix summary saved: {summary_file}")
        
        # Print summary
        print("\\n📊 Fix Summary:")
        print(f"  Epic projects fixed: {summary['fix_types']['epic_fix']}")
        print(f"  Project components fixed: {summary['fix_types']['project_fix']}")  
        print(f"  Tasks/subtasks fixed: {summary['fix_types']['task_fix']}")
        print(f"  Total fixes applied: {summary['total_fixes']}")

def main():
    fixer = RebrandHierarchyFixer()
    fixes = fixer.fix_rebrand_hierarchy()
    
    print("\\n🎉 Rebrand hierarchy fixes complete!")
    print("   Brand projects now have proper parent-child relationships")
    print("   Timeline data applied for realistic Gantt visualization")
    print("   Ready for hierarchical project management views")
    
    return fixes

if __name__ == "__main__":
    main()