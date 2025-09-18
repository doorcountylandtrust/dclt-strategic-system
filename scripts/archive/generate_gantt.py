#!/usr/bin/env python3
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
