#!/usr/bin/env python3
"""
Resource Conflict Analyzer for DCLT Strategic System

This script identifies resource conflicts, capacity issues, and workload distribution
across teams and quarters to support strategic planning and resource allocation.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))
from frontmatter_parser import FrontmatterParser, Project

class ResourceConflictAnalyzer:
    """Analyzes resource conflicts and capacity issues across projects."""
    
    def __init__(self, parser: FrontmatterParser):
        self.parser = parser
        self.projects = parser.projects
        
    def analyze_resource_conflicts(self, quarter: str = None) -> Dict[str, any]:
        """Comprehensive resource conflict analysis."""
        
        # Filter projects by quarter if specified
        if quarter:
            projects = [p for p in self.projects if self.parser.project_in_quarter(p, quarter)]
            scope = f"Q{quarter[-1]} {quarter[:4]}" if "-" in quarter else quarter
        else:
            projects = self.projects
            scope = "All Quarters"
            
        analysis = {
            'scope': scope,
            'total_projects': len(projects),
            'resource_workload': self._analyze_resource_workload(projects),
            'concurrent_projects': self._find_concurrent_projects(projects),
            'capacity_warnings': self._identify_capacity_warnings(projects),
            'external_vendor_needs': self._analyze_external_vendor_needs(projects),
            'leadership_involvement': self._analyze_leadership_involvement(projects),
            'recommendations': []
        }
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_resource_workload(self, projects: List[Project]) -> Dict[str, Dict]:
        """Analyze workload distribution across resources."""
        workload = defaultdict(lambda: {
            'total_projects': 0,
            'high_priority': 0,
            'medium_priority': 0,
            'low_priority': 0,
            'projects': [],
            'categories': defaultdict(int)
        })
        
        for project in projects:
            resources = project.tags.get('resource', ['unassigned'])
            
            for resource in resources:
                workload[resource]['total_projects'] += 1
                workload[resource]['projects'].append({
                    'title': project.title,
                    'priority': project.priority,
                    'status': project.status,
                    'category': project.category,
                    'start_date': project.start_date.isoformat() if project.start_date else None,
                    'end_date': project.end_date.isoformat() if project.end_date else None
                })
                
                # Priority breakdown
                if project.priority == 'high':
                    workload[resource]['high_priority'] += 1
                elif project.priority == 'medium':
                    workload[resource]['medium_priority'] += 1
                else:
                    workload[resource]['low_priority'] += 1
                
                # Category breakdown
                workload[resource]['categories'][project.category] += 1
        
        return dict(workload)
    
    def _find_concurrent_projects(self, projects: List[Project]) -> Dict[str, List]:
        """Find projects running concurrently by resource."""
        concurrent = defaultdict(list)
        
        # Group projects by resource and find overlaps
        resource_projects = defaultdict(list)
        
        for project in projects:
            if not (project.start_date and project.end_date):
                continue
                
            resources = project.tags.get('resource', ['unassigned'])
            for resource in resources:
                resource_projects[resource].append(project)
        
        # Find overlapping projects for each resource
        for resource, resource_project_list in resource_projects.items():
            overlaps = []
            
            for i, proj1 in enumerate(resource_project_list):
                for proj2 in resource_project_list[i+1:]:
                    # Check for date overlap
                    if self._projects_overlap(proj1, proj2):
                        overlap_key = f"{proj1.title} + {proj2.title}"
                        overlaps.append({
                            'project1': proj1.title,
                            'project2': proj2.title,
                            'overlap_period': self._calculate_overlap_period(proj1, proj2),
                            'priority_conflict': proj1.priority == 'high' and proj2.priority == 'high'
                        })
            
            if overlaps:
                concurrent[resource] = overlaps
        
        return dict(concurrent)
    
    def _projects_overlap(self, proj1: Project, proj2: Project) -> bool:
        """Check if two projects have overlapping timelines."""
        if not all([proj1.start_date, proj1.end_date, proj2.start_date, proj2.end_date]):
            return False
            
        return (proj1.start_date <= proj2.end_date and proj2.start_date <= proj1.end_date)
    
    def _calculate_overlap_period(self, proj1: Project, proj2: Project) -> Dict[str, str]:
        """Calculate the overlap period between two projects."""
        if not self._projects_overlap(proj1, proj2):
            return {}
            
        overlap_start = max(proj1.start_date, proj2.start_date)
        overlap_end = min(proj1.end_date, proj2.end_date)
        
        return {
            'start': overlap_start.isoformat(),
            'end': overlap_end.isoformat(),
            'duration_days': (overlap_end - overlap_start).days + 1
        }
    
    def _identify_capacity_warnings(self, projects: List[Project]) -> List[Dict]:
        """Identify potential capacity and workload warnings."""
        warnings = []
        workload = self._analyze_resource_workload(projects)
        
        # High workload warnings
        for resource, data in workload.items():
            total_projects = data['total_projects']
            high_priority = data['high_priority']
            
            # Warning thresholds
            if total_projects >= 10:
                warnings.append({
                    'type': 'high_workload',
                    'resource': resource,
                    'issue': f"Very high workload: {total_projects} total projects",
                    'severity': 'high' if total_projects >= 15 else 'medium',
                    'recommendation': 'Consider redistributing workload or additional resources'
                })
            
            if high_priority >= 5:
                warnings.append({
                    'type': 'high_priority_overload',
                    'resource': resource,
                    'issue': f"Too many high priority projects: {high_priority}",
                    'severity': 'high',
                    'recommendation': 'Review priority assignments and consider sequencing'
                })
        
        # Single point of failure warnings
        critical_resources = ['communications-team', 'leadership']
        for resource in critical_resources:
            if resource in workload and workload[resource]['total_projects'] > 0:
                warnings.append({
                    'type': 'single_point_of_failure',
                    'resource': resource,
                    'issue': f"Critical dependency on {resource} for {workload[resource]['total_projects']} projects",
                    'severity': 'medium',
                    'recommendation': 'Develop backup capabilities and cross-training'
                })
        
        return warnings
    
    def _analyze_external_vendor_needs(self, projects: List[Project]) -> Dict[str, any]:
        """Analyze external vendor requirements and coordination needs."""
        vendor_projects = [p for p in projects if 'external-vendor' in p.tags.get('resource', [])]
        
        analysis = {
            'total_vendor_projects': len(vendor_projects),
            'vendor_categories': defaultdict(int),
            'vendor_timeline': defaultdict(list),
            'coordination_needs': []
        }
        
        for project in vendor_projects:
            # Category analysis
            analysis['vendor_categories'][project.category] += 1
            
            # Timeline analysis
            if project.start_date:
                quarter = self._get_quarter_from_date(project.start_date)
                analysis['vendor_timeline'][quarter].append({
                    'title': project.title,
                    'category': project.category,
                    'priority': project.priority
                })
        
        # Coordination needs
        if len(vendor_projects) >= 5:
            analysis['coordination_needs'].append({
                'type': 'vendor_coordination',
                'issue': f"{len(vendor_projects)} projects require external vendors",
                'recommendation': 'Establish vendor coordination process and timeline'
            })
        
        return analysis
    
    def _analyze_leadership_involvement(self, projects: List[Project]) -> Dict[str, any]:
        """Analyze leadership involvement and decision points."""
        leadership_projects = [p for p in projects if 'leadership' in p.tags.get('resource', [])]
        
        analysis = {
            'total_leadership_projects': len(leadership_projects),
            'decision_points': [],
            'strategic_oversight': []
        }
        
        for project in leadership_projects:
            if project.priority == 'high':
                analysis['decision_points'].append({
                    'title': project.title,
                    'category': project.category,
                    'timeline': f"{project.start_date} to {project.end_date}" if project.start_date and project.end_date else "TBD"
                })
            
            if any(tag in project.tags.get('strategic', []) for tag in ['rebrand', '40th-anniversary', 'capital-campaign']):
                analysis['strategic_oversight'].append({
                    'title': project.title,
                    'strategic_initiatives': project.tags.get('strategic', []),
                    'priority': project.priority
                })
        
        return analysis
    
    def _get_quarter_from_date(self, date_obj: date) -> str:
        """Get quarter string from date object."""
        quarter_num = (date_obj.month - 1) // 3 + 1
        return f"Q{quarter_num}-{date_obj.year}"
    
    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []
        
        # Resource workload recommendations
        workload = analysis['resource_workload']
        
        # Check for overloaded communications team
        if 'communications-team' in workload:
            comm_workload = workload['communications-team']['total_projects']
            if comm_workload >= 15:
                recommendations.append({
                    'category': 'resource_planning',
                    'priority': 'high',
                    'title': 'Communications Team Capacity Issue',
                    'description': f"Communications team assigned to {comm_workload} projects",
                    'action_items': [
                        'Consider hiring additional communications staff',
                        'Redistribute non-critical projects',
                        'Implement project sequencing to reduce concurrent workload'
                    ]
                })
        
        # Vendor coordination recommendations
        vendor_analysis = analysis['external_vendor_needs']
        if vendor_analysis['total_vendor_projects'] >= 5:
            recommendations.append({
                'category': 'vendor_management',
                'priority': 'medium',
                'title': 'Vendor Coordination Required',
                'description': f"{vendor_analysis['total_vendor_projects']} projects require external vendors",
                'action_items': [
                    'Establish vendor coordination process',
                    'Create vendor timeline and capacity planning',
                    'Identify backup vendors for critical projects'
                ]
            })
        
        # Leadership bandwidth recommendations
        leadership_analysis = analysis['leadership_involvement']
        if leadership_analysis['total_leadership_projects'] >= 5:
            recommendations.append({
                'category': 'leadership_planning',
                'priority': 'medium',
                'title': 'Leadership Decision Points',
                'description': f"{leadership_analysis['total_leadership_projects']} projects require leadership involvement",
                'action_items': [
                    'Schedule regular strategic decision meetings',
                    'Delegate decision authority where appropriate',
                    'Create decision frameworks for common issues'
                ]
            })
        
        return recommendations
    
    def generate_report(self, quarter: str = None, output_file: str = None) -> str:
        """Generate comprehensive resource conflict analysis report."""
        analysis = self.analyze_resource_conflicts(quarter)
        
        report_lines = [
            "# Resource Conflict Analysis Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Scope:** {analysis['scope']}",
            f"**Total Projects Analyzed:** {analysis['total_projects']}",
            "",
            "## Executive Summary",
            ""
        ]
        
        # Resource workload summary
        workload = analysis['resource_workload']
        report_lines.extend([
            "### Resource Workload Distribution",
            ""
        ])
        
        for resource, data in sorted(workload.items(), key=lambda x: x[1]['total_projects'], reverse=True):
            report_lines.append(f"**{resource.replace('-', ' ').title()}:**")
            report_lines.append(f"- Total Projects: {data['total_projects']}")
            report_lines.append(f"- High Priority: {data['high_priority']}")
            report_lines.append(f"- Medium Priority: {data['medium_priority']}")
            report_lines.append(f"- Categories: {', '.join([f'{cat} ({count})' for cat, count in data['categories'].items()])}")
            report_lines.append("")
        
        # Capacity warnings
        warnings = analysis['capacity_warnings']
        if warnings:
            report_lines.extend([
                "## Capacity Warnings",
                ""
            ])
            
            for warning in warnings:
                severity_icon = "🔴" if warning['severity'] == 'high' else "🟡"
                report_lines.append(f"{severity_icon} **{warning['type'].replace('_', ' ').title()}**")
                report_lines.append(f"   - Resource: {warning['resource']}")
                report_lines.append(f"   - Issue: {warning['issue']}")
                report_lines.append(f"   - Recommendation: {warning['recommendation']}")
                report_lines.append("")
        
        # Concurrent projects
        concurrent = analysis['concurrent_projects']
        if concurrent:
            report_lines.extend([
                "## Concurrent Project Conflicts",
                ""
            ])
            
            for resource, conflicts in concurrent.items():
                report_lines.append(f"### {resource.replace('-', ' ').title()}")
                for conflict in conflicts:
                    priority_flag = " ⚠️ **HIGH PRIORITY CONFLICT**" if conflict['priority_conflict'] else ""
                    report_lines.append(f"- **{conflict['project1']}** + **{conflict['project2']}**{priority_flag}")
                    if conflict['overlap_period']:
                        overlap = conflict['overlap_period']
                        report_lines.append(f"  - Overlap: {overlap['start']} to {overlap['end']} ({overlap['duration_days']} days)")
                    report_lines.append("")
        
        # Recommendations
        recommendations = analysis['recommendations']
        if recommendations:
            report_lines.extend([
                "## Strategic Recommendations",
                ""
            ])
            
            for i, rec in enumerate(recommendations, 1):
                priority_icon = "🔴" if rec['priority'] == 'high' else "🟡"
                report_lines.append(f"{i}. {priority_icon} **{rec['title']}** ({rec['category'].replace('_', ' ').title()})")
                report_lines.append(f"   {rec['description']}")
                report_lines.append("   **Action Items:**")
                for action in rec['action_items']:
                    report_lines.append(f"   - {action}")
                report_lines.append("")
        
        # External vendor analysis
        vendor_analysis = analysis['external_vendor_needs']
        if vendor_analysis['total_vendor_projects'] > 0:
            report_lines.extend([
                "## External Vendor Requirements",
                f"**Total Projects:** {vendor_analysis['total_vendor_projects']}",
                ""
            ])
            
            if vendor_analysis['vendor_categories']:
                report_lines.append("**By Category:**")
                for category, count in vendor_analysis['vendor_categories'].items():
                    report_lines.append(f"- {category.title()}: {count} projects")
                report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # Save to file if specified
        if output_file:
            output_path = Path("output/reports") / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"Resource conflict analysis saved to: {output_path}")
        
        return report_content

def main():
    """Main execution function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze resource conflicts in DCLT Strategic System")
    parser.add_argument("--quarter", help="Specific quarter to analyze (e.g., Q3-2025)")
    parser.add_argument("--output", default="resource_conflict_analysis.md", 
                       help="Output filename (default: resource_conflict_analysis.md)")
    
    args = parser.parse_args()
    
    # Initialize parser and analyzer
    fm_parser = FrontmatterParser()
    analyzer = ResourceConflictAnalyzer(fm_parser)
    
    # Generate report
    print(f"Analyzing resource conflicts...")
    if args.quarter:
        print(f"Focusing on {args.quarter}")
    
    report = analyzer.generate_report(quarter=args.quarter, output_file=args.output)
    
    print("\n" + "="*60)
    print("RESOURCE CONFLICT ANALYSIS SUMMARY")
    print("="*60)
    
    # Quick summary
    analysis = analyzer.analyze_resource_conflicts(args.quarter)
    workload = analysis['resource_workload']
    
    print(f"Total Projects: {analysis['total_projects']}")
    print(f"Resources Involved: {len(workload)}")
    print(f"Capacity Warnings: {len(analysis['capacity_warnings'])}")
    print(f"Vendor Projects: {analysis['external_vendor_needs']['total_vendor_projects']}")
    
    if workload:
        busiest_resource = max(workload.items(), key=lambda x: x[1]['total_projects'])
        print(f"Busiest Resource: {busiest_resource[0]} ({busiest_resource[1]['total_projects']} projects)")

if __name__ == "__main__":
    main()