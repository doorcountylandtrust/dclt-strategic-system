# DCLT Strategic System

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
