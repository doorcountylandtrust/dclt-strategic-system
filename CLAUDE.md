# CLAUDE.md - Door County Land Trust Strategic System

## 🏢 **Project Overview**

**Organization**: Door County Land Trust (DCLT)  
**System Purpose**: Strategic project management and communications planning system  
**Primary Use**: Visual project timelines, brand system management, and strategic planning workflows

## 🎯 **System Capabilities**

### **Live Gantt Chart System**
- **Professional project management** with DHTMLX Gantt charts
- **FigJam-style visual timelines** with swim lanes and strategic grouping
- **Automatic file watching** - charts update when markdown files change
- **Real-time deployment** at http://localhost:8081/

### **Data Management**
- **350+ project files** organized in strategic hierarchy
- **Clean, standardized data** with professional frontmatter
- **Automated quality control** and data validation
- **Hierarchical project structure** (Epic → Project → Task → Subtask)

## 🚀 **Quick Commands**

### **Start the Live System**
```bash
./start_live_gantt.sh
```
Launches web server + file watcher for automatic chart updates

### **Manual Chart Generation**
```bash
# Advanced Gantt Chart
python3 scripts/visualization/advanced_gantt_generator.py

# FigJam-Style Timeline
python3 scripts/visualization/figjam_style_generator.py

# Both charts
python3 scripts/automation/simple_file_watcher.py
```

### **Data Quality Management**
```bash
# Audit data quality
python3 scripts/data_cleanup/project_data_auditor.py

# Run automated cleanup
python3 scripts/data_cleanup/automated_cleanup.py

# Analyze brand project hierarchy
python3 scripts/data_organization/rebrand_hierarchy_analyzer.py

# Fix brand project relationships
python3 scripts/data_organization/rebrand_hierarchy_fixer.py
```

## 📁 **File Structure**

```
dclt-strategic-system-v2/
├── data/dclt/                          # Strategic project files
│   ├── 1 STRATEGY/                     # Strategic planning documents
│   ├── 2 EXECUTION/                    # Implementation projects
│   └── 3 REFERENCE & TOOLS/            # Reference materials
├── scripts/
│   ├── visualization/                  # Chart generators
│   ├── data_cleanup/                   # Data quality tools
│   ├── data_organization/              # Hierarchy management
│   └── automation/                     # Live update system
├── deploy/gantt-chart/                 # Web deployment
├── output/reports/                     # Generated charts & analysis
└── backup/                            # Data backups
```

## 🗂️ **Strategic Project Structure**

### **Major Strategic Themes**
- **Brand Excellence**: Brand System (2026) rebrand project
- **Digital Transformation**: Website redesign and modernization
- **Strategic Planning**: Communications strategy and messaging
- **Foundation Building**: Research, analysis, and planning
- **Implementation**: Execution of strategic initiatives

### **Key Projects**
1. **Brand System (2026)** - 9-month epic project (July 2025 - March 2026)
2. **Website Strategy Hub** - Digital presence modernization
3. **Communications Strategy Master Hub** - Strategic messaging framework
4. **Land Seller Experience Study** - Research and analysis project
5. **Master Task Tracker** - Execution planning and tracking

## 📋 **Frontmatter Schema**

### **Epic Level Projects**
```yaml
---
title: "Project Name"
project_type: epic
project_status: in_progress
priority: critical
start_date: '2025-07-01'
end_date: '2026-03-31'
duration_days: 273
progress_percent: 35
epic_theme: "Strategic Theme"
epic_objectives:
  - "Objective 1"
  - "Objective 2"
child_projects:
  - "Child Project 1"
  - "Child Project 2"
assigned_to:
  - "Team/Person"
estimated_hours: 1200
budget_allocated: 75000
risk_level: high
strategic_theme: "Brand Excellence"
tags:
  - brand
  - strategy
created_date: '2025-09-12'
last_updated: '2025-09-12'
---
```

### **Project Level**
```yaml
---
title: "Project Name"
project_type: project
parent_project: "Parent Epic Name"
project_status: in_progress
priority: high
start_date: '2025-07-15'
end_date: '2025-08-15'
duration_days: 31
assigned_to:
  - "Team/Person"
resource_type: creative
strategic_theme: "Brand Excellence"
tags:
  - execution
created_date: '2025-09-12'
last_updated: '2025-09-12'
---
```

