#!/usr/bin/env python3
"""
Unified DCLT Strategic Planning System
Combines project management, Gantt charts, dashboards, and live watching
"""

import os
import sys
import json
import time
import hashlib
import threading
import subprocess
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional, Any
import frontmatter

class UnifiedProjectSystem:
    def __init__(self, projects_root="data/dclt/02_EXECUTION/10_Projects", 
                 output_dir=None, deploy_dir=None):
        # Handle relative paths from project root
        self.projects_root = os.path.abspath(projects_root)
        self.output_dir = output_dir or os.path.join(self.projects_root, "dashboards")
        self.deploy_dir = deploy_dir or os.path.abspath("deploy/gantt-chart")
        
        # Ensure directories exist
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        Path(self.deploy_dir).mkdir(parents=True, exist_ok=True)
        
        # File watching state
        self.file_checksums = {}
        self.last_regeneration = 0
        self.regeneration_cooldown = 10
        self.running = True
        
    def parse_date(self, date_str):
        """Parse various date formats, return None for TBD/invalid dates"""
        if not date_str or str(date_str).upper() == "TBD":
            return None
        
        try:
            return datetime.strptime(str(date_str), "%Y-%m-%d").date()
        except ValueError:
            try:
                return datetime.strptime(str(date_str), "%m/%d/%Y").date()
            except ValueError:
                return None

    def collect_projects(self):
        """Walk through markdown files and extract project data"""
        projects = []
        parent_map = defaultdict(list)
        
        for root, _, files in os.walk(self.projects_root):
            for file in files:
                if file.endswith(".md"):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding='utf-8') as f:
                            post = frontmatter.load(f)
                            meta = post.metadata
                            
                            project = {
                                "id": meta.get("project_id", file.replace(".md", "")),
                                "title": meta.get("title", file.replace(".md", "")),
                                "status": meta.get("status", "unknown"),
                                "priority": meta.get("priority", "medium"),
                                "start_date": self.parse_date(meta.get("start_date")),
                                "end_date": self.parse_date(meta.get("end_date")),
                                "notes": meta.get("notes", ""),
                                "parent_id": meta.get("parent_project_id"),
                                "file_path": path,
                                "content": post.content
                            }
                            
                            projects.append(project)
                            
                            if project["parent_id"]:
                                parent_map[project["parent_id"]].append(project)
                                
                    except Exception as e:
                        print(f"Warning: Could not parse {path}: {e}")
                        continue
        
        return projects, parent_map

    def generate_gantt_chart(self, projects, parent_map, filename="gantt_chart.html"):
        """Generate unified Gantt chart HTML"""
        
        # Calculate timeline bounds
        valid_dates = []
        for project in projects:
            if project["start_date"]:
                valid_dates.append(project["start_date"])
            if project["end_date"]:
                valid_dates.append(project["end_date"])
        
        if valid_dates:
            timeline_start = min(valid_dates).replace(day=1)
            timeline_end = max(valid_dates).replace(month=12, day=31)
        else:
            timeline_start = date.today().replace(day=1)
            timeline_end = date(date.today().year + 1, 12, 31)
        
        # Sort projects: parents first, then children
        sorted_projects = []
        parents = [p for p in projects if not p["parent_id"]]
        
        for parent in sorted(parents, key=lambda x: x["title"]):
            sorted_projects.append(parent)
            children = sorted(parent_map.get(parent["id"], []), key=lambda x: x["title"])
            sorted_projects.extend(children)
        
        # Add orphaned projects
        orphans = [p for p in projects if p["parent_id"] and not any(parent["id"] == p["parent_id"] for parent in parents)]
        sorted_projects.extend(sorted(orphans, key=lambda x: x["title"]))
        
        # Generate HTML
        chart_html = self._build_gantt_html(sorted_projects, timeline_start, timeline_end)
        
        # Save file
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(chart_html)
        
        return output_path

    def _build_gantt_html(self, projects, timeline_start, timeline_end):
        """Build the complete Gantt chart HTML"""
        
        def date_to_x(project_date, chart_width=1200):
            if not project_date:
                return None
            total_days = (timeline_end - timeline_start).days
            project_days = (project_date - timeline_start).days
            return 200 + (project_days / total_days) * chart_width
        
        def get_status_color(status):
            colors = {
                "completed": "#27AE60", "complete": "#27AE60",
                "active": "#F39C12", "in_progress": "#F39C12", "in-progress": "#F39C12",
                "planning": "#3498DB", "not_started": "#3498DB",
                "on_hold": "#95A5A6", "on-hold": "#95A5A6",
                "cancelled": "#E74C3C"
            }
            return colors.get(status.lower(), "#BDC3C7")
        
        # Generate project elements
        svg_height = max(600, len(projects) * 60 + 200)
        y_position = 100
        project_elements = []
        
        for project in projects:
            is_child = bool(project["parent_id"])
            x_indent = 40 if is_child else 0
            
            # Calculate position and width
            if project["start_date"] and project["end_date"]:
                start_x = date_to_x(project["start_date"])
                end_x = date_to_x(project["end_date"])
                width = max(50, end_x - start_x)
            elif project["start_date"]:
                start_x = date_to_x(project["start_date"])
                width = 100
            elif project["end_date"]:
                end_x = date_to_x(project["end_date"])
                start_x = end_x - 100
                width = 100
            else:
                start_x = 220
                width = 100
            
            color = get_status_color(project["status"])
            title_display = f"{'└ ' if is_child else ''}{project['title']}"
            
            project_elements.append(f'''
            <g class="project-group">
                <rect x="{start_x}" y="{y_position}" width="{width}" height="35"
                      fill="{color}" stroke="#2C3E50" stroke-width="2" rx="4" opacity="0.8"/>
                <text x="{20 + x_indent}" y="{y_position + 25}" 
                      font-family="Arial" font-size="14" font-weight="bold" fill="#2C3E50">
                      {title_display}
                </text>
                <rect x="{start_x + width + 10}" y="{y_position + 5}" width="80" height="20"
                      fill="{color}" rx="10"/>
                <text x="{start_x + width + 50}" y="{y_position + 17}" 
                      font-family="Arial" font-size="10" font-weight="bold" fill="white" text-anchor="middle">
                      {project['status'].upper()}
                </text>
                <text x="{start_x}" y="{y_position + 55}" 
                      font-family="Arial" font-size="10" fill="#7F8C8D">
                      {project['start_date'] or 'TBD'} → {project['end_date'] or 'TBD'}
                </text>
            </g>
            ''')
            y_position += 60
        
        # Generate timeline header
        months = []
        current_date = timeline_start
        x_pos = 200
        
        while current_date <= timeline_end:
            month_width = 100
            months.append(f'''
            <rect x="{x_pos}" y="20" width="{month_width}" height="25" 
                  fill="#3498DB" opacity="0.7"/>
            <text x="{x_pos + month_width/2}" y="37" 
                  font-family="Arial" font-size="12" font-weight="bold"
                  fill="white" text-anchor="middle">{current_date.strftime('%b %Y')}</text>
            ''')
            x_pos += month_width
            
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        # Complete HTML
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DCLT Projects - Unified Gantt Chart</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #F8F9FA; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #2C3E50; margin: 0; }}
        .chart-container {{ background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
                           overflow-x: auto; padding: 20px; }}
        .project-group:hover rect {{ opacity: 1; stroke-width: 3; }}
        .legend {{ display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }}
        .legend-item {{ display: flex; align-items: center; gap: 8px; font-size: 14px; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>DCLT Projects - Unified Gantt Chart</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Projects: {len(projects)}</p>
    </div>
    
    <div class="legend">
        <div class="legend-item"><div class="legend-color" style="background: #27AE60;"></div>Completed</div>
        <div class="legend-item"><div class="legend-color" style="background: #F39C12;"></div>Active/In Progress</div>
        <div class="legend-item"><div class="legend-color" style="background: #3498DB;"></div>Planning</div>
        <div class="legend-item"><div class="legend-color" style="background: #95A5A6;"></div>On Hold</div>
    </div>
    
    <div class="chart-container">
        <svg width="100%" height="{svg_height}" viewBox="0 0 1500 {svg_height}">
            <g class="timeline-header">{''.join(months)}</g>
            <defs>
                <pattern id="grid" width="100" height="60" patternUnits="userSpaceOnUse">
                    <path d="M 100 0 L 0 0 0 60" fill="none" stroke="#ECF0F1" stroke-width="1"/>
                </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" opacity="0.3"/>
            {''.join(project_elements)}
        </svg>
    </div>
</body>
</html>'''
        return html

    def generate_simple_dashboard(self, projects, filename="dashboard.html"):
        """Generate simple project dashboard"""
        
        # Status breakdown
        status_counts = Counter(p["status"] for p in projects)
        priority_counts = Counter(p["priority"] for p in projects)
        
        # Create table rows
        rows = []
        for project in sorted(projects, key=lambda x: (x["priority"], x["title"])):
            is_child = bool(project["parent_id"])
            title_display = f"{'  └ ' if is_child else ''}{project['title']}"
            
            rows.append(f'''
            <tr class="{'child-row' if is_child else 'parent-row'}">
                <td>{title_display}</td>
                <td><span class="status-badge {project['status']}">{project['status']}</span></td>
                <td><span class="priority-badge {project['priority']}">{project['priority']}</span></td>
                <td>{project['start_date'] or 'TBD'}</td>
                <td>{project['end_date'] or 'TBD'}</td>
                <td class="notes">{(project['notes'] or '')[:100]}{'...' if len(project['notes'] or '') > 100 else ''}</td>
            </tr>
            ''')
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DCLT Projects Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f8f9fa; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .stats {{ display: flex; gap: 20px; justify-content: center; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        table {{ width: 100%; background: white; border-collapse: collapse; border-radius: 8px; overflow: hidden; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        th {{ background: #2c3e50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .child-row {{ background: #f8f9fa; }}
        .status-badge, .priority-badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-size: 12px; }}
        .completed {{ background: #27ae60; }} .active, .in_progress, .in-progress {{ background: #f39c12; }}
        .planning, .not_started {{ background: #3498db; }} .on_hold, .on-hold {{ background: #95a5a6; }}
        .high {{ background: #e74c3c; }} .medium {{ background: #f39c12; }} .low {{ background: #27ae60; }}
        .notes {{ max-width: 300px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>DCLT Projects Dashboard</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card"><h3>{len(projects)}</h3><p>Total Projects</p></div>
        <div class="stat-card"><h3>{status_counts.get('completed', 0) + status_counts.get('complete', 0)}</h3><p>Completed</p></div>
        <div class="stat-card"><h3>{status_counts.get('active', 0) + status_counts.get('in_progress', 0) + status_counts.get('in-progress', 0)}</h3><p>In Progress</p></div>
        <div class="stat-card"><h3>{priority_counts.get('high', 0)}</h3><p>High Priority</p></div>
    </div>
    
    <table>
        <tr>
            <th>Project</th><th>Status</th><th>Priority</th><th>Start</th><th>End</th><th>Notes</th>
        </tr>
        {''.join(rows)}
    </table>
</body>
</html>'''
        
        output_path = os.path.join(self.output_dir, filename)
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(html)
        
        return output_path

    def generate_all_outputs(self):
        """Generate all charts and dashboards"""
        print("Collecting projects...")
        projects, parent_map = self.collect_projects()
        print(f"Found {len(projects)} projects")
        
        outputs = {}
        
        # Generate Gantt chart
        print("Generating Gantt chart...")
        gantt_path = self.generate_gantt_chart(projects, parent_map, "gantt_chart.html")
        outputs['gantt'] = gantt_path
        
        # Generate dashboard
        print("Generating dashboard...")
        dashboard_path = self.generate_simple_dashboard(projects, "dashboard.html")
        outputs['dashboard'] = dashboard_path
        
        # Deploy files
        if os.path.exists(gantt_path):
            import shutil
            shutil.copy2(gantt_path, os.path.join(self.deploy_dir, "index.html"))
            shutil.copy2(dashboard_path, os.path.join(self.deploy_dir, "dashboard.html"))
        
        # Save JSON data
        json_data = []
        for project in projects:
            p = project.copy()
            if p["start_date"]:
                p["start_date"] = p["start_date"].isoformat()
            if p["end_date"]:
                p["end_date"] = p["end_date"].isoformat()
            json_data.append(p)
        
        json_path = os.path.join(self.output_dir, "projects.json")
        with open(json_path, "w") as f:
            json.dump(json_data, f, indent=2)
        outputs['json'] = json_path
        
        return outputs

    # File watching functionality
    def get_file_checksum(self, filepath):
        """Get file checksum for change detection"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def scan_markdown_files(self):
        """Find all markdown files in project directory"""
        files = []
        for root, dirs, filenames in os.walk(self.projects_root):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for filename in filenames:
                if filename.endswith('.md') and not filename.startswith('.'):
                    files.append(os.path.join(root, filename))
        return files

    def check_for_changes(self):
        """Check for file changes"""
        current_files = self.scan_markdown_files()
        changes = []
        
        for filepath in current_files:
            checksum = self.get_file_checksum(filepath)
            if checksum is None:
                continue
                
            if filepath not in self.file_checksums:
                changes.append(('new', filepath))
            elif self.file_checksums[filepath] != checksum:
                changes.append(('modified', filepath))
            
            self.file_checksums[filepath] = checksum
        
        # Check for deleted files
        for filepath in list(self.file_checksums.keys()):
            if filepath not in current_files:
                changes.append(('deleted', filepath))
                del self.file_checksums[filepath]
        
        return changes

    def start_file_watcher(self, check_interval=5):
        """Start watching files for changes"""
        print("Starting file watcher...")
        print(f"Watching: {self.projects_root}")
        print("Press Ctrl+C to stop")
        print("=" * 50)
        
        # Initial scan
        initial_files = self.scan_markdown_files()
        for filepath in initial_files:
            self.file_checksums[filepath] = self.get_file_checksum(filepath)
        
        print(f"Monitoring {len(initial_files)} markdown files")
        
        # Initial generation
        print("Generating initial charts...")
        self.generate_all_outputs()
        print("Charts available at:", self.deploy_dir)
        
        # Watch loop
        try:
            while self.running:
                time.sleep(check_interval)
                changes = self.check_for_changes()
                
                if changes:
                    current_time = time.time()
                    if current_time - self.last_regeneration >= self.regeneration_cooldown:
                        self.last_regeneration = current_time
                        
                        print(f"\\nChanges detected at {datetime.now().strftime('%H:%M:%S')}")
                        for change_type, filepath in changes:
                            rel_path = os.path.relpath(filepath, self.projects_root)
                            print(f"  {change_type}: {rel_path}")
                        
                        print("Regenerating charts...")
                        self.generate_all_outputs()
                        print("Update complete!")
                        
        except KeyboardInterrupt:
            print("\\nStopping file watcher...")
            self.running = False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Unified DCLT Project System")
    parser.add_argument('--action', choices=['generate', 'watch'], default='generate',
                       help='Action to perform')
    parser.add_argument('--projects-dir', default='data/dclt/02_EXECUTION/10_Projects',
                       help='Projects directory')
    parser.add_argument('--output-dir', help='Output directory (optional)')
    parser.add_argument('--watch-interval', type=int, default=5, 
                       help='File watch check interval in seconds')
    
    args = parser.parse_args()
    
    # Create system instance
    system = UnifiedProjectSystem(
        projects_root=args.projects_dir,
        output_dir=args.output_dir
    )
    
    if args.action == 'generate':
        print("Generating project charts and dashboards...")
        outputs = system.generate_all_outputs()
        print("\\nGenerated files:")
        for output_type, path in outputs.items():
            print(f"  {output_type}: {path}")
    
    elif args.action == 'watch':
        system.start_file_watcher(args.watch_interval)

if __name__ == "__main__":
    main()