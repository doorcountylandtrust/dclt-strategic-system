#!/usr/bin/env python3
"""
FigJam-Style Project Visualization Generator
Creates rich, visual project timelines with swim lanes, varied heights, and strategic grouping
"""

import os
import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path
import re
import math

class FigJamStyleVisualizer:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.projects = []
        self.strategic_themes = {}
        self.colors = {
            'discovery': '#4A90E2',      # Blue
            'strategy': '#7B68EE',       # Medium Slate Blue  
            'execution': '#50C878',      # Emerald Green
            'branding': '#FF6B35',       # Orange Red
            'milestone': '#FFD700',      # Gold
            'critical': '#FF4757',       # Red
            'high': '#FF6B35',          # Orange  
            'medium': '#4A90E2',        # Blue
            'low': '#95A5A6',           # Gray
            'completed': '#27AE60',     # Green
            'in_progress': '#F39C12',   # Orange
            'planned': '#3498DB'        # Light Blue
        }
        
    def load_projects(self):
        """Load and parse all project files"""
        print("🔍 Loading project data...")
        
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.md') and not file.startswith('_'):
                    file_path = os.path.join(root, file)
                    project_data = self.parse_project_file(file_path)
                    if project_data:
                        self.projects.append(project_data)
        
        print(f"✅ Loaded {len(self.projects)} projects")
        return self.projects
    
    def parse_project_file(self, file_path):
        """Parse markdown file and extract project metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract frontmatter
            frontmatter = self.extract_frontmatter(content)
            if not frontmatter:
                return None
                
            # Extract title from frontmatter or filename
            title = frontmatter.get('title', os.path.basename(file_path).replace('.md', ''))
            
            # Determine project data
            project = {
                'title': title,
                'file_path': file_path,
                'frontmatter': frontmatter,
                'content': content,
                'project_type': self.determine_project_type(frontmatter, file_path),
                'strategic_theme': self.determine_strategic_theme(frontmatter, file_path),
                'visual_priority': self.calculate_visual_priority(frontmatter),
                'timeline': self.extract_timeline(frontmatter),
                'status': frontmatter.get('project_status', 'planned'),
                'priority': frontmatter.get('priority', 'medium'),
                'description': self.extract_description(content),
                'team': frontmatter.get('assigned_to', []),
                'is_milestone': frontmatter.get('is_milestone', False)
            }
            
            return project
            
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return None
    
    def extract_frontmatter(self, content):
        """Extract YAML frontmatter from markdown content"""
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
    
    def determine_project_type(self, frontmatter, file_path):
        """Determine project type for visual grouping"""
        project_type = frontmatter.get('project_type', '')
        
        if frontmatter.get('is_milestone'):
            return 'milestone'
        elif 'strategy' in file_path.lower() or project_type == 'strategy':
            return 'strategy'
        elif 'brand' in file_path.lower() or 'brand' in frontmatter.get('tags', []):
            return 'branding'
        elif project_type in ['execution', 'implementation']:
            return 'execution'
        else:
            return 'discovery'
    
    def determine_strategic_theme(self, frontmatter, file_path):
        """Determine strategic theme for swim lane grouping"""
        theme = frontmatter.get('strategic_theme', '')
        if theme:
            return theme
            
        # Infer from file path
        if 'brand' in file_path.lower():
            return 'Brand Excellence'
        elif 'website' in file_path.lower():
            return 'Digital Transformation'
        elif 'strategy' in file_path.lower():
            return 'Strategic Planning'
        elif 'execution' in file_path.lower():
            return 'Implementation'
        else:
            return 'Foundation Building'
    
    def calculate_visual_priority(self, frontmatter):
        """Calculate visual prominence (height/size) based on project importance"""
        priority = frontmatter.get('priority', 'medium')
        project_type = frontmatter.get('project_type', 'task')
        
        base_height = 40
        
        # Adjust by priority
        priority_multiplier = {
            'critical': 1.8,
            'high': 1.4,
            'medium': 1.0,
            'low': 0.7
        }.get(priority, 1.0)
        
        # Adjust by project type
        type_multiplier = {
            'epic': 2.0,
            'project': 1.5,
            'milestone': 1.2,
            'task': 1.0
        }.get(project_type, 1.0)
        
        return int(base_height * priority_multiplier * type_multiplier)
    
    def extract_timeline(self, frontmatter):
        """Extract and standardize timeline information"""
        start_date = self.parse_date(frontmatter.get('start_date'))
        end_date = self.parse_date(frontmatter.get('end_date'))
        
        if not start_date and not end_date:
            # Use current date as default
            start_date = datetime.now()
            end_date = start_date + timedelta(days=30)
        elif start_date and not end_date:
            duration = frontmatter.get('duration_days', 30)
            end_date = start_date + timedelta(days=duration)
        elif end_date and not start_date:
            duration = frontmatter.get('duration_days', 30)
            start_date = end_date - timedelta(days=duration)
            
        return {
            'start_date': start_date,
            'end_date': end_date,
            'duration_days': (end_date - start_date).days if start_date and end_date else 30
        }
    
    def parse_date(self, date_str):
        """Parse various date formats"""
        if not date_str:
            return None
            
        try:
            if isinstance(date_str, str):
                return datetime.strptime(date_str, '%Y-%m-%d')
            elif isinstance(date_str, datetime):
                return date_str
        except:
            return None
        return None
    
    def extract_description(self, content):
        """Extract meaningful description from content"""
        # Remove frontmatter
        if content.startswith('---'):
            content = content.split('---', 2)[-1]
        
        # Get first paragraph or summary
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Find first substantial content
        for line in lines:
            if len(line) > 20 and not line.startswith('#'):
                return line[:100] + "..." if len(line) > 100 else line
        
        return "Strategic project initiative"
    
    def group_by_swim_lanes(self):
        """Group projects into swim lanes by strategic theme and timeline"""
        swim_lanes = {}
        
        for project in self.projects:
            theme = project['strategic_theme']
            if theme not in swim_lanes:
                swim_lanes[theme] = []
            swim_lanes[theme].append(project)
        
        # Sort projects within each lane by start date
        for theme in swim_lanes:
            swim_lanes[theme].sort(key=lambda p: p['timeline']['start_date'] or datetime.now())
        
        return swim_lanes
    
    def calculate_timeline_bounds(self):
        """Calculate the overall timeline bounds for the visualization"""
        all_dates = []
        
        for project in self.projects:
            if project['timeline']['start_date']:
                all_dates.append(project['timeline']['start_date'])
            if project['timeline']['end_date']:
                all_dates.append(project['timeline']['end_date'])
        
        if not all_dates:
            start_date = datetime.now()
            end_date = start_date + timedelta(days=365)
        else:
            start_date = min(all_dates) - timedelta(days=30)
            end_date = max(all_dates) + timedelta(days=30)
        
        return start_date, end_date
    
    def generate_figjam_style_html(self):
        """Generate FigJam-style project visualization"""
        print("🎨 Generating FigJam-style visualization...")
        
        swim_lanes = self.group_by_swim_lanes()
        start_date, end_date = self.calculate_timeline_bounds()
        total_days = (end_date - start_date).days
        
        html_content = self.create_html_template()
        
        # Generate swim lanes
        lanes_html = ""
        lane_y = 100  # Starting Y position
        
        for theme, projects in swim_lanes.items():
            lanes_html += self.generate_swim_lane(theme, projects, lane_y, start_date, total_days)
            lane_y += self.calculate_lane_height(projects) + 60  # Lane spacing
        
        # Generate timeline header
        timeline_html = self.generate_timeline_header(start_date, end_date)
        
        html_content = html_content.replace('{{TIMELINE_HEADER}}', timeline_html)
        html_content = html_content.replace('{{SWIM_LANES}}', lanes_html)
        html_content = html_content.replace('{{TOTAL_HEIGHT}}', str(lane_y + 100))
        
        return html_content
    
    def generate_swim_lane(self, theme, projects, y_pos, start_date, total_days):
        """Generate a single swim lane with projects"""
        lane_html = f"""
        <g class="swim-lane" data-theme="{theme}">
            <!-- Lane Background -->
            <rect x="0" y="{y_pos}" width="100%" height="{self.calculate_lane_height(projects)}" 
                  fill="rgba(248,249,250,0.3)" stroke="#dee2e6" stroke-width="1" rx="8"/>
            
            <!-- Lane Label -->
            <text x="20" y="{y_pos + 25}" class="lane-label">{theme}</text>
            
            <!-- Projects in Lane -->
        """
        
        project_y = y_pos + 40
        for project in projects:
            lane_html += self.generate_project_box(project, project_y, start_date, total_days)
            project_y += project['visual_priority'] + 15  # Project spacing
        
        lane_html += "</g>"
        return lane_html
    
    def generate_project_box(self, project, y_pos, start_date, total_days):
        """Generate a single project box with FigJam-style design"""
        timeline = project['timeline']
        
        if not timeline['start_date'] or not timeline['end_date']:
            return ""
        
        # Calculate position and width
        start_offset = (timeline['start_date'] - start_date).days
        duration = timeline['duration_days']
        
        x_pos = 200 + (start_offset / total_days) * 1200  # Scale to fit
        width = (duration / total_days) * 1200
        width = max(width, 80)  # Minimum width
        
        height = project['visual_priority']
        
        # Choose colors
        primary_color = self.get_project_color(project)
        text_color = "#ffffff" if self.is_dark_color(primary_color) else "#2c3e50"
        
        # Generate milestone diamond if applicable
        milestone_html = ""
        if project['is_milestone']:
            milestone_html = f"""
            <g class="milestone-marker">
                <polygon points="{x_pos + width/2},{y_pos-20} {x_pos + width/2 + 15},{y_pos-5} {x_pos + width/2},{y_pos+10} {x_pos + width/2 - 15},{y_pos-5}" 
                         fill="#FFD700" stroke="#E6B800" stroke-width="2"/>
                <text x="{x_pos + width/2}" y="{y_pos-25}" text-anchor="middle" class="milestone-label">MILESTONE</text>
            </g>
            """
        
        # Truncate title and description for display
        display_title = project['title'][:30] + "..." if len(project['title']) > 30 else project['title']
        display_desc = project['description'][:50] + "..." if len(project['description']) > 50 else project['description']
        
        project_html = f"""
        <g class="project-box" data-project="{project['title']}" data-status="{project['status']}">
            {milestone_html}
            
            <!-- Project Box -->
            <rect x="{x_pos}" y="{y_pos}" width="{width}" height="{height}" 
                  fill="{primary_color}" stroke="{self.darken_color(primary_color)}" stroke-width="2" 
                  rx="8" class="project-rect"/>
            
            <!-- Project Title -->
            <text x="{x_pos + 10}" y="{y_pos + 20}" fill="{text_color}" class="project-title">
                {display_title}
            </text>
            
            <!-- Project Description -->
            <text x="{x_pos + 10}" y="{y_pos + height - 15}" fill="{text_color}" class="project-description" opacity="0.8">
                {display_desc}
            </text>
            
            <!-- Status Badge -->
            <rect x="{x_pos + width - 80}" y="{y_pos + 5}" width="70" height="20" 
                  fill="{self.get_status_color(project['status'])}" rx="10" opacity="0.9"/>
            <text x="{x_pos + width - 45}" y="{y_pos + 17}" text-anchor="middle" fill="white" class="status-text">
                {project['status'].upper()}
            </text>
            
            <!-- Progress Bar (if in progress) -->
            {self.generate_progress_bar(project, x_pos, y_pos, width, height)}
        </g>
        """
        
        return project_html
    
    def generate_progress_bar(self, project, x_pos, y_pos, width, height):
        """Generate progress bar for in-progress projects"""
        if project['status'] != 'in_progress':
            return ""
            
        progress = project['frontmatter'].get('progress_percent', 50)
        progress_width = (progress / 100) * (width - 20)
        
        return f"""
        <rect x="{x_pos + 10}" y="{y_pos + height - 8}" width="{width - 20}" height="4" 
              fill="rgba(255,255,255,0.3)" rx="2"/>
        <rect x="{x_pos + 10}" y="{y_pos + height - 8}" width="{progress_width}" height="4" 
              fill="rgba(255,255,255,0.8)" rx="2"/>
        """
    
    def generate_timeline_header(self, start_date, end_date):
        """Generate the timeline header with quarters and months"""
        header_html = """
        <g class="timeline-header">
            <!-- Quarter Headers -->
            <rect x="200" y="20" width="1200" height="40" fill="#4A90E2" rx="8"/>
        """
        
        # Generate month divisions
        current_date = start_date
        x_offset = 200
        total_width = 1200
        total_days = (end_date - start_date).days
        
        quarter_colors = ['#E74C3C', '#8E44AD', '#2ECC71', '#F39C12']  # Q1, Q2, Q3, Q4
        current_quarter = (start_date.month - 1) // 3
        
        # Add quarter labels
        quarter_width = total_width / 2  # Assuming 6 months visible
        for i, quarter in enumerate(['Q2 2025', 'Q3 2025']):
            header_html += f"""
            <rect x="{200 + i * quarter_width}" y="20" width="{quarter_width}" height="25" 
                  fill="{quarter_colors[i % 4]}" opacity="0.9"/>
            <text x="{200 + i * quarter_width + quarter_width/2}" y="37" text-anchor="middle" 
                  fill="white" class="quarter-label">{quarter}</text>
            """
        
        # Add month labels
        months = ['April', 'May', 'June', 'July', 'August', 'September']
        month_width = total_width / len(months)
        
        for i, month in enumerate(months):
            month_color = quarter_colors[0] if i < 3 else quarter_colors[1]
            header_html += f"""
            <rect x="{200 + i * month_width}" y="45" width="{month_width}" height="20" 
                  fill="{month_color}" opacity="0.7"/>
            <text x="{200 + i * month_width + month_width/2}" y="57" text-anchor="middle" 
                  fill="white" class="month-label">{month}</text>
            """
        
        header_html += "</g>"
        return header_html
    
    def calculate_lane_height(self, projects):
        """Calculate the height needed for a swim lane"""
        if not projects:
            return 60
        
        total_height = 40  # Lane label space
        for project in projects:
            total_height += project['visual_priority'] + 15  # Project height + spacing
        
        return total_height
    
    def get_project_color(self, project):
        """Get appropriate color for project based on type and status"""
        project_type = project['project_type']
        priority = project['priority']
        status = project['status']
        
        # Priority-based coloring
        if priority == 'critical':
            return self.colors['critical']
        elif project_type in self.colors:
            return self.colors[project_type]
        elif status in self.colors:
            return self.colors[status]
        else:
            return self.colors['medium']
    
    def get_status_color(self, status):
        """Get color for status badge"""
        status_colors = {
            'completed': '#27AE60',
            'in_progress': '#F39C12', 
            'planned': '#3498DB',
            'on_hold': '#95A5A6'
        }
        return status_colors.get(status, '#95A5A6')
    
    def is_dark_color(self, hex_color):
        """Determine if a color is dark (for text contrast)"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        return luminance < 0.5
    
    def darken_color(self, hex_color, factor=0.8):
        """Darken a hex color for borders"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def create_html_template(self):
        """Create the HTML template with FigJam-style CSS"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DCLT Strategic Projects - FigJam Style</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 0;
            background: #f8f9fa;
            overflow-x: auto;
        }
        
        .header {
            background: white;
            padding: 20px;
            border-bottom: 2px solid #dee2e6;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .header h1 {
            margin: 0;
            color: #2c3e50;
            font-size: 24px;
            font-weight: 600;
        }
        
        .header .subtitle {
            color: #6c757d;
            font-size: 14px;
            margin: 5px 0 0 0;
        }
        
        .visualization-container {
            padding: 20px;
            min-width: 1500px;
        }
        
        .project-timeline {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        /* SVG Styles */
        .lane-label {
            font-size: 16px;
            font-weight: 600;
            fill: #2c3e50;
        }
        
        .project-title {
            font-size: 14px;
            font-weight: 600;
        }
        
        .project-description {
            font-size: 12px;
        }
        
        .quarter-label {
            font-size: 14px;
            font-weight: 700;
        }
        
        .month-label {
            font-size: 12px;
            font-weight: 500;
        }
        
        .milestone-label {
            font-size: 10px;
            font-weight: 700;
            fill: #2c3e50;
        }
        
        .status-text {
            font-size: 9px;
            font-weight: 600;
        }
        
        .project-box:hover .project-rect {
            stroke-width: 3;
            filter: brightness(1.1);
        }
        
        .project-box {
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .legend {
            margin: 20px 0;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #dee2e6;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 DCLT Strategic Projects - FigJam Style</h1>
        <p class="subtitle">Rich visual project timeline with swim lanes and strategic grouping</p>
    </div>
    
    <div class="visualization-container">
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background: #4A90E2;"></div>
                Discovery
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #7B68EE;"></div>
                Strategy
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #50C878;"></div>
                Execution
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FF6B35;"></div>
                Branding
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background: #FFD700;"></div>
                Milestone
            </div>
        </div>
        
        <div class="project-timeline">
            <svg width="100%" height="{{TOTAL_HEIGHT}}" viewBox="0 0 1500 {{TOTAL_HEIGHT}}">
                <!-- Timeline Header -->
                {{TIMELINE_HEADER}}
                
                <!-- Swim Lanes -->
                {{SWIM_LANES}}
            </svg>
        </div>
    </div>
    
    <script>
        // Add interactivity
        document.querySelectorAll('.project-box').forEach(box => {
            box.addEventListener('click', function() {
                const projectName = this.dataset.project;
                const status = this.dataset.status;
                alert(`Project: ${projectName}\\nStatus: ${status}`);
            });
        });
        
        console.log("🎨 FigJam-style visualization loaded successfully");
    </script>
</body>
</html>"""

def main():
    generator = FigJamStyleVisualizer()
    generator.load_projects()
    
    html_content = generator.generate_figjam_style_html()
    
    # Save the visualization
    output_dir = Path("output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "dclt_figjam_style_timeline.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ FigJam-style visualization saved to: {output_file}")
    print(f"🌐 Open in browser: file://{output_file.absolute()}")

if __name__ == "__main__":
    main()