#!/usr/bin/env python3
"""
Strategic Dashboard Generator for DCLT Strategic System

This script generates comprehensive analysis dashboards combining resource conflicts,
dependencies, timeline analysis, and strategic initiative tracking.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict, Counter
from typing import Dict, List, Set, Tuple, Optional, Any

# Add scripts directory to path for imports
sys.path.append(str(Path(__file__).parent))
from frontmatter_parser import FrontmatterParser
from resource_conflict_analyzer import ResourceConflictAnalyzer
from dependency_analyzer import DependencyAnalyzer
from strategic_query import StrategicQueryEngine

class DashboardGenerator:
    """Generates comprehensive strategic planning dashboards."""
    
    def __init__(self, parser: FrontmatterParser):
        self.parser = parser
        self.projects = parser.projects
        self.conflict_analyzer = ResourceConflictAnalyzer(parser)
        self.dependency_analyzer = DependencyAnalyzer(parser)
        self.query_engine = StrategicQueryEngine(parser)
        
    def generate_executive_dashboard(self, output_file: str = "executive_dashboard.md") -> str:
        """Generate executive-level strategic dashboard."""
        
        # Gather all analyses
        resource_analysis = self.conflict_analyzer.analyze_resource_conflicts()
        dependency_analysis = self.dependency_analyzer.find_critical_path()
        brand_website_deps = self.dependency_analyzer.analyze_brand_website_dependencies()
        bottlenecks = self.dependency_analyzer.identify_bottlenecks()
        
        # Strategic initiative analysis
        rebrand_analysis = self.query_engine.query("rebrand initiative")
        high_priority_analysis = self.query_engine.query("high priority projects")
        q3_analysis = self.query_engine.query("projects in Q3-2025")
        
        dashboard_content = self._build_executive_dashboard(
            resource_analysis, dependency_analysis, brand_website_deps,
            bottlenecks, rebrand_analysis, high_priority_analysis, q3_analysis
        )
        
        # Save dashboard
        output_path = Path("output/reports") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)
        
        print(f"Executive dashboard saved to: {output_path}")
        return dashboard_content
    
    def generate_operational_dashboard(self, output_file: str = "operational_dashboard.md") -> str:
        """Generate operational-level detailed dashboard."""
        
        # Detailed operational analyses
        communications_workload = self.query_engine.query("communications team work")
        vendor_conflicts = self.conflict_analyzer.analyze_resource_conflicts()
        timeline_risks = self._analyze_timeline_risks()
        capacity_analysis = self._analyze_capacity_planning()
        
        dashboard_content = self._build_operational_dashboard(
            communications_workload, vendor_conflicts, timeline_risks, capacity_analysis
        )
        
        # Save dashboard
        output_path = Path("output/reports") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)
        
        print(f"Operational dashboard saved to: {output_path}")
        return dashboard_content
    
    def generate_project_status_dashboard(self, output_file: str = "project_status_dashboard.md") -> str:
        """Generate project status tracking dashboard."""
        
        status_breakdown = self._analyze_project_status()
        milestone_tracking = self._analyze_milestone_tracking()
        completion_forecasts = self._generate_completion_forecasts()
        
        dashboard_content = self._build_project_status_dashboard(
            status_breakdown, milestone_tracking, completion_forecasts
        )
        
        # Save dashboard
        output_path = Path("output/reports") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)
        
        print(f"Project status dashboard saved to: {output_path}")
        return dashboard_content
    
    def generate_all_dashboards(self, output_dir: str = "output/reports") -> Dict[str, str]:
        """Generate all dashboard types."""
        dashboards = {}
        
        print("Generating comprehensive strategic dashboards...")
        
        # Generate individual dashboards
        dashboards['executive'] = self.generate_executive_dashboard("executive_dashboard.md")
        dashboards['operational'] = self.generate_operational_dashboard("operational_dashboard.md")
        dashboards['project_status'] = self.generate_project_status_dashboard("project_status_dashboard.md")
        
        # Generate summary index
        index_content = self._generate_dashboard_index()
        index_path = Path(output_dir) / "dashboard_index.md"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"Dashboard index saved to: {index_path}")
        dashboards['index'] = index_content
        
        return dashboards
    
    def _build_executive_dashboard(self, resource_analysis, dependency_analysis, 
                                 brand_website_deps, bottlenecks, rebrand_analysis,
                                 high_priority_analysis, q3_analysis) -> str:
        """Build executive dashboard content."""
        
        lines = [
            "# DCLT Strategic Planning - Executive Dashboard",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**System Status:** {len(self.projects)} active projects tracked",
            "",
            "## 🎯 Strategic Overview",
            ""
        ]
        
        # Key metrics summary
        total_projects = len(self.projects)
        high_priority_count = high_priority_analysis['data'].get('total_high_priority', 0)
        resource_warnings = len(resource_analysis.get('capacity_warnings', []))
        critical_path_length = len(dependency_analysis)
        
        lines.extend([
            f"- **Total Active Projects:** {total_projects}",
            f"- **High Priority Projects:** {high_priority_count}",
            f"- **Resource Capacity Warnings:** {resource_warnings}",
            f"- **Critical Path Length:** {critical_path_length} projects",
            ""
        ])
        
        # Strategic initiative status
        rebrand_data = rebrand_analysis['data']
        lines.extend([
            "### Strategic Initiative Status",
            "",
            f"**🎨 Rebrand Initiative:** {rebrand_data.get('total_projects', 0)} projects",
        ])
        
        rebrand_status = rebrand_data.get('completion_status', {})
        if rebrand_status:
            lines.append(f"   - Complete: {rebrand_status.get('complete', 0)}")
            lines.append(f"   - In Progress: {rebrand_status.get('in_progress', 0)}")
            lines.append(f"   - Not Started: {rebrand_status.get('not_started', 0)}")
        
        lines.append("")
        
        # High-level risks and opportunities
        lines.extend([
            "## ⚠️ Strategic Risks & Opportunities",
            ""
        ])
        
        # Resource risks
        workload = resource_analysis.get('resource_workload', {})
        if 'communications-team' in workload:
            comm_projects = workload['communications-team']['total_projects']
            lines.append(f"🔴 **Communications Team Capacity:** {comm_projects} concurrent projects")
            if comm_projects >= 15:
                lines.append("   *Risk: Team overload may impact delivery quality and timelines*")
            lines.append("")
        
        # Dependency risks
        if bottlenecks:
            high_risk_bottlenecks = [b for b in bottlenecks if b['risk_level'] == 'high']
            lines.append(f"🟡 **Project Bottlenecks:** {len(high_risk_bottlenecks)} high-risk dependencies")
            if high_risk_bottlenecks:
                for bottleneck in high_risk_bottlenecks[:2]:  # Top 2
                    lines.append(f"   - {bottleneck['project']} (blocks {bottleneck['dependents_count']} projects)")
            lines.append("")
        
        # Brand-Website coordination
        brand_deps = brand_website_deps.get('cross_dependencies', [])
        lines.extend([
            f"🔗 **Brand-Website Dependencies:** {len(brand_deps)} cross-project links",
            "   *Opportunity: Optimize sequencing for maximum efficiency*",
            ""
        ])
        
        # Timeline concentration
        q3_data = q3_analysis['data']
        q3_projects = q3_data.get('total_projects', 0)
        lines.extend([
            f"📅 **Q3 2025 Timeline:** {q3_projects} concurrent projects",
        ])
        
        if q3_projects >= 20:
            lines.append("   *Risk: High activity concentration may stress resources*")
        
        lines.append("")
        
        # Key recommendations
        lines.extend([
            "## 🚀 Executive Recommendations",
            "",
            "### Immediate Actions (Next 30 Days)",
        ])
        
        recommendations = []
        
        # Resource recommendations
        if 'communications-team' in workload and workload['communications-team']['total_projects'] >= 15:
            recommendations.append("**Staff Augmentation:** Consider temporary communications support or contractor")
        
        # Timeline recommendations
        if q3_projects >= 20:
            recommendations.append("**Project Sequencing:** Stagger non-critical projects to reduce Q3 peak load")
        
        # Dependency recommendations
        if len(brand_deps) >= 5:
            recommendations.append("**Coordination Protocols:** Establish weekly brand-website sync meetings")
        
        for i, rec in enumerate(recommendations[:3], 1):  # Top 3
            lines.append(f"{i}. {rec}")
        
        lines.extend([
            "",
            "### Strategic Opportunities (Next 90 Days)",
            "1. **Process Optimization:** Leverage parallel execution opportunities in brand/website work",
            "2. **Vendor Coordination:** Establish master vendor schedule for Q3-Q4 deliverables",
            "3. **Milestone Integration:** Align rebrand milestones with 40th anniversary celebration",
            ""
        ])
        
        # Success metrics dashboard
        lines.extend([
            "## 📊 Success Metrics Dashboard",
            "",
            "| Metric | Current | Target | Status |",
            "|--------|---------|--------|--------|"
        ])
        
        # Calculate metrics
        completed_projects = len([p for p in self.projects if p.status == 'complete'])
        completion_rate = (completed_projects / total_projects * 100) if total_projects > 0 else 0
        on_time_projects = len([p for p in self.projects if p.status in ['complete', 'in_progress']])
        
        lines.extend([
            f"| Project Completion Rate | {completion_rate:.1f}% | 90% | {'🟢' if completion_rate >= 80 else '🟡' if completion_rate >= 60 else '🔴'} |",
            f"| High Priority On Track | {high_priority_count} | {high_priority_count} | {'🟢' if resource_warnings == 0 else '🟡'} |",
            f"| Resource Capacity | {resource_warnings} warnings | 0 warnings | {'🟢' if resource_warnings == 0 else '🔴'} |",
            f"| Brand-Website Coordination | {len(brand_deps)} links | Managed | {'🟢' if len(brand_deps) <= 8 else '🟡'} |",
            ""
        ])
        
        return "\n".join(lines)
    
    def _build_operational_dashboard(self, communications_workload, vendor_conflicts,
                                   timeline_risks, capacity_analysis) -> str:
        """Build operational dashboard content."""
        
        lines = [
            "# DCLT Strategic Planning - Operational Dashboard",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Focus:** Resource management and operational coordination",
            "",
            "## 👥 Resource Allocation Overview",
            ""
        ]
        
        # Communications team workload detail
        comm_data = communications_workload['data']
        lines.extend([
            f"### Communications Team ({comm_data.get('total_projects', 0)} projects)",
            ""
        ])
        
        comm_projects = comm_data.get('projects', [])
        by_category = defaultdict(int)
        by_priority = defaultdict(int)
        
        for project in comm_projects:
            by_category[project['category']] += 1
            by_priority[project['priority']] += 1
        
        lines.extend([
            "**Workload Breakdown:**",
            f"- High Priority: {by_priority.get('high', 0)} projects",
            f"- Medium Priority: {by_priority.get('medium', 0)} projects",
            f"- Low Priority: {by_priority.get('low', 0)} projects",
            "",
            "**By Category:**"
        ])
        
        for category, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- {category.title()}: {count} projects")
        
        lines.append("")
        
        # External vendor coordination
        vendor_analysis = vendor_conflicts.get('external_vendor_needs', {})
        vendor_count = vendor_analysis.get('total_vendor_projects', 0)
        
        lines.extend([
            f"### External Vendor Coordination ({vendor_count} projects)",
            ""
        ])
        
        if vendor_count > 0:
            vendor_categories = vendor_analysis.get('vendor_categories', {})
            lines.append("**Vendor Requirements by Category:**")
            for category, count in sorted(vendor_categories.items(), key=lambda x: x[1], reverse=True):
                lines.append(f"- {category.title()}: {count} projects")
            
            vendor_timeline = vendor_analysis.get('vendor_timeline', {})
            if vendor_timeline:
                lines.extend([
                    "",
                    "**Vendor Timeline Distribution:**"
                ])
                for quarter, projects in sorted(vendor_timeline.items()):
                    lines.append(f"- {quarter}: {len(projects)} projects")
        
        lines.append("")
        
        # Resource conflicts detail
        resource_conflicts = vendor_conflicts.get('resource_conflicts', {})
        lines.extend([
            "## ⚠️ Resource Conflicts & Capacity Issues",
            ""
        ])
        
        if resource_conflicts:
            total_conflicts = sum(len(conflicts) for conflicts in resource_conflicts.values())
            lines.append(f"**Active Resource Conflicts:** {total_conflicts}")
            lines.append("")
            
            for resource, conflicts in resource_conflicts.items():
                if conflicts:
                    lines.append(f"### {resource.replace('-', ' ').title()}")
                    for conflict in conflicts[:3]:  # Top 3 conflicts per resource
                        priority_flag = " ⚠️" if conflict.get('high_priority_conflict') else ""
                        lines.append(f"- **{conflict['project1']}** ↔ **{conflict['project2']}**{priority_flag}")
                        if 'overlap_start' in conflict:
                            lines.append(f"  *Overlap: {conflict['overlap_start']} to {conflict['overlap_end']}*")
                    lines.append("")
        
        # Capacity planning recommendations
        capacity_warnings = vendor_conflicts.get('capacity_warnings', [])
        if capacity_warnings:
            lines.extend([
                "## 📋 Capacity Planning Actions",
                ""
            ])
            
            for warning in capacity_warnings:
                severity_icon = "🔴" if warning['warning_level'] == 'high' else "🟡"
                lines.append(f"{severity_icon} **{warning['resource'].replace('-', ' ').title()}**")
                lines.append(f"   - Current Load: {warning['total_projects']} projects")
                lines.append(f"   - Recommendation: {warning['recommendation']}")
                lines.append("")
        
        # Timeline risk analysis
        lines.extend([
            "## 📅 Timeline Risk Analysis",
            ""
        ])
        
        timeline_data = timeline_risks
        lines.extend([
            f"**Peak Activity Period:** {timeline_data['peak_period']}",
            f"**Concurrent Projects:** {timeline_data['peak_concurrent']}",
            f"**Risk Level:** {timeline_data['risk_level']}",
            ""
        ])
        
        if timeline_data.get('risk_mitigation'):
            lines.extend([
                "**Risk Mitigation Strategies:**"
            ])
            for strategy in timeline_data['risk_mitigation']:
                lines.append(f"- {strategy}")
            lines.append("")
        
        # Action items
        lines.extend([
            "## 🎯 Immediate Action Items",
            "",
            "### Resource Management",
            "1. **Weekly Capacity Reviews:** Monitor communications team workload",
            "2. **Vendor Coordination:** Schedule Q3 vendor kickoff meetings",
            "3. **Conflict Resolution:** Address high-priority project overlaps",
            "",
            "### Process Improvements",
            "1. **Project Sequencing:** Implement staggered start dates for non-critical work",
            "2. **Cross-Training:** Develop backup capabilities for critical resources",
            "3. **Tool Integration:** Automate resource conflict detection",
            ""
        ])
        
        return "\n".join(lines)
    
    def _build_project_status_dashboard(self, status_breakdown, milestone_tracking,
                                      completion_forecasts) -> str:
        """Build project status dashboard content."""
        
        lines = [
            "# DCLT Strategic Planning - Project Status Dashboard",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Focus:** Project progress tracking and milestone management",
            "",
            "## 📊 Project Portfolio Status",
            ""
        ]
        
        # Overall status breakdown
        lines.extend([
            "### Overall Progress",
            "",
            f"**Total Projects:** {status_breakdown['total_projects']}",
            ""
        ])
        
        status_counts = status_breakdown['by_status']
        total = status_breakdown['total_projects']
        
        for status, count in status_counts.items():
            percentage = (count / total * 100) if total > 0 else 0
            status_icon = {
                'complete': '🟢',
                'in_progress': '🟡',
                'not_started': '🔴',
                'on_hold': '⏸️'
            }.get(status, '⚪')
            
            lines.append(f"{status_icon} **{status.replace('_', ' ').title()}:** {count} projects ({percentage:.1f}%)")
        
        lines.append("")
        
        # Priority status breakdown
        lines.extend([
            "### By Priority Level",
            ""
        ])
        
        priority_status = status_breakdown['priority_status']
        for priority in ['high', 'medium', 'low']:
            if priority in priority_status:
                data = priority_status[priority]
                lines.append(f"**{priority.title()} Priority:** {data['total']} projects")
                
                for status, count in data['status_breakdown'].items():
                    if count > 0:
                        lines.append(f"   - {status.replace('_', ' ').title()}: {count}")
                lines.append("")
        
        # Strategic initiative progress
        lines.extend([
            "## 🎯 Strategic Initiative Progress",
            ""
        ])
        
        strategic_progress = status_breakdown['strategic_progress']
        for initiative, data in strategic_progress.items():
            progress_percent = (data['complete'] / data['total'] * 100) if data['total'] > 0 else 0
            
            progress_icon = "🟢" if progress_percent >= 75 else "🟡" if progress_percent >= 50 else "🔴"
            
            lines.extend([
                f"{progress_icon} **{initiative.replace('-', ' ').title()}**",
                f"   - Progress: {data['complete']}/{data['total']} projects ({progress_percent:.1f}%)",
                f"   - In Progress: {data['in_progress']}",
                f"   - Not Started: {data['not_started']}",
                ""
            ])
        
        # Milestone tracking
        lines.extend([
            "## 🎯 Milestone Tracking",
            ""
        ])
        
        upcoming_milestones = milestone_tracking['upcoming_milestones']
        overdue_milestones = milestone_tracking['overdue_milestones']
        
        if overdue_milestones:
            lines.extend([
                "### 🔴 Overdue Milestones",
                ""
            ])
            for milestone in overdue_milestones:
                lines.append(f"- **{milestone['project']}** (due {milestone['due_date']})")
            lines.append("")
        
        if upcoming_milestones:
            lines.extend([
                "### 🟡 Upcoming Milestones (Next 30 Days)",
                ""
            ])
            for milestone in upcoming_milestones[:5]:  # Next 5 milestones
                lines.append(f"- **{milestone['project']}** (due {milestone['due_date']})")
            lines.append("")
        
        # Completion forecasts
        lines.extend([
            "## 📈 Completion Forecasts",
            ""
        ])
        
        monthly_forecasts = completion_forecasts['monthly_completion']
        lines.extend([
            "### Expected Completions by Month",
            ""
        ])
        
        for month, projects in sorted(monthly_forecasts.items()):
            if projects:
                lines.append(f"**{month}:** {len(projects)} projects")
                for project in projects[:3]:  # Top 3 per month
                    lines.append(f"   - {project['title']} ({project['priority']} priority)")
                if len(projects) > 3:
                    lines.append(f"   - ... and {len(projects) - 3} more")
                lines.append("")
        
        # Risk alerts
        lines.extend([
            "## ⚠️ Status Alerts & Risks",
            ""
        ])
        
        risk_alerts = status_breakdown.get('risk_alerts', [])
        if risk_alerts:
            for alert in risk_alerts:
                severity_icon = "🔴" if alert['severity'] == 'high' else "🟡"
                lines.append(f"{severity_icon} **{alert['type'].replace('_', ' ').title()}**")
                lines.append(f"   - {alert['description']}")
                lines.append(f"   - Action: {alert['recommended_action']}")
                lines.append("")
        else:
            lines.append("✅ No critical status alerts at this time")
            lines.append("")
        
        # Action dashboard
        lines.extend([
            "## 🎯 Action Dashboard",
            "",
            "### This Week",
            "- [ ] Review overdue milestone status",
            "- [ ] Update project progress reports",
            "- [ ] Schedule stakeholder check-ins for high priority projects",
            "",
            "### Next 30 Days",
            "- [ ] Conduct quarterly project portfolio review",
            "- [ ] Adjust resource allocations based on progress",
            "- [ ] Plan milestone celebration events",
            ""
        ])
        
        return "\n".join(lines)
    
    def _analyze_timeline_risks(self) -> Dict[str, Any]:
        """Analyze timeline-related risks."""
        monthly_distribution = defaultdict(list)
        
        for project in self.projects:
            if project.start_date:
                month_key = f"{project.start_date.year}-{project.start_date.month:02d}"
                monthly_distribution[month_key].append(project)
        
        # Find peak month
        peak_month = max(monthly_distribution.items(), key=lambda x: len(x[1])) if monthly_distribution else (None, [])
        
        risk_level = "low"
        peak_concurrent = len(peak_month[1]) if peak_month[0] else 0
        
        if peak_concurrent >= 20:
            risk_level = "high"
        elif peak_concurrent >= 15:
            risk_level = "medium"
        
        risk_mitigation = []
        if risk_level in ["high", "medium"]:
            risk_mitigation.extend([
                "Stagger project start dates where possible",
                "Pre-allocate additional temporary resources",
                "Identify projects that can be delayed without impact",
                "Establish rapid escalation procedures for bottlenecks"
            ])
        
        return {
            'peak_period': peak_month[0] if peak_month[0] else "None identified",
            'peak_concurrent': peak_concurrent,
            'risk_level': risk_level,
            'risk_mitigation': risk_mitigation,
            'monthly_distribution': {k: len(v) for k, v in monthly_distribution.items()}
        }
    
    def _analyze_capacity_planning(self) -> Dict[str, Any]:
        """Analyze capacity planning needs."""
        resource_capacity = defaultdict(lambda: {
            'current_load': 0,
            'peak_load': 0,
            'capacity_estimate': 10  # Default capacity
        })
        
        # Calculate current and peak loads
        monthly_resource_load = defaultdict(lambda: defaultdict(int))
        
        for project in self.projects:
            if project.start_date:
                month_key = f"{project.start_date.year}-{project.start_date.month:02d}"
                for resource in project.tags.get('resource', []):
                    monthly_resource_load[resource][month_key] += 1
        
        for resource, monthly_loads in monthly_resource_load.items():
            resource_capacity[resource]['current_load'] = sum(monthly_loads.values())
            resource_capacity[resource]['peak_load'] = max(monthly_loads.values()) if monthly_loads else 0
        
        return dict(resource_capacity)
    
    def _analyze_project_status(self) -> Dict[str, Any]:
        """Analyze comprehensive project status."""
        total_projects = len(self.projects)
        by_status = Counter(p.status for p in self.projects)
        
        # Priority status breakdown
        priority_status = {}
        for priority in ['high', 'medium', 'low']:
            priority_projects = [p for p in self.projects if p.priority == priority]
            priority_status[priority] = {
                'total': len(priority_projects),
                'status_breakdown': Counter(p.status for p in priority_projects)
            }
        
        # Strategic initiative progress
        strategic_progress = {}
        all_strategic_tags = set()
        for project in self.projects:
            for tag in project.tags.get('strategic', []):
                all_strategic_tags.add(tag)
        
        for initiative in all_strategic_tags:
            initiative_projects = [p for p in self.projects if initiative in p.tags.get('strategic', [])]
            strategic_progress[initiative] = {
                'total': len(initiative_projects),
                'complete': len([p for p in initiative_projects if p.status == 'complete']),
                'in_progress': len([p for p in initiative_projects if p.status == 'in_progress']),
                'not_started': len([p for p in initiative_projects if p.status == 'not_started'])
            }
        
        # Risk alerts
        risk_alerts = []
        
        # High priority projects not in progress
        stalled_high_priority = [p for p in self.projects if p.priority == 'high' and p.status == 'not_started']
        if len(stalled_high_priority) >= 3:
            risk_alerts.append({
                'type': 'stalled_high_priority',
                'severity': 'high',
                'description': f"{len(stalled_high_priority)} high priority projects not yet started",
                'recommended_action': 'Review and prioritize project initiation'
            })
        
        # Overdue projects (if we had due dates)
        overdue_projects = []
        for project in self.projects:
            if project.due_date and project.due_date < date.today() and project.status != 'complete':
                overdue_projects.append(project)
        
        if overdue_projects:
            risk_alerts.append({
                'type': 'overdue_projects',
                'severity': 'high',
                'description': f"{len(overdue_projects)} projects are overdue",
                'recommended_action': 'Immediate status review and recovery planning'
            })
        
        return {
            'total_projects': total_projects,
            'by_status': dict(by_status),
            'priority_status': priority_status,
            'strategic_progress': strategic_progress,
            'risk_alerts': risk_alerts
        }
    
    def _analyze_milestone_tracking(self) -> Dict[str, Any]:
        """Analyze milestone tracking and upcoming deadlines."""
        upcoming_milestones = []
        overdue_milestones = []
        today = date.today()
        thirty_days = today + timedelta(days=30)
        
        for project in self.projects:
            milestone_data = {
                'project': project.title,
                'priority': project.priority,
                'status': project.status
            }
            
            # Check due dates
            if project.due_date:
                milestone_data['due_date'] = project.due_date.isoformat()
                milestone_data['days_until_due'] = (project.due_date - today).days
                
                if project.due_date < today and project.status != 'complete':
                    overdue_milestones.append(milestone_data)
                elif project.due_date <= thirty_days:
                    upcoming_milestones.append(milestone_data)
            
            # Check end dates
            elif project.end_date:
                milestone_data['due_date'] = project.end_date.isoformat()
                milestone_data['days_until_due'] = (project.end_date - today).days
                
                if project.end_date < today and project.status != 'complete':
                    overdue_milestones.append(milestone_data)
                elif project.end_date <= thirty_days:
                    upcoming_milestones.append(milestone_data)
        
        # Sort by due date
        upcoming_milestones.sort(key=lambda x: x['due_date'])
        overdue_milestones.sort(key=lambda x: x['due_date'], reverse=True)  # Most overdue first
        
        return {
            'upcoming_milestones': upcoming_milestones,
            'overdue_milestones': overdue_milestones
        }
    
    def _generate_completion_forecasts(self) -> Dict[str, Any]:
        """Generate project completion forecasts."""
        monthly_completion = defaultdict(list)
        
        for project in self.projects:
            if project.end_date and project.status != 'complete':
                month_key = f"{project.end_date.year}-{project.end_date.month:02d}"
                monthly_completion[month_key].append({
                    'title': project.title,
                    'priority': project.priority,
                    'category': project.category,
                    'end_date': project.end_date.isoformat()
                })
        
        return {
            'monthly_completion': dict(monthly_completion)
        }
    
    def _generate_dashboard_index(self) -> str:
        """Generate dashboard index page."""
        lines = [
            "# DCLT Strategic Planning - Dashboard Index",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Available Dashboards",
            "",
            "### 🎯 Executive Dashboard",
            "**Purpose:** High-level strategic overview for leadership and board",
            "**Contains:** Key metrics, strategic risks, executive recommendations",
            "**Audience:** Executive team, board members, senior leadership",
            "**File:** `executive_dashboard.md`",
            "",
            "### 🛠️ Operational Dashboard", 
            "**Purpose:** Detailed resource management and coordination",
            "**Contains:** Resource allocation, capacity planning, conflict resolution",
            "**Audience:** Project managers, operations team, communications team",
            "**File:** `operational_dashboard.md`",
            "",
            "### 📋 Project Status Dashboard",
            "**Purpose:** Project progress tracking and milestone management",
            "**Contains:** Status breakdowns, milestone tracking, completion forecasts",
            "**Audience:** Project teams, stakeholders, progress tracking",
            "**File:** `project_status_dashboard.md`",
            "",
            "## Quick Stats",
            f"- **Total Projects:** {len(self.projects)}",
            f"- **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- **Data Source:** {len(self.projects)} projects with structured frontmatter",
            "",
            "## Usage Instructions",
            "",
            "1. **Executives/Board:** Start with Executive Dashboard for strategic overview",
            "2. **Operations Teams:** Use Operational Dashboard for daily management",
            "3. **Project Teams:** Reference Project Status Dashboard for progress tracking",
            "4. **Regular Updates:** Regenerate dashboards weekly for current data",
            "",
            "## Generated Reports Available",
            "",
            "- Resource Conflict Analysis: `resource_conflict_analysis.md`",
            "- Project Dependencies: `dependency_analysis.md`", 
            "- Tag Inventory: `tag_inventory_report.md`",
            "- Frontmatter Analysis: `frontmatter_candidates.md`",
            "",
            "---",
            "*Dashboards are automatically generated from project frontmatter data*"
        ]
        
        return "\n".join(lines)

def main():
    """Main execution function for command line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate strategic planning dashboards for DCLT Strategic System")
    parser.add_argument("--type", choices=['executive', 'operational', 'status', 'all'], 
                       default='all', help="Dashboard type to generate")
    parser.add_argument("--output-dir", default="output/reports", 
                       help="Output directory for dashboards")
    
    args = parser.parse_args()
    
    # Initialize parser and dashboard generator
    fm_parser = FrontmatterParser()
    dashboard_gen = DashboardGenerator(fm_parser)
    
    print(f"Generating {args.type} dashboard(s)...")
    
    if args.type == 'executive':
        dashboard_gen.generate_executive_dashboard()
    elif args.type == 'operational':
        dashboard_gen.generate_operational_dashboard()
    elif args.type == 'status':
        dashboard_gen.generate_project_status_dashboard()
    else:  # all
        dashboards = dashboard_gen.generate_all_dashboards(args.output_dir)
        print(f"\nGenerated {len(dashboards)} dashboards:")
        for name, _ in dashboards.items():
            print(f"- {name.title()} Dashboard")
    
    print(f"\nDashboards saved to: {args.output_dir}")

if __name__ == "__main__":
    main()