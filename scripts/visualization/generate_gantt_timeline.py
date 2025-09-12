#!/usr/bin/env python3
"""
Generate Gantt Chart from DCLT Strategic Timeline Data
Parse markdown files with timeline data and create interactive Gantt visualization
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import json
from collections import defaultdict

class DCLTGanttGenerator:
    def __init__(self, data_dir='data/dclt'):
        self.data_dir = Path(data_dir)
        self.projects = []
        self.tasks = []
        self.stats = {
            'files_scanned': 0,
            'files_with_dates': 0,
            'tasks_found': 0,
            'projects_found': 0
        }
    
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
            return yaml.safe_load(frontmatter_text), body_content
        except:
            return None, content
    
    def parse_date(self, date_str):
        """Parse various date formats to datetime object"""
        if not date_str:
            return None
            
        date_str = str(date_str).strip()
        
        # Try different date formats
        formats = [
            '%Y-%m-%d',      # 2025-07-15
            '%B %d, %Y',     # July 15, 2025
            '%b %d, %Y',     # Jul 15, 2025
            '%m/%d/%Y',      # 07/15/2025
            '%d-%m-%Y',      # 15-07-2025
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def extract_dates_from_content(self, content):
        """Extract dates from markdown content"""
        dates = {}
        
        # Look for various date patterns
        patterns = [
            (r'Start Date:\s*(.+)', 'start_date'),
            (r'End Date:\s*(.+)', 'end_date'),
            (r'Due Date:\s*(.+)', 'due_date'),
            (r'Date:\s*(.+)', 'date'),
        ]
        
        for pattern, key in patterns:
            match = re.search(pattern, content)
            if match:
                date_val = match.group(1).strip()
                parsed_date = self.parse_date(date_val)
                if parsed_date:
                    dates[key] = parsed_date
        
        return dates
    
    def classify_project_type(self, file_path, frontmatter):
        """Classify the type of project/task based on path and metadata"""
        path_str = str(file_path)
        
        if 'Master Task Tracker' in path_str:
            return 'execution-task'
        elif '1 STRATEGY' in path_str:
            return 'strategy'
        elif '2 EXECUTION' in path_str:
            return 'execution'
        elif '3 REFERENCE' in path_str:
            return 'reference'
        else:
            return 'other'
    
    def determine_priority_color(self, priority, status):
        """Determine color based on priority and status"""
        priority_colors = {
            'critical': '#e74c3c',  # Red
            'high': '#f39c12',      # Orange
            'medium': '#3498db',    # Blue  
            'low': '#95a5a6'        # Gray
        }
        
        status_colors = {
            'completed': '#2ecc71',    # Green
            'in_progress': '#f1c40f',  # Yellow
            'planned': '#9b59b6',      # Purple
            'on_hold': '#95a5a6'       # Gray
        }
        
        # Status takes precedence
        if status and status.lower() in status_colors:
            return status_colors[status.lower()]
        
        # Fall back to priority
        if priority and priority.lower() in priority_colors:
            return priority_colors[priority.lower()]
        
        return '#3498db'  # Default blue
    
    def scan_for_timeline_data(self):
        """Scan all markdown files for timeline data"""
        print("Scanning DCLT files for timeline data...")
        
        for file_path in self.data_dir.rglob('*.md'):
            self.stats['files_scanned'] += 1
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter and dates from content
                frontmatter, body = self.extract_frontmatter(content)
                content_dates = self.extract_dates_from_content(content)
                
                if not content_dates and not frontmatter:
                    continue
                
                # Build task data
                task_data = {
                    'name': frontmatter.get('title', file_path.stem) if frontmatter else file_path.stem,
                    'file_path': str(file_path.relative_to(self.data_dir)),
                    'type': self.classify_project_type(file_path, frontmatter),
                    'priority': frontmatter.get('priority', 'medium') if frontmatter else 'medium',
                    'status': frontmatter.get('project_status', 'planned') if frontmatter else 'planned',
                    'stakeholders': frontmatter.get('stakeholders', []) if frontmatter else [],
                    'tags': frontmatter.get('tags', []) if frontmatter else []
                }
                
                # Add date information
                start_date = None
                end_date = None
                
                # Priority: content dates > frontmatter dates
                if 'start_date' in content_dates:
                    start_date = content_dates['start_date']
                elif 'date' in content_dates:
                    start_date = content_dates['date']
                elif frontmatter and 'created_date' in frontmatter:
                    start_date = self.parse_date(frontmatter['created_date'])
                
                if 'end_date' in content_dates:
                    end_date = content_dates['end_date']
                elif 'due_date' in content_dates:
                    end_date = content_dates['due_date']
                
                # If we have at least one date, include this task
                if start_date or end_date:
                    self.stats['files_with_dates'] += 1
                    
                    # Set defaults if missing dates
                    if start_date and not end_date:
                        # Default to 1 week duration
                        end_date = start_date + timedelta(days=7)
                    elif end_date and not start_date:
                        # Default to 1 week before end
                        start_date = end_date - timedelta(days=7)
                    
                    task_data.update({
                        'start_date': start_date,
                        'end_date': end_date,
                        'color': self.determine_priority_color(task_data['priority'], task_data['status'])
                    })
                    
                    self.tasks.append(task_data)
                    self.stats['tasks_found'] += 1
                    
                    print(f"✅ Found timeline: {task_data['name']} ({start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')})")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    
    def group_tasks_by_category(self):
        """Group tasks by type for better visualization"""
        grouped = defaultdict(list)
        
        for task in sorted(self.tasks, key=lambda x: x['start_date']):
            grouped[task['type']].append(task)
        
        return grouped
    
    def generate_gantt_html(self):
        """Generate HTML Gantt chart using Chart.js"""
        grouped_tasks = self.group_tasks_by_category()
        
        # Prepare data for Chart.js
        datasets = []
        labels = []
        
        type_names = {
            'strategy': '📋 Strategy Planning',
            'execution': '🚀 Execution Tasks', 
            'execution-task': '⚡ Master Task Tracker',
            'reference': '📚 Reference & Research',
            'other': '📁 Other Projects'
        }
        
        for task_type, tasks in grouped_tasks.items():
            for task in tasks:
                labels.append(task['name'][:50] + ('...' if len(task['name']) > 50 else ''))
                
                datasets.append({
                    'label': type_names.get(task_type, task_type.title()),
                    'data': [{
                        'x': [task['start_date'].strftime('%Y-%m-%d'), task['end_date'].strftime('%Y-%m-%d')],
                        'y': task['name'][:50] + ('...' if len(task['name']) > 50 else ''),
                        'status': task['status'],
                        'priority': task['priority'],
                        'file_path': task['file_path']
                    }],
                    'backgroundColor': task['color'],
                    'borderColor': task['color'],
                    'borderWidth': 1
                })
        
        # Generate HTML
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DCLT Strategic Timeline - Gantt Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f8f9fa;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            height: 80vh;
        }}
        .legend {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
            justify-content: center;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9em;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🗓️ DCLT Strategic Timeline</h1>
        <p>Gantt Chart Visualization of Strategic Planning & Execution Projects</p>
        <p><em>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{self.stats['files_scanned']}</div>
            <div>Files Scanned</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{self.stats['files_with_dates']}</div>
            <div>Files with Timeline Data</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{self.stats['tasks_found']}</div>
            <div>Timeline Items</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(grouped_tasks)}</div>
            <div>Project Categories</div>
        </div>
    </div>
    
    <div class="legend">
        <div class="legend-item">
            <div class="legend-color" style="background: #2ecc71;"></div>
            <span>Completed</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #f1c40f;"></div>
            <span>In Progress</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #9b59b6;"></div>
            <span>Planned</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #e74c3c;"></div>
            <span>Critical Priority</span>
        </div>
        <div class="legend-item">
            <div class="legend-color" style="background: #f39c12;"></div>
            <span>High Priority</span>
        </div>
    </div>
    
    <div class="chart-container">
        <canvas id="ganttChart"></canvas>
    </div>
    
    <script>
        // Simple Gantt-like visualization using horizontal bar chart
        const ctx = document.getElementById('ganttChart').getContext('2d');
        
        const chartData = {json.dumps(datasets, default=str)};
        
        // Convert to horizontal bar chart format
        const tasks = [];
        const colors = [];
        const data = [];
        
        chartData.forEach(item => {{
            tasks.push(item.data[0].y);
            colors.push(item.backgroundColor);
            
            const start = new Date(item.data[0].x[0]);
            const end = new Date(item.data[0].x[1]);
            const duration = (end - start) / (1000 * 60 * 60 * 24); // days
            
            data.push({{
                x: duration,
                y: item.data[0].y,
                start: start,
                end: end,
                status: item.data[0].status,
                priority: item.data[0].priority,
                file_path: item.data[0].file_path
            }});
        }});
        
        const chart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: tasks,
                datasets: [{{
                    label: 'Task Duration (Days)',
                    data: data.map(item => item.x),
                    backgroundColor: colors,
                    borderColor: colors,
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                scales: {{
                    x: {{
                        title: {{
                            display: true,
                            text: 'Duration (Days)'
                        }},
                        grid: {{
                            display: true
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: 'Strategic Projects & Tasks'
                        }}
                    }}
                }},
                plugins: {{
                    tooltip: {{
                        callbacks: {{
                            title: function(context) {{
                                const item = data[context[0].dataIndex];
                                return item.y;
                            }},
                            label: function(context) {{
                                const item = data[context.dataIndex];
                                return [
                                    `Duration: ${{item.x}} days`,
                                    `Start: ${{item.start.toLocaleDateString()}}`,
                                    `End: ${{item.end.toLocaleDateString()}}`,
                                    `Status: ${{item.status}}`,
                                    `Priority: ${{item.priority}}`,
                                    `File: ${{item.file_path}}`
                                ];
                            }}
                        }}
                    }},
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html_content
    
    def generate_data_quality_report(self):
        """Generate report on timeline data quality"""
        report = f"""# DCLT Timeline Data Quality Report
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Summary Statistics

