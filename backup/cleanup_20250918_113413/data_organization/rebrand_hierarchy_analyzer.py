#!/usr/bin/env python3
"""
Rebrand Project Hierarchy Analyzer
Identifies parent-child relationships in brand system projects
"""

import os
import yaml
import json
from pathlib import Path
import re
from datetime import datetime

class RebrandHierarchyAnalyzer:
    def __init__(self, data_dir="data/dclt"):
        self.data_dir = data_dir
        self.brand_projects = []
        self.hierarchy_map = {}
        
    def analyze_brand_projects(self):
        """Analyze brand project structure and relationships"""
        print("🔍 Analyzing Brand System project hierarchy...")
        
        # Find all brand-related files
        brand_files = self.find_brand_files()
        
        # Analyze each file for content and relationships
        for file_path in brand_files:
            project_data = self.analyze_project_file(file_path)
            if project_data:
                self.brand_projects.append(project_data)
        
        # Build hierarchy map
        self.build_hierarchy_map()
        
        # Generate recommendations
        self.generate_hierarchy_recommendations()
        
        return self.hierarchy_map
    
    def find_brand_files(self):
        """Find all brand-related markdown files"""
        brand_files = []
        
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    
                    # Check if brand-related by path or content
                    if self.is_brand_related(file_path):
                        brand_files.append(file_path)
        
        print(f"📋 Found {len(brand_files)} brand-related files")
        return brand_files
    
    def is_brand_related(self, file_path):
        """Check if file is brand-related"""
        # Check file path
        brand_keywords = [
            'brand system', 'brand', 'logo', 'visual identity', 
            'rebrand', 'creative direction', 'brand audit',
            'moodboard', 'focus group', 'brand delivery'
        ]
        
        path_lower = file_path.lower()
        for keyword in brand_keywords:
            if keyword in path_lower:
                return True
        
        # Check file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                for keyword in brand_keywords:
                    if keyword in content:
                        return True
        except:
            pass
        
        return False
    
    def analyze_project_file(self, file_path):
        """Analyze individual project file for hierarchy clues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter = self.extract_frontmatter(content)
            
            # Determine project level and relationships
            project_data = {
                'file_path': file_path,
                'relative_path': os.path.relpath(file_path, self.data_dir),
                'title': frontmatter.get('title', os.path.basename(file_path).replace('.md', '')),
                'frontmatter': frontmatter,
                'content': content,
                'inferred_level': self.infer_project_level(file_path, content),
                'potential_parent': self.infer_parent_project(file_path, content),
                'timeline_info': self.extract_timeline_info(frontmatter, content),
                'dependencies': self.extract_dependencies(content)
            }
            
            return project_data
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
            return None
    
    def extract_frontmatter(self, content):
        """Extract YAML frontmatter"""
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
    
    def infer_project_level(self, file_path, content):
        """Infer project hierarchy level"""
        path_parts = file_path.split(os.sep)
        
        # Epic level - main brand system
        if 'Brand System (2026).md' in file_path:
            return 'epic'
        
        # Project level - major components
        major_components = [
            'Creative Direction', 'Logo & Visual Identity', 'Brand Audit',
            'Focus Group', 'Moodboard Exploration', 'System Elements',
            'Brand Delivery Kit', 'Feedback Rounds'
        ]
        
        filename = os.path.basename(file_path)
        for component in major_components:
            if component.lower() in filename.lower():
                return 'project'
        
        # Task level - specific deliverables
        task_indicators = [
            'Notes', 'Timeline', 'Concept', 'Evaluation', 'Summary',
            'Kickoff', 'Analysis', 'Tracker', 'Overview'
        ]
        
        for indicator in task_indicators:
            if indicator.lower() in filename.lower():
                return 'task'
        
        # Subtask level - deep nested items
        if len(path_parts) > 6:  # Deep nesting
            return 'subtask'
        
        return 'task'  # Default
    
    def infer_parent_project(self, file_path, content):
        """Infer parent project from file structure"""
        path_parts = file_path.split(os.sep)
        
        # Find Brand System reference
        for i, part in enumerate(path_parts):
            if 'Brand System' in part:
                if i + 1 < len(path_parts):
                    # Parent is the immediate directory
                    parent_part = path_parts[i + 1]
                    if parent_part.startswith('—'):
                        parent_part = parent_part[1:].strip()
                    return parent_part
        
        # Default to Brand System (2026) if in brand hierarchy
        if 'Brand System' in file_path:
            return 'Brand System (2026)'
        
        return None
    
    def extract_timeline_info(self, frontmatter, content):
        """Extract timeline information"""
        timeline_info = {
            'start_date': frontmatter.get('start_date'),
            'end_date': frontmatter.get('end_date'),
            'duration_days': frontmatter.get('duration_days'),
            'estimated_duration': None
        }
        
        # Look for timeline clues in content
        timeline_patterns = [
            r'(\\d{1,2})\\s*(weeks?|months?|days?)',
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\\s*(\\d{4})',
            r'Q[1-4]\\s*(\\d{4})'
        ]
        
        for pattern in timeline_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                timeline_info['content_timeline_refs'] = matches
                break
        
        return timeline_info
    
    def extract_dependencies(self, content):
        """Extract dependency information from content"""
        dependencies = []
        
        # Look for dependency keywords
        dependency_patterns = [
            r'depends on ([^\\n\\.]+)',
            r'requires ([^\\n\\.]+)',
            r'after ([^\\n\\.]+)',
            r'following ([^\\n\\.]+)'
        ]
        
        for pattern in dependency_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            dependencies.extend(matches)
        
        return list(set(dependencies))  # Remove duplicates
    
    def build_hierarchy_map(self):
        """Build hierarchical map of brand projects"""
        print("🏗️ Building project hierarchy map...")
        
        # Group by project level
        by_level = {
            'epic': [],
            'project': [], 
            'task': [],
            'subtask': []
        }
        
        for project in self.brand_projects:
            level = project['inferred_level']
            by_level[level].append(project)
        
        # Build parent-child relationships
        self.hierarchy_map = {
            'epic_projects': by_level['epic'],
            'projects': by_level['project'],
            'tasks': by_level['task'],
            'subtasks': by_level['subtask'],
            'relationships': self.build_relationships()
        }
        
        print(f"📊 Hierarchy summary:")
        print(f"  Epic projects: {len(by_level['epic'])}")
        print(f"  Projects: {len(by_level['project'])}")
        print(f"  Tasks: {len(by_level['task'])}")
        print(f"  Subtasks: {len(by_level['subtask'])}")
    
    def build_relationships(self):
        """Build parent-child relationships"""
        relationships = []
        
        for project in self.brand_projects:
            if project['potential_parent']:
                relationships.append({
                    'child': project['title'],
                    'child_path': project['relative_path'],
                    'parent': project['potential_parent'],
                    'level': project['inferred_level']
                })
        
        return relationships
    
    def generate_hierarchy_recommendations(self):
        """Generate recommendations for fixing hierarchy"""
        recommendations = []
        
        # Epic project recommendations
        if len(self.hierarchy_map.get('epic_projects', [])) == 0:
            recommendations.append({
                'priority': 'high',
                'issue': 'No epic project identified',
                'fix': 'Add project_type: "epic" to Brand System (2026).md'
            })
        
        # Timeline issues
        projects_missing_dates = []
        for project in self.brand_projects:
            timeline = project['timeline_info']
            if not timeline['start_date'] and not timeline['end_date']:
                projects_missing_dates.append(project['title'])
        
        if projects_missing_dates:
            recommendations.append({
                'priority': 'medium',
                'issue': f'{len(projects_missing_dates)} projects missing dates',
                'fix': 'Add start_date and end_date to frontmatter',
                'affected_files': projects_missing_dates[:5]  # Show first 5
            })
        
        # Parent-child relationships
        orphaned_projects = []
        for project in self.brand_projects:
            if project['inferred_level'] in ['task', 'subtask'] and not project['potential_parent']:
                orphaned_projects.append(project['title'])
        
        if orphaned_projects:
            recommendations.append({
                'priority': 'high',
                'issue': f'{len(orphaned_projects)} projects missing parent relationships',
                'fix': 'Add parent_project field to frontmatter',
                'affected_files': orphaned_projects[:5]
            })
        
        return recommendations
    
    def save_analysis_report(self, output_file="output/reports/rebrand_hierarchy_analysis.json"):
        """Save analysis report"""
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_brand_files': len(self.brand_projects),
            'hierarchy_map': self.hierarchy_map,
            'recommendations': self.generate_hierarchy_recommendations(),
            'project_details': [
                {
                    'title': p['title'],
                    'path': p['relative_path'],
                    'level': p['inferred_level'],
                    'parent': p['potential_parent'],
                    'has_timeline': bool(p['timeline_info']['start_date']),
                    'has_dependencies': len(p['dependencies']) > 0
                }
                for p in self.brand_projects
            ]
        }
        
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Analysis report saved: {output_file}")
        return report

def main():
    analyzer = RebrandHierarchyAnalyzer()
    hierarchy_map = analyzer.analyze_brand_projects()
    report = analyzer.save_analysis_report()
    
    print("\\n🎯 Key Findings:")
    recommendations = analyzer.generate_hierarchy_recommendations()
    for rec in recommendations:
        print(f"  {rec['priority'].upper()}: {rec['issue']}")
        print(f"    Fix: {rec['fix']}")
    
    return report

if __name__ == "__main__":
    main()