# DCLT Active Scripts Directory

## Active Scripts (Post-Cleanup)

### 🎯 Primary Workflow
**Location**: `scripts/visualization/unified_project_system.py`
**Purpose**: Complete project management system with dashboard, Gantt chart, and JSON export
**Usage**:
```bash
source venv/bin/activate
python3 scripts/visualization/unified_project_system.py --action generate
```

### 📊 Specialized Generators
- **`scripts/visualization/advanced_gantt_generator.py`** - Professional DHTMLX Gantt charts
- **`scripts/visualization/figjam_style_generator.py`** - FigJam-style swim lane timelines
- **`scripts/automation/simple_file_watcher.py`** - Live file watching for auto-regeneration

### 🧹 Utility Scripts
- **`scripts/cleanup_file_names.py`** - Standardize file naming across project
- **`scripts/data_cleanup/`** - Data quality and auditing tools
- **`scripts/data_organization/`** - Hierarchy management tools

## Archived Scripts

**Location**: `scripts/archive/`
- `generate_gantt.py` - Obsolete Gantt generator
- `generate_projects_dashboard.py` - Obsolete dashboard generator

## Requirements

**Virtual Environment Required**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install python-frontmatter
```

## Quick Start

1. **Activate environment**: `source venv/bin/activate`
2. **Generate all visualizations**: `python3 scripts/visualization/unified_project_system.py --action generate`
3. **View outputs**: Check `data/dclt/02_EXECUTION/10_Projects/dashboards/`

---
**Last Updated**: 2025-09-18 (Post-Cleanup)
**Status**: All scripts operational and tested