- **Total Files Scanned**: {self.stats['files_scanned']}
- **Files with Timeline Data**: {self.stats['files_with_dates']}
- **Timeline Items Found**: {self.stats['tasks_found']}
- **Coverage Rate**: {(self.stats['files_with_dates']/self.stats['files_scanned']*100):.1f}%

## Timeline Data by Category

"""
        grouped = self.group_tasks_by_category()
        
        for category, tasks in grouped.items():
            report += f"### {category.title().replace('_', ' ')} ({len(tasks)} items)\n\n"
            for task in sorted(tasks, key=lambda x: x['start_date']):
                duration = (task['end_date'] - task['start_date']).days
                report += f"- **{task['name']}** ({task['start_date'].strftime('%Y-%m-%d')} → {task['end_date'].strftime('%Y-%m-%d')}, {duration} days) - {task['status']}\n"
            report += "\n"
        
        report += """## Recommendations

### Files with Good Timeline Data
- Master Task Tracker files have comprehensive start/end dates
- Land Seller Experience Study has detailed milestone tracking
- Some execution tasks have clear deliverable dates

### Files Needing Timeline Enhancement
- Many strategic documents lack specific dates
- Reference documents could benefit from review/update cycles
- Some execution plans need start date definitions

### Data Quality Improvements
1. **Add date fields to frontmatter** for documents missing them
2. **Standardize date formats** across all documents
3. **Include milestone tracking** for longer strategic initiatives
4. **Add review cycles** for reference documents
5. **Define project phases** with clear deliverable dates

"""
        return report

def main():
    """Generate Gantt chart and data quality report"""
    generator = DCLTGanttGenerator()
    generator.scan_for_timeline_data()
    
    # Generate outputs
    output_dir = Path('output/reports')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate Gantt chart HTML
    gantt_html = generator.generate_gantt_html()
    gantt_path = output_dir / 'dclt_strategic_timeline_gantt.html'
    with open(gantt_path, 'w', encoding='utf-8') as f:
        f.write(gantt_html)
    
    # Generate data quality report
    quality_report = generator.generate_data_quality_report()
    report_path = output_dir / 'dclt_timeline_data_quality.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(quality_report)
    
    print(f"\n📊 Gantt Chart Generated: {gantt_path}")
    print(f"📋 Data Quality Report: {report_path}")
    print(f"\n✅ Found {generator.stats['tasks_found']} timeline items from {generator.stats['files_with_dates']} files")

if __name__ == '__main__':
    main()