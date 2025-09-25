# CLAUDE.md - Door County Land Trust Strategic System

## 🏢 **Project Overview**

**Organization**: Door County Land Trust (DCLT)  
**System Purpose**: Strategic project management and communications planning system  
**Primary Use**: Strategic project planning, competitive research, and knowledge organization workflows

## 🎯 **System Capabilities**

### **Visualization Pipeline (paused)**
- Legacy Gantt/visual timeline scripts removed for a future rebuild
- Repository content remains structured to support the next iteration
- No live deployment or watcher processes at the moment

### **Data & Knowledge Management**
- Strategic markdown files organized with consistent frontmatter
- Competitive intelligence datasets under `data/landtrusts/`
- Reminder inbox (`data/dclt/reminders.json`) for lightweight task capture
- Embedding index + Q&A assistant powered by OpenAI APIs

## 🚀 **Quick Commands**

### **Reminder Inbox**
```bash
python3 scripts/add_reminder.py --text "Follow up with design team" --due 2025-10-15 --project "Website Overhaul" --open-md
python3 scripts/list_reminders.py
```
Capture new reminders and review the queue.

### **Knowledge Index Refresh**
```bash
python3 scripts/indexing/index_repo.py
python3 scripts/ask.py "What are the next milestones for the website overhaul?"
```
Regenerate embeddings for execution docs and query them.

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
│   ├── dashboards/                     # Dashboard utilities (under rebuild)
│   ├── indexing/                       # Embedding + search tooling
│   ├── query/                          # CLI helpers for indexed data
│   ├── scrapers/                       # Competitive intelligence scrapers
│   ├── utils/                          # Shared helpers (currently empty)
│   └── *.py                            # Standalone helpers (e.g., reminders)
├── output/reports/                     # Generated analysis & exports
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
