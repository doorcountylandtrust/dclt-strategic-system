# DCLT Strategic System - Query & Analysis Scripts

This directory contains powerful query and analysis scripts for strategic planning and project management using the frontmatter data from your DCLT projects.

## 📋 Available Scripts

### 1. `frontmatter_parser.py` - Core Data Infrastructure
**Purpose:** Parses YAML frontmatter from markdown files and provides query capabilities

**Key Features:**
- Loads all projects with frontmatter metadata
- Provides filtering by tags, dates, resources, and categories
- Exports project data for analysis
- Foundation for all other analysis tools

### 2. `strategic_query.py` - Natural Language Queries
**Purpose:** Answer strategic planning questions using natural language

**Example Queries:**
```bash
python strategic_query.py "What work requires communications team in Q4 2025?"
python strategic_query.py "Show dependencies between brand and website projects" 
python strategic_query.py "Identify resource conflicts in upcoming quarters"
python strategic_query.py "High priority projects in brand category"
python strategic_query.py "Rebrand initiative timeline"
```

**Query Types Supported:**
- Resource workload analysis
- Timeline and scheduling queries
- Project dependencies
- Resource conflicts
- Priority-based filtering
- Strategic initiative tracking

### 3. `resource_conflict_analyzer.py` - Capacity Planning
**Purpose:** Identify resource conflicts, capacity issues, and workload distribution

**Usage:**
```bash
# Analyze all quarters
python resource_conflict_analyzer.py

# Focus on specific quarter
python resource_conflict_analyzer.py --quarter Q3-2025

# Custom output file
python resource_conflict_analyzer.py --output capacity_report.md
```

**Analysis Includes:**
- Resource workload distribution
- Concurrent project conflicts
- Capacity warnings and recommendations
- External vendor coordination needs
- Leadership involvement analysis

### 4. `dependency_analyzer.py` - Project Dependencies
**Purpose:** Analyze project dependencies, critical paths, and bottlenecks

**Usage:**
```bash
# Full dependency analysis
python dependency_analyzer.py

# Focus on brand-website dependencies
python dependency_analyzer.py --focus brand-website

# Critical path analysis
python dependency_analyzer.py --focus critical-path

# Bottleneck identification
python dependency_analyzer.py --focus bottlenecks
```

**Analysis Includes:**
- Critical path identification
- Project bottlenecks
- Brand-Website coordination opportunities
- Dependency risk analysis
- Sequential vs. parallel execution opportunities

### 5. `dashboard_generator.py` - Strategic Dashboards
**Purpose:** Generate comprehensive strategic planning dashboards

**Usage:**
```bash
# Generate all dashboards
python dashboard_generator.py --type all

# Executive dashboard only
python dashboard_generator.py --type executive

# Operational dashboard
python dashboard_generator.py --type operational

# Project status dashboard
python dashboard_generator.py --type status
```

**Dashboard Types:**
- **Executive Dashboard:** Strategic overview for leadership
- **Operational Dashboard:** Resource management and coordination
- **Project Status Dashboard:** Progress tracking and milestones

### 6. `run_examples.py` - Demonstration Script
**Purpose:** Run example queries and demonstrate system capabilities

**Usage:**
```bash
# Run all examples
python run_examples.py

# Just show CLI examples
python run_examples.py --demo cli

# Just run queries
python run_examples.py --demo queries
```

## 🚀 Quick Start Guide

### 1. First-Time Setup
```bash
# Ensure you have Python environment activated
source venv/bin/activate

# Install required dependencies (already done in setup)
pip install pyyaml

# Test the system
python scripts/run_examples.py
```

### 2. Common Usage Patterns

**Weekly Leadership Review:**
```bash
python scripts/dashboard_generator.py --type executive
```

**Resource Planning:**
```bash
python scripts/resource_conflict_analyzer.py --quarter Q3-2025
python scripts/strategic_query.py "communications team workload"
```

**Project Coordination:**
```bash
python scripts/dependency_analyzer.py --focus brand-website
python scripts/strategic_query.py "show dependencies between brand and website"
```

**Strategic Planning:**
```bash
python scripts/strategic_query.py "rebrand initiative progress"
python scripts/strategic_query.py "high priority projects timeline"
```

## 📊 Output Files

All reports are saved to `output/reports/` with these naming patterns:

### Default Output Files:
- `resource_conflict_analysis.md` - Resource capacity analysis
- `dependency_analysis.md` - Project dependency mapping
- `executive_dashboard.md` - Strategic overview dashboard
- `operational_dashboard.md` - Resource management dashboard
- `project_status_dashboard.md` - Progress tracking dashboard

### Query-Specific Files:
- Query results are saved with custom names when `--output` is specified
- Dashboard index created at `dashboard_index.md`

## 🎯 Example Queries & Answers

### Resource Questions:
```bash
Q: "What work requires communications team in Q3 2025?"
A: Shows all projects assigned to communications team during Q3, with priority breakdown

Q: "External vendor projects"
A: Lists all projects requiring external vendors, grouped by category and timeline
```

### Dependency Questions:
```bash
Q: "Show dependencies between brand and website projects"  
A: Maps brand→website dependencies, parallel opportunities, and coordination risks

Q: "What depends on brand strategy completion?"
A: Shows all projects blocked by brand strategy work
```

### Timeline Questions:
```bash
Q: "Projects starting in July 2025"
A: Timeline view of July project starts with resource allocation

Q: "High priority projects timeline"
A: Critical project schedule with milestone tracking
```

### Strategic Questions:
```bash
Q: "Rebrand initiative progress"
A: Complete rebrand project status, timeline, and resource analysis

Q: "Resource conflicts in Q3 2025"
A: Detailed conflict analysis with resolution recommendations
```

## 🔧 Advanced Usage

### Custom Queries in Python:
```python
from frontmatter_parser import FrontmatterParser
from strategic_query import StrategicQueryEngine

parser = FrontmatterParser()
query_engine = StrategicQueryEngine(parser)

# Custom analysis
results = query_engine.query("your custom question")
print(results['summary'])
```

### Batch Analysis:
```python
from dashboard_generator import DashboardGenerator

dashboard_gen = DashboardGenerator(parser)
dashboards = dashboard_gen.generate_all_dashboards()
```

### Integration with Other Tools:
- Export project data as JSON for external tools
- Generate reports in Markdown for easy sharing
- Pipe results to other analysis scripts

## 🎛️ Configuration Options

### Query Behavior:
- Modify query patterns in `strategic_query.py`
- Adjust analysis thresholds in analyzer scripts
- Customize output formats in dashboard generator

### Report Formatting:
- Templates can be modified in each script's `_build_*` methods
- Output formats support Markdown with embedded data
- Custom styling through CSS (for HTML conversion)

## ❓ Troubleshooting

### Common Issues:

**"No projects found"**
- Verify frontmatter exists in markdown files
- Check that files are in the `data/` directory
- Ensure YAML syntax is valid

**"Module not found" errors**
- Activate Python virtual environment: `source venv/bin/activate`
- Ensure all scripts are in the same directory
- Check Python path includes scripts directory

**Empty query results**
- Verify query syntax matches expected patterns
- Check that project tags match query terms
- Use broader search terms or try example queries

### Getting Help:
1. Run `python scripts/run_examples.py` to test system functionality
2. Check example queries in this README
3. Verify frontmatter data with `python scripts/frontmatter_parser.py`

## 🔮 Future Enhancements

Planned improvements:
- Web-based query interface
- Automated report scheduling
- Integration with project management tools
- Real-time dashboard updates
- Email notifications for critical issues

---

*These scripts transform your strategic planning documents into a powerful, queryable project management system.*