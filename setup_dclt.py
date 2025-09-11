#!/usr/bin/env python3
"""
DCLT Strategic System Project Scaffolding
Creates the directory structure and initial files for the strategic planning system.
"""

import os
import yaml
from pathlib import Path

def create_project_structure():
    """Create the main project directory structure"""
    
    directories = [
        "data",
        "data/1-strategy",
        "data/2-execution", 
        "data/3-reference-tools",
        "scripts",
        "scripts/utils",
        "output",
        "output/gantt_charts",
        "output/reports",
        "templates",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_config_files():
    """Create configuration files"""
    
    # Main settings configuration
    settings = {
        'timeline_types': ['project', 'initiative', 'campaign'],
        'timeline_statuses': ['active', 'planned', 'in-progress'],
        'scan_paths': ['data/1-strategy', 'data/2-execution'],
        'ignore_paths': ['data/3-reference-tools'],
        'gantt_output': 'output/gantt_charts/dclt_timeline.html',
        'default_timeline_duration_weeks': 12
    }
    
    with open('config/settings.yaml', 'w') as f:
        yaml.dump(settings, f, default_flow_style=False, indent=2)
    
    print("Created config/settings.yaml")

def create_templates():
    """Create markdown templates with proper YAML frontmatter"""
    
    project_template = """---
title: "Project Title"
type: "project"  # project | initiative | campaign | research | reference
status: "planned"  # active | planned | in-progress | completed | on-hold | someday
timeline:
  start: "2024-01-15"  # YYYY-MM-DD format
  end: "2024-06-30"
  estimated_hours: 40
priority: "medium"  # critical | high | medium | low
tags: 
  - "strategic-planning"
  - "communications"
owner: "team-member-name"
dependencies: []  # List of other project IDs this depends on
gantt_display: true  # Include in timeline visualization
---

# Project Title

## Overview
Brief description of the project and its objectives.

## Goals
- Goal 1
- Goal 2

## Timeline & Milestones
Key milestones and deadlines.

## Resources Needed
What resources, people, or tools are required.

## Success Metrics
How will we measure success.
"""

    initiative_template = """---
title: "Strategic Initiative"
type: "initiative"
status: "active"
timeline:
  start: "2024-01-01"
  end: "2024-12-31"
priority: "high"
tags:
  - "strategic-initiative"
owner: "leadership-team"
gantt_display: true
---

# Strategic Initiative Title

## Strategic Context
Why this initiative matters to DCLT's mission.

## Key Components
Major workstreams and projects under this initiative.

## Success Metrics
Measurable outcomes and KPIs.
"""

    reference_template = """---
title: "Reference Document"
type: "reference"
status: "completed"
tags:
  - "reference"
  - "documentation"
gantt_display: false
---

# Reference Document Title

## Purpose
What this document contains and when to reference it.

## Key Information
Core content and insights.
"""

    # Write templates
    templates = {
        'project_template.md': project_template,
        'initiative_template.md': initiative_template,
        'reference_template.md': reference_template
    }
    
    for filename, content in templates.items():
        with open(f'templates/{filename}', 'w') as f:
            f.write(content)
        print(f"Created templates/{filename}")

def create_parsing_script():
    """Create the main frontmatter parsing script"""
    
    parsing_script = '''#!/usr/bin/env python3
"""
DCLT Strategic System - Frontmatter Parser
Scans all markdown files and extracts YAML frontmatter for analysis.
"""

import os
import yaml
import re
from pathlib import Path
from datetime import datetime
import json

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for YAML frontmatter
        if content.startswith('---'):
            # Find the closing ---
            end_marker = content.find('---', 3)
            if end_marker != -1:
                yaml_content = content[3:end_marker].strip()
                try:
                    metadata = yaml.safe_load(yaml_content)
                    return metadata
                except yaml.YAMLError as e:
                    print(f"YAML error in {file_path}: {e}")
                    return None
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def scan_files(base_path, scan_paths):
    """Scan specified paths for markdown files"""
    all_files = []
    
    for scan_path in scan_paths:
        full_path = Path(base_path) / scan_path
        if full_path.exists():
            for md_file in full_path.rglob('*.md'):
                all_files.append(md_file)
    
    return all_files

def main():
    """Main parsing function"""
    # Load configuration
    try:
        with open('config/settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found. Run setup script first.")
        return
    
    # Scan for markdown files
    base_path = Path('.')
    scan_paths = config.get('scan_paths', ['data'])
    
    markdown_files = scan_files(base_path, scan_paths)
    print(f"Found {len(markdown_files)} markdown files")
    
    # Extract frontmatter from all files
    all_metadata = []
    for file_path in markdown_files:
        metadata = extract_frontmatter(file_path)
        if metadata:
            metadata['file_path'] = str(file_path)
            metadata['last_modified'] = datetime.fromtimestamp(
                file_path.stat().st_mtime
            ).isoformat()
            all_metadata.append(metadata)
    
    # Save extracted metadata
    output_path = Path('output/reports/extracted_metadata.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_metadata, f, indent=2, default=str)
    
    print(f"Extracted metadata from {len(all_metadata)} files")
    print(f"Results saved to {output_path}")
    
    # Print summary
    types = {}
    statuses = {}
    for item in all_metadata:
        item_type = item.get('type', 'unknown')
        item_status = item.get('status', 'unknown')
        types[item_type] = types.get(item_type, 0) + 1
        statuses[item_status] = statuses.get(item_status, 0) + 1
    
    print("\\nSummary by type:")
    for type_name, count in types.items():
        print(f"  {type_name}: {count}")
    
    print("\\nSummary by status:")
    for status_name, count in statuses.items():
        print(f"  {status_name}: {count}")

if __name__ == "__main__":
    main()
'''
    
    with open('scripts/parse_frontmatter.py', 'w') as f:
        f.write(parsing_script)
    
    print("Created scripts/parse_frontmatter.py")

def create_gantt_script():
    """Create basic Gantt chart generation script"""
    
    gantt_script = '''#!/usr/bin/env python3
"""
DCLT Strategic System - Gantt Chart Generator
Creates timeline visualizations from parsed frontmatter data.
"""

import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path

def load_metadata():
    """Load the extracted metadata from parsing script"""
    try:
        with open('output/reports/extracted_metadata.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No metadata found. Run parse_frontmatter.py first.")
        return []

def filter_timeline_items(metadata, config):
    """Filter items that should appear on timeline"""
    timeline_items = []
    
    valid_types = config.get('timeline_types', [])
    valid_statuses = config.get('timeline_statuses', [])
    
    for item in metadata:
        # Check if item should be displayed on timeline
        if not item.get('gantt_display', False):
            continue
            
        item_type = item.get('type', '')
        item_status = item.get('status', '')
        
        if item_type in valid_types and item_status in valid_statuses:
            # Check if timeline data exists
            timeline = item.get('timeline', {})
            if timeline.get('start') and timeline.get('end'):
                timeline_items.append(item)
    
    return timeline_items

def generate_simple_gantt_html(timeline_items, output_path):
    """Generate a simple HTML Gantt chart"""
    
    html_template = """<!DOCTYPE html>
<html>
<head>
    <title>DCLT Strategic Timeline</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .gantt-container { overflow-x: auto; }
        .gantt-item { margin: 10px 0; padding: 10px; border-left: 4px solid #007acc; background: #f0f8ff; }
        .timeline-bar { height: 20px; background: #007acc; margin: 5px 0; border-radius: 3px; }
        .item-title { font-weight: bold; color: #333; }
        .item-meta { color: #666; font-size: 0.9em; }
        .priority-critical { border-left-color: #e74c3c; }
        .priority-high { border-left-color: #f39c12; }
        .priority-medium { border-left-color: #2ecc71; }
        .priority-low { border-left-color: #95a5a6; }
    </style>
</head>
<body>
    <h1>DCLT Strategic Timeline</h1>
    <div class="gantt-container">
"""
    
    for item in sorted(timeline_items, key=lambda x: x.get('timeline', {}).get('start', '')):
        title = item.get('title', 'Untitled')
        timeline = item.get('timeline', {})
        priority = item.get('priority', 'medium')
        status = item.get('status', 'unknown')
        item_type = item.get('type', 'unknown')
        
        start_date = timeline.get('start', '')
        end_date = timeline.get('end', '')
        
        html_template += f"""
        <div class="gantt-item priority-{priority}">
            <div class="item-title">{title}</div>
            <div class="item-meta">
                Type: {item_type} | Status: {status} | Priority: {priority}<br>
                Timeline: {start_date} to {end_date}
            </div>
            <div class="timeline-bar"></div>
        </div>
        """
    
    html_template += """
    </div>
    <p><em>Generated on """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</em></p>
</body>
</html>"""
    
    with open(output_path, 'w') as f:
        f.write(html_template)
    
    print(f"Gantt chart saved to {output_path}")

def main():
    """Main Gantt generation function"""
    # Load configuration
    try:
        with open('config/settings.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Config file not found. Run setup script first.")
        return
    
    # Load metadata
    metadata = load_metadata()
    if not metadata:
        return
    
    # Filter for timeline items
    timeline_items = filter_timeline_items(metadata, config)
    print(f"Found {len(timeline_items)} items for timeline")
    
    if not timeline_items:
        print("No timeline items found. Check your frontmatter and config settings.")
        return
    
    # Generate Gantt chart
    output_path = Path(config.get('gantt_output', 'output/gantt_charts/timeline.html'))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    generate_simple_gantt_html(timeline_items, output_path)

if __name__ == "__main__":
    main()
'''
    
    with open('scripts/generate_gantt.py', 'w') as f:
        f.write(gantt_script)
    
    print("Created scripts/generate_gantt.py")

def create_requirements():
    """Create requirements.txt file"""
    requirements = """PyYAML>=6.0
pathlib
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("Created requirements.txt")

def create_readme():
    """Create project README"""
    readme = """# DCLT Strategic System

A markdown-based strategic planning system with automated timeline visualization.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Place your exported Notion files in the `data/` directories

3. Run the parsing script:
   ```bash
   python scripts/parse_frontmatter.py
   ```

4. Generate timeline visualization:
   ```bash
   python scripts/generate_gantt.py
   ```

## File Structure

- `data/` - Your markdown files organized by category
- `scripts/` - Processing and generation scripts
- `output/` - Generated reports and visualizations
- `templates/` - Markdown templates for new documents
- `config/` - System configuration

## YAML Frontmatter Format

Each strategic document should include frontmatter like:

```yaml
---
title: "Project Name"
type: "project"
status: "active"
timeline:
  start: "2024-01-15"
  end: "2024-06-30"
priority: "high"
gantt_display: true
---
```

## Usage

1. Edit markdown files with proper frontmatter
2. Run parsing script to extract metadata
3. Generate Gantt charts and reports
4. Iterate and refine your strategic planning
"""
    
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print("Created README.md")

def main():
    """Main setup function"""
    print("Setting up DCLT Strategic System...")
    
    create_project_structure()
    create_config_files()
    create_templates()
    create_parsing_script()
    create_gantt_script()
    create_requirements()
    create_readme()
    
    print("\n✅ Project scaffolding complete!")
    print("\nNext steps:")
    print("1. pip install -r requirements.txt")
    print("2. Copy your Notion export files to the data/ directories")
    print("3. python scripts/parse_frontmatter.py")
    print("4. python scripts/generate_gantt.py")

if __name__ == "__main__":
    main()