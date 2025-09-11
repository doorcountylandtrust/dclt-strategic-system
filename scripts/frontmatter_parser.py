#!/usr/bin/env python3
"""
Frontmatter Parser Library for DCLT Strategic System

This module provides utilities for parsing YAML frontmatter from markdown files
and querying project data for strategic planning analysis.
"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class Project:
    """Represents a project/task with frontmatter metadata."""
    file_path: str
    title: str
    type: str
    category: str
    status: str
    priority: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    due_date: Optional[date] = None
    tags: Dict[str, List[str]] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    assignee: str = "TBD"
    gantt_display: bool = True
    raw_frontmatter: Dict[str, Any] = field(default_factory=dict)
    content: str = ""

class FrontmatterParser:
    """Parses and queries YAML frontmatter from markdown files."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.projects: List[Project] = []
        self.load_all_projects()
    
    def parse_date(self, date_str: Union[str, date, None]) -> Optional[date]:
        """Parse various date formats into date objects."""
        if not date_str:
            return None
        if isinstance(date_str, date):
            return date_str
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                try:
                    return datetime.strptime(date_str, "%m/%d/%Y").date()
                except ValueError:
                    return None
        return None
    
    def extract_frontmatter(self, file_path: Path) -> tuple[Dict[str, Any], str]:
        """Extract YAML frontmatter and content from a markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for frontmatter
            if not content.startswith('---'):
                return {}, content
            
            # Split frontmatter and content
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, content
            
            # Parse YAML frontmatter
            try:
                frontmatter = yaml.safe_load(parts[1])
                if not isinstance(frontmatter, dict):
                    return {}, content
                markdown_content = parts[2].strip()
                return frontmatter, markdown_content
            except yaml.YAMLError:
                return {}, content
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return {}, ""
    
    def create_project(self, file_path: Path, frontmatter: Dict[str, Any], content: str) -> Project:
        """Create a Project object from frontmatter data."""
        return Project(
            file_path=str(file_path),
            title=frontmatter.get('title', file_path.stem),
            type=frontmatter.get('type', 'unknown'),
            category=frontmatter.get('category', 'unknown'),
            status=frontmatter.get('status', 'unknown'),
            priority=frontmatter.get('priority', 'medium'),
            start_date=self.parse_date(frontmatter.get('start_date')),
            end_date=self.parse_date(frontmatter.get('end_date')),
            due_date=self.parse_date(frontmatter.get('due_date')),
            tags=frontmatter.get('tags', {}),
            dependencies=frontmatter.get('dependencies', []),
            assignee=frontmatter.get('assignee', 'TBD'),
            gantt_display=frontmatter.get('gantt_display', True),
            raw_frontmatter=frontmatter,
            content=content
        )
    
    def load_all_projects(self):
        """Load all projects with frontmatter from the data directory."""
        self.projects = []
        
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    frontmatter, content = self.extract_frontmatter(file_path)
                    
                    if frontmatter:  # Only include files with frontmatter
                        project = self.create_project(file_path, frontmatter, content)
                        self.projects.append(project)
    
    def query_projects(self, **filters) -> List[Project]:
        """Query projects with various filters."""
        results = self.projects.copy()
        
        # Filter by basic fields
        for field, value in filters.items():
            if field in ['title', 'type', 'category', 'status', 'priority', 'assignee']:
                if isinstance(value, list):
                    results = [p for p in results if getattr(p, field) in value]
                else:
                    results = [p for p in results if getattr(p, field) == value]
        
        return results
    
    def query_by_tags(self, tag_filters: Dict[str, List[str]]) -> List[Project]:
        """Query projects by tag categories."""
        results = []
        
        for project in self.projects:
            match = True
            for tag_category, required_tags in tag_filters.items():
                project_tags = project.tags.get(tag_category, [])
                if not any(tag in project_tags for tag in required_tags):
                    match = False
                    break
            
            if match:
                results.append(project)
        
        return results
    
    def query_by_date_range(self, start_date: Optional[date] = None, 
                           end_date: Optional[date] = None,
                           date_field: str = 'start_date') -> List[Project]:
        """Query projects by date range."""
        results = []
        
        for project in self.projects:
            project_date = getattr(project, date_field)
            if not project_date:
                continue
                
            if start_date and project_date < start_date:
                continue
            if end_date and project_date > end_date:
                continue
                
            results.append(project)
        
        return results
    
    def get_resource_assignments(self, quarter: Optional[str] = None) -> Dict[str, List[Project]]:
        """Get projects grouped by resource/team assignments."""
        resource_map = defaultdict(list)
        
        for project in self.projects:
            # Filter by quarter if specified
            if quarter:
                if not self.project_in_quarter(project, quarter):
                    continue
            
            # Group by resource tags
            resource_tags = project.tags.get('resource', [])
            if resource_tags:
                for resource in resource_tags:
                    resource_map[resource].append(project)
            else:
                resource_map['unassigned'].append(project)
        
        return dict(resource_map)
    
    def project_in_quarter(self, project: Project, quarter: str) -> bool:
        """Check if a project is active in the specified quarter."""
        quarter_tags = project.tags.get('temporal', [])
        return quarter in quarter_tags
    
    def find_dependencies(self, project: Project) -> List[Project]:
        """Find projects that this project depends on."""
        dependencies = []
        for dep_name in project.dependencies:
            for other_project in self.projects:
                if other_project.title == dep_name or dep_name in other_project.title:
                    dependencies.append(other_project)
        return dependencies
    
    def find_dependents(self, project: Project) -> List[Project]:
        """Find projects that depend on this project."""
        dependents = []
        for other_project in self.projects:
            if (project.title in other_project.dependencies or 
                any(project.title in dep for dep in other_project.dependencies)):
                dependents.append(other_project)
        return dependents
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the project portfolio."""
        stats = {
            'total_projects': len(self.projects),
            'by_status': defaultdict(int),
            'by_priority': defaultdict(int),
            'by_type': defaultdict(int),
            'by_category': defaultdict(int),
            'by_quarter': defaultdict(int),
            'by_resource': defaultdict(int),
            'by_strategic': defaultdict(int)
        }
        
        for project in self.projects:
            stats['by_status'][project.status] += 1
            stats['by_priority'][project.priority] += 1
            stats['by_type'][project.type] += 1
            stats['by_category'][project.category] += 1
            
            # Count tag occurrences
            for quarter in project.tags.get('temporal', []):
                stats['by_quarter'][quarter] += 1
            for resource in project.tags.get('resource', []):
                stats['by_resource'][resource] += 1
            for strategic in project.tags.get('strategic', []):
                stats['by_strategic'][strategic] += 1
        
        return dict(stats)
    
    def export_to_dict(self) -> List[Dict[str, Any]]:
        """Export all projects as a list of dictionaries."""
        return [
            {
                'file_path': p.file_path,
                'title': p.title,
                'type': p.type,
                'category': p.category,
                'status': p.status,
                'priority': p.priority,
                'start_date': p.start_date.isoformat() if p.start_date else None,
                'end_date': p.end_date.isoformat() if p.end_date else None,
                'due_date': p.due_date.isoformat() if p.due_date else None,
                'tags': p.tags,
                'dependencies': p.dependencies,
                'assignee': p.assignee,
                'gantt_display': p.gantt_display
            }
            for p in self.projects
        ]

if __name__ == "__main__":
    # Example usage
    parser = FrontmatterParser()
    
    print(f"Loaded {len(parser.projects)} projects with frontmatter")
    
    # Example queries
    high_priority = parser.query_projects(priority='high')
    print(f"High priority projects: {len(high_priority)}")
    
    communications_q4 = parser.query_by_tags({
        'resource': ['communications-team'],
        'temporal': ['Q4-2025']
    })
    print(f"Communications team work in Q4 2025: {len(communications_q4)}")
    
    stats = parser.get_statistics()
    print("Project statistics:", stats)