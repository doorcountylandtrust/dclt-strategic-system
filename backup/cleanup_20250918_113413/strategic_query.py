#!/usr/bin/env python3
"""
Strategic Planning Query Tool for DCLT Strategic System

This script provides a flexible query interface for answering strategic planning
questions using natural language queries and structured data analysis.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional, Any

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))
from frontmatter_parser import FrontmatterParser, Project

class StrategicQueryEngine:
    """Natural language query engine for strategic planning questions."""
    
    def __init__(self, parser: FrontmatterParser):
        self.parser = parser
        self.projects = parser.projects
        
        # Query pattern definitions
        self.query_patterns = {
            'resource_workload': [
                r'what work requires? (\w+(?:-\w+)*)(?: in (\w+(?:-\w+)*))?',
                r'show (\w+(?:-\w+)*) work(?: for (\w+(?:-\w+)*))?',
                r'(\w+(?:-\w+)*) projects(?: in (\w+(?:-\w+)*))?'
            ],
            'timeline': [
                r'what.+in (Q\d+-\d{4})',
                r'projects.+(\d{4})',
                r'timeline for (.+)',
                r'schedule.+(\w+(?:-\w+)*)'
            ],
            'dependencies': [
                r'dependencies between (\w+) and (\w+)',
                r'show dependencies.+(\w+)',
                r'what depends on (.+)',
                r'(\w+) dependencies'
            ],
            'conflicts': [
                r'resource conflicts?',
                r'capacity issues?',
                r'workload conflicts?',
                r'overlapping projects?'
            ],
            'priority': [
                r'high priority.+(\w+)',
                r'critical projects?',
                r'urgent.+(\w+)'
            ],
            'strategic': [
                r'(\w+(?:-\w+)*) initiative',
                r'strategic.+(\w+)',
                r'(\w+) campaign'
            ]
        }
    
    def query(self, question: str, output_file: str = None) -> Dict[str, Any]:
        """Process a natural language query and return structured results."""
        question_lower = question.lower().strip()
        
        # Determine query type and extract parameters
        query_type, parameters = self._parse_query(question_lower)
        
        # Execute appropriate analysis
        results = {
            'query': question,
            'query_type': query_type,
            'parameters': parameters,
            'timestamp': datetime.now().isoformat(),
            'data': {},
            'summary': '',
            'recommendations': []
        }
        
        if query_type == 'resource_workload':
            results['data'] = self._analyze_resource_workload(parameters)
            results['summary'] = self._summarize_resource_workload(results['data'], parameters)
        
        elif query_type == 'timeline':
            results['data'] = self._analyze_timeline(parameters)
            results['summary'] = self._summarize_timeline(results['data'], parameters)
        
        elif query_type == 'dependencies':
            results['data'] = self._analyze_dependencies(parameters)
            results['summary'] = self._summarize_dependencies(results['data'], parameters)
        
        elif query_type == 'conflicts':
            results['data'] = self._analyze_conflicts()
            results['summary'] = self._summarize_conflicts(results['data'])
        
        elif query_type == 'priority':
            results['data'] = self._analyze_priority(parameters)
            results['summary'] = self._summarize_priority(results['data'], parameters)
        
        elif query_type == 'strategic':
            results['data'] = self._analyze_strategic_initiative(parameters)
            results['summary'] = self._summarize_strategic(results['data'], parameters)
        
        else:
            results['data'] = self._general_search(question_lower)
            results['summary'] = self._summarize_general_search(results['data'], question)
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        # Save results if output file specified
        if output_file:
            self._save_results(results, output_file)
        
        return results
    
    def _parse_query(self, question: str) -> Tuple[str, Dict[str, Any]]:
        """Parse natural language query to determine type and parameters."""
        
        for query_type, patterns in self.query_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, question)
                if match:
                    parameters = {
                        'matches': match.groups(),
                        'full_match': match.group(0)
                    }
                    return query_type, parameters
        
        return 'general', {'search_terms': question.split()}
    
    def _analyze_resource_workload(self, parameters: Dict) -> Dict[str, Any]:
        """Analyze workload for specific resources."""
        matches = parameters.get('matches', [])
        resource = matches[0] if matches else None
        quarter = matches[1] if len(matches) > 1 else None
        
        if resource:
            # Normalize resource name
            resource = resource.replace(' ', '-').lower()
        
        filtered_projects = []
        
        for project in self.projects:
            # Filter by resource
            if resource:
                project_resources = [r.lower() for r in project.tags.get('resource', [])]
                if resource not in project_resources and not any(resource in r for r in project_resources):
                    continue
            
            # Filter by quarter
            if quarter:
                project_quarters = [q.lower() for q in project.tags.get('temporal', [])]
                if quarter.lower() not in project_quarters:
                    continue
            
            filtered_projects.append(project)
        
        # Analyze the filtered projects
        analysis = {
            'total_projects': len(filtered_projects),
            'resource_filter': resource,
            'quarter_filter': quarter,
            'projects': [],
            'by_priority': defaultdict(int),
            'by_category': defaultdict(int),
            'by_status': defaultdict(int),
            'timeline_distribution': defaultdict(list)
        }
        
        for project in filtered_projects:
            analysis['projects'].append({
                'title': project.title,
                'priority': project.priority,
                'status': project.status,
                'category': project.category,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'tags': project.tags
            })
            
            analysis['by_priority'][project.priority] += 1
            analysis['by_category'][project.category] += 1
            analysis['by_status'][project.status] += 1
            
            if project.start_date:
                month_key = f"{project.start_date.year}-{project.start_date.month:02d}"
                analysis['timeline_distribution'][month_key].append(project.title)
        
        return analysis
    
    def _analyze_timeline(self, parameters: Dict) -> Dict[str, Any]:
        """Analyze project timeline for specific periods."""
        matches = parameters.get('matches', [])
        time_filter = matches[0] if matches else None
        
        filtered_projects = []
        
        for project in self.projects:
            if time_filter:
                # Quarter filter (e.g., Q3-2025)
                if re.match(r'Q\d+-\d{4}', time_filter):
                    project_quarters = project.tags.get('temporal', [])
                    if time_filter not in project_quarters:
                        continue
                
                # Year filter
                elif time_filter.isdigit():
                    if project.start_date and str(project.start_date.year) != time_filter:
                        continue
                
                # Month filter or other patterns
                else:
                    if project.start_date:
                        project_date_str = project.start_date.strftime('%B %Y').lower()
                        if time_filter.lower() not in project_date_str:
                            continue
            
            filtered_projects.append(project)
        
        # Sort by start date
        filtered_projects.sort(key=lambda p: p.start_date if p.start_date else date.max)
        
        analysis = {
            'time_filter': time_filter,
            'total_projects': len(filtered_projects),
            'timeline': [],
            'resource_utilization': defaultdict(list),
            'critical_milestones': [],
            'potential_conflicts': []
        }
        
        for project in filtered_projects:
            timeline_entry = {
                'title': project.title,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'priority': project.priority,
                'resources': project.tags.get('resource', []),
                'status': project.status
            }
            analysis['timeline'].append(timeline_entry)
            
            # Track resource utilization
            for resource in project.tags.get('resource', []):
                analysis['resource_utilization'][resource].append({
                    'project': project.title,
                    'start_date': project.start_date.isoformat() if project.start_date else None,
                    'end_date': project.end_date.isoformat() if project.end_date else None
                })
            
            # Identify critical milestones
            if project.priority == 'high' and project.end_date:
                analysis['critical_milestones'].append({
                    'project': project.title,
                    'milestone_date': project.end_date.isoformat(),
                    'type': 'project_completion'
                })
        
        return analysis
    
    def _analyze_dependencies(self, parameters: Dict) -> Dict[str, Any]:
        """Analyze project dependencies."""
        matches = parameters.get('matches', [])
        
        if len(matches) >= 2:
            # Specific dependency between two areas
            area1, area2 = matches[0], matches[1]
            return self._analyze_cross_area_dependencies(area1, area2)
        elif len(matches) == 1:
            # Dependencies for specific area or project
            target = matches[0]
            return self._analyze_target_dependencies(target)
        else:
            # General dependency analysis
            return self._analyze_all_dependencies()
    
    def _analyze_cross_area_dependencies(self, area1: str, area2: str) -> Dict[str, Any]:
        """Analyze dependencies between two specific areas (e.g., brand and website)."""
        area1_projects = []
        area2_projects = []
        
        for project in self.projects:
            functional_tags = [tag.lower() for tag in project.tags.get('functional', [])]
            
            if area1.lower() in functional_tags or area1.lower() in project.category.lower():
                area1_projects.append(project)
            
            if area2.lower() in functional_tags or area2.lower() in project.category.lower():
                area2_projects.append(project)
        
        dependencies = []
        implicit_dependencies = []
        
        # Find explicit and implicit dependencies
        for proj1 in area1_projects:
            for proj2 in area2_projects:
                # Check explicit dependencies
                if proj1.title in proj2.dependencies or proj2.title in proj1.dependencies:
                    dependencies.append({
                        'from': proj1.title if proj1.title in proj2.dependencies else proj2.title,
                        'to': proj2.title if proj1.title in proj2.dependencies else proj1.title,
                        'type': 'explicit',
                        'area_from': area1 if proj1.title in proj2.dependencies else area2,
                        'area_to': area2 if proj1.title in proj2.dependencies else area1
                    })
                
                # Check for implicit dependencies (timeline-based)
                elif (proj1.start_date and proj2.start_date and 
                      proj1.end_date and proj2.start_date >= proj1.end_date):
                    implicit_dependencies.append({
                        'from': proj1.title,
                        'to': proj2.title,
                        'type': 'implicit_temporal',
                        'area_from': area1,
                        'area_to': area2
                    })
        
        return {
            'area1': area1,
            'area2': area2,
            'area1_projects': len(area1_projects),
            'area2_projects': len(area2_projects),
            'explicit_dependencies': dependencies,
            'implicit_dependencies': implicit_dependencies,
            'total_dependencies': len(dependencies) + len(implicit_dependencies),
            'area1_project_list': [p.title for p in area1_projects],
            'area2_project_list': [p.title for p in area2_projects]
        }
    
    def _analyze_target_dependencies(self, target: str) -> Dict[str, Any]:
        """Analyze dependencies for a specific target (project or area)."""
        matching_projects = []
        
        for project in self.projects:
            if (target.lower() in project.title.lower() or 
                target.lower() in project.category.lower() or
                target.lower() in [tag.lower() for tag in project.tags.get('functional', [])]):
                matching_projects.append(project)
        
        dependencies_in = []  # What these projects depend on
        dependencies_out = []  # What depends on these projects
        
        for project in matching_projects:
            # Dependencies in
            for dep in project.dependencies:
                dependencies_in.append({
                    'project': project.title,
                    'depends_on': dep,
                    'type': 'explicit'
                })
            
            # Dependencies out (find projects that depend on this one)
            for other_project in self.projects:
                if project.title in other_project.dependencies:
                    dependencies_out.append({
                        'project': other_project.title,
                        'depends_on': project.title,
                        'type': 'explicit'
                    })
        
        return {
            'target': target,
            'matching_projects': len(matching_projects),
            'project_list': [p.title for p in matching_projects],
            'dependencies_in': dependencies_in,
            'dependencies_out': dependencies_out,
            'total_incoming': len(dependencies_in),
            'total_outgoing': len(dependencies_out)
        }
    
    def _analyze_all_dependencies(self) -> Dict[str, Any]:
        """Analyze all project dependencies in the system."""
        all_deps = []
        projects_with_deps = 0
        
        for project in self.projects:
            if project.dependencies:
                projects_with_deps += 1
                for dep in project.dependencies:
                    all_deps.append({
                        'from': dep,
                        'to': project.title,
                        'to_priority': project.priority,
                        'to_category': project.category
                    })
        
        # Find most critical dependencies (high-priority projects with many dependencies)
        critical_deps = [dep for dep in all_deps if dep['to_priority'] == 'high']
        
        return {
            'total_dependencies': len(all_deps),
            'projects_with_dependencies': projects_with_deps,
            'dependency_list': all_deps,
            'critical_dependencies': critical_deps,
            'dependency_frequency': Counter(dep['from'] for dep in all_deps)
        }
    
    def _analyze_conflicts(self) -> Dict[str, Any]:
        """Analyze resource conflicts and capacity issues."""
        conflicts = {
            'resource_conflicts': defaultdict(list),
            'timeline_conflicts': [],
            'capacity_warnings': [],
            'high_risk_areas': []
        }
        
        # Resource conflicts - multiple projects using same resource simultaneously
        resource_timeline = defaultdict(list)
        
        for project in self.projects:
            if project.start_date and project.end_date:
                for resource in project.tags.get('resource', []):
                    resource_timeline[resource].append({
                        'project': project.title,
                        'start': project.start_date,
                        'end': project.end_date,
                        'priority': project.priority
                    })
        
        # Find overlapping projects per resource
        for resource, projects in resource_timeline.items():
            for i, proj1 in enumerate(projects):
                for proj2 in projects[i+1:]:
                    # Check for overlap
                    if proj1['start'] <= proj2['end'] and proj2['start'] <= proj1['end']:
                        conflicts['resource_conflicts'][resource].append({
                            'project1': proj1['project'],
                            'project2': proj2['project'],
                            'overlap_start': max(proj1['start'], proj2['start']).isoformat(),
                            'overlap_end': min(proj1['end'], proj2['end']).isoformat(),
                            'high_priority_conflict': proj1['priority'] == 'high' and proj2['priority'] == 'high'
                        })
        
        # Capacity warnings
        for resource, project_list in resource_timeline.items():
            if len(project_list) >= 5:
                conflicts['capacity_warnings'].append({
                    'resource': resource,
                    'total_projects': len(project_list),
                    'warning_level': 'high' if len(project_list) >= 10 else 'medium',
                    'recommendation': f'Review {resource} capacity and consider additional resources'
                })
        
        return dict(conflicts)
    
    def _analyze_priority(self, parameters: Dict) -> Dict[str, Any]:
        """Analyze high priority projects and critical work."""
        matches = parameters.get('matches', [])
        focus_area = matches[0] if matches else None
        
        high_priority_projects = [p for p in self.projects if p.priority == 'high']
        
        if focus_area:
            high_priority_projects = [
                p for p in high_priority_projects 
                if (focus_area.lower() in p.category.lower() or
                    focus_area.lower() in [tag.lower() for tag in p.tags.get('functional', [])])
            ]
        
        analysis = {
            'focus_area': focus_area,
            'total_high_priority': len(high_priority_projects),
            'projects': [],
            'resource_demands': defaultdict(int),
            'timeline_concentration': defaultdict(int),
            'strategic_alignment': defaultdict(int)
        }
        
        for project in high_priority_projects:
            analysis['projects'].append({
                'title': project.title,
                'category': project.category,
                'status': project.status,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'resources': project.tags.get('resource', []),
                'strategic_tags': project.tags.get('strategic', [])
            })
            
            # Resource demand analysis
            for resource in project.tags.get('resource', []):
                analysis['resource_demands'][resource] += 1
            
            # Timeline concentration
            if project.start_date:
                quarter = f"Q{((project.start_date.month - 1) // 3) + 1}-{project.start_date.year}"
                analysis['timeline_concentration'][quarter] += 1
            
            # Strategic alignment
            for strategic_tag in project.tags.get('strategic', []):
                analysis['strategic_alignment'][strategic_tag] += 1
        
        return analysis
    
    def _analyze_strategic_initiative(self, parameters: Dict) -> Dict[str, Any]:
        """Analyze projects by strategic initiative."""
        matches = parameters.get('matches', [])
        initiative = matches[0] if matches else None
        
        if initiative:
            initiative = initiative.lower().replace(' ', '-')
        
        initiative_projects = []
        
        for project in self.projects:
            strategic_tags = [tag.lower() for tag in project.tags.get('strategic', [])]
            
            if not initiative:
                # Return all strategic projects
                if strategic_tags:
                    initiative_projects.append(project)
            else:
                # Filter by specific initiative
                if initiative in strategic_tags or any(initiative in tag for tag in strategic_tags):
                    initiative_projects.append(project)
        
        analysis = {
            'initiative_filter': initiative,
            'total_projects': len(initiative_projects),
            'projects': [],
            'timeline_distribution': defaultdict(list),
            'resource_allocation': defaultdict(int),
            'priority_breakdown': defaultdict(int),
            'completion_status': defaultdict(int)
        }
        
        for project in initiative_projects:
            project_data = {
                'title': project.title,
                'category': project.category,
                'priority': project.priority,
                'status': project.status,
                'start_date': project.start_date.isoformat() if project.start_date else None,
                'end_date': project.end_date.isoformat() if project.end_date else None,
                'strategic_tags': project.tags.get('strategic', []),
                'resources': project.tags.get('resource', [])
            }
            analysis['projects'].append(project_data)
            
            # Timeline distribution
            for quarter in project.tags.get('temporal', []):
                analysis['timeline_distribution'][quarter].append(project.title)
            
            # Resource allocation
            for resource in project.tags.get('resource', []):
                analysis['resource_allocation'][resource] += 1
            
            # Priority and status breakdowns
            analysis['priority_breakdown'][project.priority] += 1
            analysis['completion_status'][project.status] += 1
        
        return analysis
    
    def _general_search(self, search_terms: str) -> Dict[str, Any]:
        """Perform general search across all project data."""
        terms = search_terms.split()
        matching_projects = []
        
        for project in self.projects:
            # Search in title, category, and content
            searchable_text = f"{project.title} {project.category} {project.content}".lower()
            
            # Also search in tags
            all_tags = []
            for tag_category, tag_list in project.tags.items():
                all_tags.extend(tag_list)
            searchable_text += " " + " ".join(all_tags).lower()
            
            # Check if any search terms match
            if any(term in searchable_text for term in terms):
                matching_projects.append(project)
        
        return {
            'search_terms': terms,
            'total_matches': len(matching_projects),
            'projects': [
                {
                    'title': p.title,
                    'category': p.category,
                    'priority': p.priority,
                    'status': p.status,
                    'tags': p.tags
                }
                for p in matching_projects
            ]
        }
    
    def _summarize_resource_workload(self, data: Dict, parameters: Dict) -> str:
        """Generate summary for resource workload analysis."""
        resource = data.get('resource_filter', 'specified resource')
        quarter = data.get('quarter_filter', 'all quarters')
        total = data.get('total_projects', 0)
        
        summary = f"Found {total} projects for {resource}"
        if quarter != 'all quarters':
            summary += f" in {quarter}"
        
        if total > 0:
            by_priority = data.get('by_priority', {})
            high_priority = by_priority.get('high', 0)
            
            summary += f". Breakdown: {high_priority} high priority"
            
            if by_priority.get('medium', 0) > 0:
                summary += f", {by_priority['medium']} medium priority"
            
            top_category = max(data.get('by_category', {}).items(), key=lambda x: x[1], default=('none', 0))
            if top_category[1] > 0:
                summary += f". Primary category: {top_category[0]} ({top_category[1]} projects)"
        
        return summary
    
    def _summarize_timeline(self, data: Dict, parameters: Dict) -> str:
        """Generate summary for timeline analysis."""
        time_filter = data.get('time_filter', 'specified period')
        total = data.get('total_projects', 0)
        
        summary = f"Found {total} projects"
        if time_filter:
            summary += f" in {time_filter}"
        
        if total > 0:
            critical_milestones = len(data.get('critical_milestones', []))
            if critical_milestones > 0:
                summary += f". {critical_milestones} critical milestones identified"
            
            resource_util = data.get('resource_utilization', {})
            if resource_util:
                busiest_resource = max(resource_util.items(), key=lambda x: len(x[1]))[0]
                summary += f". Busiest resource: {busiest_resource}"
        
        return summary
    
    def _summarize_dependencies(self, data: Dict, parameters: Dict) -> str:
        """Generate summary for dependency analysis."""
        if 'area1' in data and 'area2' in data:
            # Cross-area analysis
            area1, area2 = data['area1'], data['area2']
            explicit = len(data.get('explicit_dependencies', []))
            implicit = len(data.get('implicit_dependencies', []))
            
            summary = f"Dependencies between {area1} and {area2}: {explicit} explicit, {implicit} implicit"
        
        elif 'target' in data:
            # Target-specific analysis
            target = data['target']
            incoming = data.get('total_incoming', 0)
            outgoing = data.get('total_outgoing', 0)
            
            summary = f"{target} dependencies: {incoming} incoming, {outgoing} outgoing"
        
        else:
            # General analysis
            total = data.get('total_dependencies', 0)
            projects_with_deps = data.get('projects_with_dependencies', 0)
            
            summary = f"Total system dependencies: {total} across {projects_with_deps} projects"
        
        return summary
    
    def _summarize_conflicts(self, data: Dict) -> str:
        """Generate summary for conflict analysis."""
        resource_conflicts = sum(len(conflicts) for conflicts in data.get('resource_conflicts', {}).values())
        capacity_warnings = len(data.get('capacity_warnings', []))
        
        summary = f"Resource analysis: {resource_conflicts} resource conflicts, {capacity_warnings} capacity warnings"
        
        if capacity_warnings > 0:
            high_warnings = sum(1 for w in data.get('capacity_warnings', []) if w.get('warning_level') == 'high')
            if high_warnings > 0:
                summary += f" ({high_warnings} high priority)"
        
        return summary
    
    def _summarize_priority(self, data: Dict, parameters: Dict) -> str:
        """Generate summary for priority analysis."""
        focus_area = data.get('focus_area')
        total = data.get('total_high_priority', 0)
        
        summary = f"High priority projects"
        if focus_area:
            summary += f" in {focus_area}"
        summary += f": {total}"
        
        if total > 0:
            resource_demands = data.get('resource_demands', {})
            if resource_demands:
                top_resource = max(resource_demands.items(), key=lambda x: x[1])
                summary += f". Top resource demand: {top_resource[0]} ({top_resource[1]} projects)"
        
        return summary
    
    def _summarize_strategic(self, data: Dict, parameters: Dict) -> str:
        """Generate summary for strategic initiative analysis."""
        initiative = data.get('initiative_filter', 'strategic initiatives')
        total = data.get('total_projects', 0)
        
        summary = f"{initiative}: {total} projects"
        
        if total > 0:
            priority_breakdown = data.get('priority_breakdown', {})
            high_priority = priority_breakdown.get('high', 0)
            if high_priority > 0:
                summary += f", {high_priority} high priority"
            
            completion_status = data.get('completion_status', {})
            completed = completion_status.get('complete', 0)
            in_progress = completion_status.get('in_progress', 0)
            
            summary += f". Status: {completed} complete, {in_progress} in progress"
        
        return summary
    
    def _summarize_general_search(self, data: Dict, question: str) -> str:
        """Generate summary for general search results."""
        total = data.get('total_matches', 0)
        search_terms = data.get('search_terms', [])
        
        summary = f"Search for '{' '.join(search_terms)}': {total} matching projects"
        
        if total > 0:
            projects = data.get('projects', [])
            categories = Counter(p.get('category', 'unknown') for p in projects)
            top_category = categories.most_common(1)[0] if categories else ('none', 0)
            
            summary += f". Top category: {top_category[0]} ({top_category[1]} projects)"
        
        return summary
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on query results."""
        recommendations = []
        query_type = results.get('query_type')
        data = results.get('data', {})
        
        if query_type == 'resource_workload':
            total_projects = data.get('total_projects', 0)
            if total_projects > 10:
                recommendations.append("Consider redistributing workload or adding resources due to high project volume")
            
            high_priority = data.get('by_priority', {}).get('high', 0)
            if high_priority > 3:
                recommendations.append("Review high priority project sequencing to avoid resource conflicts")
        
        elif query_type == 'conflicts':
            resource_conflicts = data.get('resource_conflicts', {})
            if resource_conflicts:
                recommendations.append("Schedule coordination meetings for overlapping project resources")
            
            capacity_warnings = data.get('capacity_warnings', [])
            high_warnings = [w for w in capacity_warnings if w.get('warning_level') == 'high']
            if high_warnings:
                recommendations.append("Address high-capacity warnings with additional staffing or project sequencing")
        
        elif query_type == 'dependencies':
            if 'explicit_dependencies' in data and data.get('total_dependencies', 0) > 5:
                recommendations.append("Create dependency tracking system to monitor critical path changes")
            
            if data.get('total_outgoing', 0) > 3:
                recommendations.append("Monitor bottleneck projects that block multiple other initiatives")
        
        elif query_type == 'priority':
            total_high = data.get('total_high_priority', 0)
            if total_high > 5:
                recommendations.append("Review priority assignments to ensure realistic execution capacity")
            
            resource_demands = data.get('resource_demands', {})
            overloaded_resources = [r for r, count in resource_demands.items() if count > 3]
            if overloaded_resources:
                recommendations.append(f"Address capacity concerns for: {', '.join(overloaded_resources)}")
        
        return recommendations
    
    def _save_results(self, results: Dict, output_file: str):
        """Save query results to output file."""
        output_path = Path("output/reports") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate formatted report
        report_lines = [
            "# Strategic Query Results",
            f"**Query:** {results['query']}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Query Type:** {results['query_type']}",
            "",
            "## Summary",
            results['summary'],
            ""
        ]
        
        # Add recommendations
        if results.get('recommendations'):
            report_lines.extend([
                "## Recommendations",
                ""
            ])
            for i, rec in enumerate(results['recommendations'], 1):
                report_lines.append(f"{i}. {rec}")
            report_lines.append("")
        
        # Add detailed data
        report_lines.extend([
            "## Detailed Results",
            "```json"
        ])
        
        import json
        report_lines.append(json.dumps(results['data'], indent=2, default=str))
        report_lines.append("```")
        
        report_content = "\n".join(report_lines)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Query results saved to: {output_path}")

def main():
    """Main execution function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Strategic planning query tool for DCLT Strategic System")
    parser.add_argument("query", help="Natural language query (use quotes for multi-word queries)")
    parser.add_argument("--output", help="Output filename for results")
    parser.add_argument("--format", choices=['summary', 'detailed'], default='summary',
                       help="Output format (default: summary)")
    
    args = parser.parse_args()
    
    # Initialize parser and query engine
    fm_parser = FrontmatterParser()
    query_engine = StrategicQueryEngine(fm_parser)
    
    print(f"Processing query: '{args.query}'")
    
    # Execute query
    results = query_engine.query(args.query, args.output)
    
    # Display results
    print("\n" + "="*60)
    print("QUERY RESULTS")
    print("="*60)
    print(f"Query Type: {results['query_type']}")
    print(f"Summary: {results['summary']}")
    
    if results.get('recommendations'):
        print("\nRecommendations:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"{i}. {rec}")
    
    if args.format == 'detailed':
        print(f"\nDetailed Data:")
        import json
        print(json.dumps(results['data'], indent=2, default=str))

if __name__ == "__main__":
    main()