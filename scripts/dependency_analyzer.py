#!/usr/bin/env python3
"""
Project Dependency Analyzer for DCLT Strategic System

This script analyzes project dependencies, identifies critical paths, and maps
relationships between brand and website projects for strategic planning.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Optional

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))
from frontmatter_parser import FrontmatterParser, Project

class DependencyAnalyzer:
    """Analyzes project dependencies and critical paths."""
    
    def __init__(self, parser: FrontmatterParser):
        self.parser = parser
        self.projects = parser.projects
        self.dependency_graph = self._build_dependency_graph()
        
    def _build_dependency_graph(self) -> Dict[str, Dict]:
        """Build a comprehensive dependency graph."""
        graph = {}
        
        for project in self.projects:
            graph[project.title] = {
                'project': project,
                'dependencies': [],
                'dependents': [],
                'explicit_deps': project.dependencies.copy(),
                'implicit_deps': []
            }
        
        # Add explicit dependencies
        for project in self.projects:
            for dep_name in project.dependencies:
                matching_projects = self._find_matching_projects(dep_name)
                for dep_project in matching_projects:
                    if dep_project.title in graph and project.title in graph:
                        graph[project.title]['dependencies'].append(dep_project.title)
                        graph[dep_project.title]['dependents'].append(project.title)
        
        # Add implicit dependencies based on project relationships
        self._add_implicit_dependencies(graph)
        
        return graph
    
    def _find_matching_projects(self, dependency_name: str) -> List[Project]:
        """Find projects that match a dependency name or pattern."""
        matches = []
        
        for project in self.projects:
            # Exact match
            if project.title == dependency_name:
                matches.append(project)
            # Partial match
            elif dependency_name.lower() in project.title.lower():
                matches.append(project)
            # Category-based matching
            elif dependency_name.lower().replace(' ', '-') == project.category:
                matches.append(project)
        
        return matches
    
    def _add_implicit_dependencies(self, graph: Dict[str, Dict]):
        """Add implicit dependencies based on project relationships."""
        
        # Brand → Website dependencies
        brand_projects = [p for p in self.projects if 'brand' in p.tags.get('functional', [])]
        website_projects = [p for p in self.projects if 'website' in p.tags.get('functional', [])]
        
        for brand_proj in brand_projects:
            for website_proj in website_projects:
                # Brand system should come before website implementation
                if ('system' in brand_proj.title.lower() or 
                    'identity' in brand_proj.title.lower() or
                    'logo' in brand_proj.title.lower()):
                    
                    if ('development' in website_proj.title.lower() or
                        'implementation' in website_proj.title.lower() or
                        'build' in website_proj.title.lower()):
                        
                        if brand_proj.title not in graph[website_proj.title]['dependencies']:
                            graph[website_proj.title]['dependencies'].append(brand_proj.title)
                            graph[website_proj.title]['implicit_deps'].append(brand_proj.title)
                            graph[brand_proj.title]['dependents'].append(website_proj.title)
        
        # Strategy → Implementation dependencies
        strategy_projects = [p for p in self.projects if 'strategy' in p.type.lower() or 'planning' in p.type.lower()]
        implementation_projects = [p for p in self.projects if p.type in ['task', 'development_project']]
        
        for strategy_proj in strategy_projects:
            for impl_proj in implementation_projects:
                # Check for category alignment
                strategy_categories = strategy_proj.tags.get('functional', [])
                impl_categories = impl_proj.tags.get('functional', [])
                
                if any(cat in impl_categories for cat in strategy_categories):
                    if (strategy_proj.start_date and impl_proj.start_date and 
                        strategy_proj.start_date <= impl_proj.start_date):
                        
                        if strategy_proj.title not in graph[impl_proj.title]['dependencies']:
                            graph[impl_proj.title]['dependencies'].append(strategy_proj.title)
                            graph[impl_proj.title]['implicit_deps'].append(strategy_proj.title)
                            graph[strategy_proj.title]['dependents'].append(impl_proj.title)
    
    def find_critical_path(self) -> List[Tuple[str, int]]:
        """Find the critical path through the project network."""
        # Calculate earliest start times
        earliest_start = {}
        for project_title in self.dependency_graph:
            earliest_start[project_title] = self._calculate_earliest_start(project_title)
        
        # Find longest path (critical path)
        critical_path = []
        visited = set()
        
        def find_longest_path(current: str, path: List[str]) -> List[str]:
            if current in visited:
                return path
            
            visited.add(current)
            longest = path + [current]
            
            for dependent in self.dependency_graph[current]['dependents']:
                candidate = find_longest_path(dependent, path + [current])
                if len(candidate) > len(longest):
                    longest = candidate
            
            visited.remove(current)
            return longest
        
        # Start from projects with no dependencies
        root_projects = [title for title, data in self.dependency_graph.items() 
                        if not data['dependencies']]
        
        longest_overall = []
        for root in root_projects:
            path = find_longest_path(root, [])
            if len(path) > len(longest_overall):
                longest_overall = path
        
        # Convert to tuples with duration estimates
        critical_path = []
        for project_title in longest_overall:
            project = self.dependency_graph[project_title]['project']
            duration = self._estimate_project_duration(project)
            critical_path.append((project_title, duration))
        
        return critical_path
    
    def _calculate_earliest_start(self, project_title: str) -> int:
        """Calculate earliest start time for a project (in days from project start)."""
        project_data = self.dependency_graph[project_title]
        
        if not project_data['dependencies']:
            return 0
        
        max_predecessor_finish = 0
        for dep_title in project_data['dependencies']:
            dep_earliest = self._calculate_earliest_start(dep_title)
            dep_duration = self._estimate_project_duration(self.dependency_graph[dep_title]['project'])
            predecessor_finish = dep_earliest + dep_duration
            max_predecessor_finish = max(max_predecessor_finish, predecessor_finish)
        
        return max_predecessor_finish
    
    def _estimate_project_duration(self, project: Project) -> int:
        """Estimate project duration in days."""
        if project.start_date and project.end_date:
            return (project.end_date - project.start_date).days + 1
        
        # Default duration estimates by type
        duration_map = {
            'task': 5,
            'campaign': 90,
            'development_project': 120,
            'strategic_plan': 30,
            'research_project': 14
        }
        
        return duration_map.get(project.type, 14)  # Default 2 weeks
    
    def analyze_brand_website_dependencies(self) -> Dict[str, any]:
        """Specific analysis of brand and website project dependencies."""
        brand_projects = [p for p in self.projects if 'brand' in p.tags.get('functional', [])]
        website_projects = [p for p in self.projects if 'website' in p.tags.get('functional', [])]
        
        analysis = {
            'brand_projects': len(brand_projects),
            'website_projects': len(website_projects),
            'cross_dependencies': [],
            'sequential_workflow': [],
            'parallel_opportunities': [],
            'risk_analysis': []
        }
        
        # Find cross-dependencies
        for brand_proj in brand_projects:
            for website_proj in website_projects:
                if (brand_proj.title in self.dependency_graph[website_proj.title]['dependencies'] or
                    website_proj.title in self.dependency_graph[brand_proj.title]['dependencies']):
                    
                    analysis['cross_dependencies'].append({
                        'brand_project': brand_proj.title,
                        'website_project': website_proj.title,
                        'dependency_type': 'explicit' if brand_proj.title in self.dependency_graph[website_proj.title]['explicit_deps'] else 'implicit',
                        'brand_priority': brand_proj.priority,
                        'website_priority': website_proj.priority
                    })
        
        # Sequential workflow analysis
        brand_sequence = sorted(brand_projects, key=lambda p: p.start_date if p.start_date else date.max)
        website_sequence = sorted(website_projects, key=lambda p: p.start_date if p.start_date else date.max)
        
        analysis['sequential_workflow'] = {
            'brand_sequence': [{'title': p.title, 'start_date': p.start_date.isoformat() if p.start_date else None} for p in brand_sequence],
            'website_sequence': [{'title': p.title, 'start_date': p.start_date.isoformat() if p.start_date else None} for p in website_sequence]
        }
        
        # Parallel opportunities
        for brand_proj in brand_projects:
            for website_proj in website_projects:
                if (not self._projects_dependent(brand_proj.title, website_proj.title) and
                    self._projects_can_run_parallel(brand_proj, website_proj)):
                    
                    analysis['parallel_opportunities'].append({
                        'brand_project': brand_proj.title,
                        'website_project': website_proj.title,
                        'benefit': 'Time savings through parallel execution'
                    })
        
        # Risk analysis
        critical_brand_projects = [p for p in brand_projects if p.priority == 'high']
        for brand_proj in critical_brand_projects:
            dependents = self.dependency_graph[brand_proj.title]['dependents']
            website_dependents = [d for d in dependents if any(wp.title == d for wp in website_projects)]
            
            if website_dependents:
                analysis['risk_analysis'].append({
                    'risk_type': 'brand_delay_impact',
                    'source_project': brand_proj.title,
                    'impacted_projects': website_dependents,
                    'risk_level': 'high' if len(website_dependents) > 1 else 'medium',
                    'mitigation': 'Ensure brand project stays on schedule or prepare contingency plans'
                })
        
        return analysis
    
    def _projects_dependent(self, proj1_title: str, proj2_title: str) -> bool:
        """Check if two projects have a dependency relationship."""
        return (proj1_title in self.dependency_graph[proj2_title]['dependencies'] or
                proj2_title in self.dependency_graph[proj1_title]['dependencies'])
    
    def _projects_can_run_parallel(self, proj1: Project, proj2: Project) -> bool:
        """Check if two projects can run in parallel without conflicts."""
        if not (proj1.start_date and proj1.end_date and proj2.start_date and proj2.end_date):
            return False
        
        # Check for timeline overlap
        overlap = (proj1.start_date <= proj2.end_date and proj2.start_date <= proj1.end_date)
        
        # Check for resource conflicts
        proj1_resources = set(proj1.tags.get('resource', []))
        proj2_resources = set(proj2.tags.get('resource', []))
        resource_conflict = bool(proj1_resources & proj2_resources)
        
        return overlap and not resource_conflict
    
    def identify_bottlenecks(self) -> List[Dict]:
        """Identify potential bottleneck projects."""
        bottlenecks = []
        
        for project_title, data in self.dependency_graph.items():
            project = data['project']
            dependents_count = len(data['dependents'])
            
            # High-impact bottlenecks
            if dependents_count >= 3:
                bottlenecks.append({
                    'project': project_title,
                    'type': 'high_impact',
                    'dependents_count': dependents_count,
                    'impacted_projects': data['dependents'],
                    'risk_level': 'high' if dependents_count >= 5 else 'medium',
                    'priority': project.priority,
                    'resource_requirements': project.tags.get('resource', [])
                })
            
            # Resource bottlenecks
            if 'communications-team' in project.tags.get('resource', []):
                if dependents_count >= 2:
                    bottlenecks.append({
                        'project': project_title,
                        'type': 'resource_bottleneck',
                        'resource': 'communications-team',
                        'dependents_count': dependents_count,
                        'risk_level': 'medium',
                        'mitigation': 'Ensure communications team capacity or cross-training'
                    })
        
        return sorted(bottlenecks, key=lambda x: x['dependents_count'], reverse=True)
    
    def generate_dependency_report(self, output_file: str = None) -> str:
        """Generate comprehensive dependency analysis report."""
        report_lines = [
            "# Project Dependency Analysis Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Total Projects Analyzed:** {len(self.projects)}",
            "",
            "## Executive Summary",
            ""
        ]
        
        # Critical path analysis
        critical_path = self.find_critical_path()
        if critical_path:
            total_duration = sum(duration for _, duration in critical_path)
            report_lines.extend([
                f"**Critical Path Length:** {len(critical_path)} projects",
                f"**Estimated Total Duration:** {total_duration} days",
                "",
                "### Critical Path Projects:",
                ""
            ])
            
            for i, (project_title, duration) in enumerate(critical_path, 1):
                project = self.dependency_graph[project_title]['project']
                report_lines.append(f"{i}. **{project_title}** ({duration} days)")
                report_lines.append(f"   - Priority: {project.priority}")
                report_lines.append(f"   - Resources: {', '.join(project.tags.get('resource', []))}")
                report_lines.append("")
        
        # Brand-Website dependency analysis
        brand_website_analysis = self.analyze_brand_website_dependencies()
        report_lines.extend([
            "## Brand & Website Project Dependencies",
            f"**Brand Projects:** {brand_website_analysis['brand_projects']}",
            f"**Website Projects:** {brand_website_analysis['website_projects']}",
            f"**Cross-Dependencies:** {len(brand_website_analysis['cross_dependencies'])}",
            ""
        ])
        
        if brand_website_analysis['cross_dependencies']:
            report_lines.append("### Direct Dependencies:")
            for dep in brand_website_analysis['cross_dependencies']:
                dep_type = dep['dependency_type'].title()
                report_lines.append(f"- **{dep['brand_project']}** → **{dep['website_project']}** ({dep_type})")
            report_lines.append("")
        
        if brand_website_analysis['parallel_opportunities']:
            report_lines.extend([
                "### Parallel Execution Opportunities:",
                ""
            ])
            for opp in brand_website_analysis['parallel_opportunities']:
                report_lines.append(f"- **{opp['brand_project']}** + **{opp['website_project']}**")
                report_lines.append(f"  *{opp['benefit']}*")
            report_lines.append("")
        
        # Bottleneck analysis
        bottlenecks = self.identify_bottlenecks()
        if bottlenecks:
            report_lines.extend([
                "## Potential Bottlenecks",
                ""
            ])
            
            for bottleneck in bottlenecks:
                risk_icon = "🔴" if bottleneck['risk_level'] == 'high' else "🟡"
                report_lines.append(f"{risk_icon} **{bottleneck['project']}** ({bottleneck['type'].replace('_', ' ').title()})")
                report_lines.append(f"   - Blocks {bottleneck['dependents_count']} projects")
                report_lines.append(f"   - Priority: {bottleneck.get('priority', 'unknown')}")
                
                if 'mitigation' in bottleneck:
                    report_lines.append(f"   - Mitigation: {bottleneck['mitigation']}")
                
                report_lines.append(f"   - Impacted: {', '.join(bottleneck.get('impacted_projects', []))}")
                report_lines.append("")
        
        # Risk analysis
        risks = brand_website_analysis.get('risk_analysis', [])
        if risks:
            report_lines.extend([
                "## Dependency Risk Analysis",
                ""
            ])
            
            for risk in risks:
                risk_icon = "🔴" if risk['risk_level'] == 'high' else "🟡"
                report_lines.append(f"{risk_icon} **{risk['risk_type'].replace('_', ' ').title()}**")
                report_lines.append(f"   - Source: {risk['source_project']}")
                report_lines.append(f"   - Impact: {len(risk['impacted_projects'])} projects")
                report_lines.append(f"   - Mitigation: {risk['mitigation']}")
                report_lines.append("")
        
        # Dependency graph visualization
        report_lines.extend([
            "## Dependency Graph Overview",
            ""
        ])
        
        for project_title, data in sorted(self.dependency_graph.items()):
            if data['dependencies'] or data['dependents']:
                report_lines.append(f"**{project_title}**")
                
                if data['dependencies']:
                    deps_list = []
                    for dep in data['dependencies']:
                        if dep in data['explicit_deps']:
                            deps_list.append(f"{dep} (explicit)")
                        else:
                            deps_list.append(f"{dep} (implicit)")
                    report_lines.append(f"   - Depends on: {', '.join(deps_list)}")
                
                if data['dependents']:
                    report_lines.append(f"   - Blocks: {', '.join(data['dependents'])}")
                
                report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # Save to file if specified
        if output_file:
            output_path = Path("output/reports") / output_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"Dependency analysis saved to: {output_path}")
        
        return report_content

def main():
    """Main execution function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze project dependencies in DCLT Strategic System")
    parser.add_argument("--output", default="dependency_analysis.md", 
                       help="Output filename (default: dependency_analysis.md)")
    parser.add_argument("--focus", choices=['brand-website', 'critical-path', 'bottlenecks'],
                       help="Focus analysis on specific area")
    
    args = parser.parse_args()
    
    # Initialize parser and analyzer
    fm_parser = FrontmatterParser()
    analyzer = DependencyAnalyzer(fm_parser)
    
    print(f"Analyzing project dependencies...")
    
    if args.focus == 'brand-website':
        analysis = analyzer.analyze_brand_website_dependencies()
        print(f"Brand projects: {analysis['brand_projects']}")
        print(f"Website projects: {analysis['website_projects']}")
        print(f"Cross-dependencies: {len(analysis['cross_dependencies'])}")
    elif args.focus == 'critical-path':
        critical_path = analyzer.find_critical_path()
        print(f"Critical path length: {len(critical_path)} projects")
        if critical_path:
            total_duration = sum(duration for _, duration in critical_path)
            print(f"Total duration: {total_duration} days")
    elif args.focus == 'bottlenecks':
        bottlenecks = analyzer.identify_bottlenecks()
        print(f"Potential bottlenecks identified: {len(bottlenecks)}")
        for bottleneck in bottlenecks[:3]:  # Top 3
            print(f"- {bottleneck['project']} (blocks {bottleneck['dependents_count']} projects)")
    
    # Generate full report
    report = analyzer.generate_dependency_report(output_file=args.output)
    
    print(f"\nFull dependency analysis saved to output/reports/{args.output}")

if __name__ == "__main__":
    main()