### **Task Level**
```yaml
---
title: "Task Name"
project_type: task
parent_project: "Parent Project Name"
project_status: completed
priority: medium
start_date: '2025-07-20'
end_date: '2025-07-27'
duration_days: 7
assigned_to:
  - "Team/Person"
resource_type: operational
strategic_theme: "Brand Excellence"
tags:
  - task
created_date: '2025-09-12'
last_updated: '2025-09-12'
---
```

## 🎨 **Visualization Features**

### **Advanced DHTMLX Gantt Chart**
- **Hierarchical project structure** with expand/collapse
- **Interactive timeline** with drag-and-drop scheduling
- **Progress tracking** with completion percentages
- **Dependency arrows** showing project relationships
- **Professional project management** interface

### **FigJam-Style Timeline**
- **Swim lane organization** by strategic theme
- **Varied visual heights** based on project importance
- **Rich color coding** by project type and priority
- **Milestone markers** and status indicators
- **Hand-crafted aesthetic** with automated data

## 🔄 **Live Update Workflow**

1. **Edit any markdown file** in `data/dclt/`
2. **Save the file** - system detects changes within 3 seconds
3. **Automatic regeneration** begins (10-30 seconds)
4. **Refresh browser** - charts reflect changes immediately
5. **No manual intervention** required

## 📊 **Current System Statistics**

- **Total Projects**: 257 items across all strategic themes
- **Brand System Projects**: 51 hierarchically organized items
- **Timeline Span**: March 2025 - November 2025 (254 days)
- **Active Work**: 175 projects currently in progress
- **Strategic Themes**: 5 major areas with swim lane organization

## 🛠️ **Maintenance Commands**

### **System Health Checks**
```bash
# Check web server status
curl -I http://localhost:8081/

# View file watcher logs
tail -f watcher_test.log

# Check for data quality issues
python3 scripts/data_cleanup/project_data_auditor.py
```

### **Backup and Recovery**
```bash
# Manual backup
cp -r data/ backup/manual_$(date +%Y%m%d_%H%M%S)/

# Restore from backup
cp -r backup/cleanup_20250912_094936/data/ ./

# View cleanup history
cat output/reports/cleanup_report.json
```

## 🎯 **Strategic Context**

### **Brand System (2026) Project**
This is DCLT's major rebranding initiative spanning 9 months with:
- **8 major components** (Creative Direction, Logo Design, Focus Groups, etc.)
- **$75,000 budget** with professional brand consultant
- **Strategic alignment** with organizational modernization goals
- **Risk management** for large-scope organizational change

### **Communications Strategy**
Comprehensive approach to stakeholder engagement including:
- **Audience segmentation** and persona development
- **Messaging frameworks** with values-driven approach
- **Digital transformation** with website modernization
- **Membership strategy** evolution into movement building

## 📈 **Success Metrics**

### **Project Management Excellence**
- **Real-time visibility** into all strategic initiatives
- **Professional timeline management** with dependency tracking
- **Resource allocation** optimization across projects
- **Risk identification** and mitigation planning

### **Data Quality Achievement**
- **Improved from 0/100 to clean data** through automated cleanup
- **51 hierarchical fixes** applied to brand projects
- **Standardized frontmatter** across 350+ project files
- **Automated quality control** preventing future degradation

## 🌐 **Access Points**

- **Advanced Gantt Chart**: http://localhost:8081/
- **FigJam-Style Timeline**: http://localhost:8081/figjam-style.html
- **System Documentation**: `README_LIVE_SYSTEM.md`
- **Project Reports**: `output/reports/`

## 💡 **Best Practices**

### **File Management**
- Always use proper frontmatter with required fields
- Maintain parent-child relationships for hierarchical projects
- Use consistent naming conventions (no em-dashes, special characters)
- Keep project timelines realistic and calendar-based

### **Strategic Planning**
- Align all projects with strategic themes
- Use epic → project → task hierarchy for complex initiatives
- Include resource allocation and risk assessment
- Maintain regular progress updates and status tracking

### **System Maintenance**
- Run data quality audits before major planning sessions
- Use automated cleanup tools to maintain data standards
- Keep backup of data before major organizational changes
- Monitor live system logs for optimal performance

---

**System Status**: ✅ **OPERATIONAL**  
**Last Major Update**: 2025-09-12  
**Data Quality**: Professional Grade  
**Automation**: Fully Live with File Watching