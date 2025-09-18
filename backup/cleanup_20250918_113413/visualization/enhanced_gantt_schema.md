# Enhanced Project Management Frontmatter Schema
*Design for Professional Gantt Chart Generation*

## Core Project Fields

### Basic Information
```yaml
---
title: "Website Redesign Project"
project_type: "execution"          # strategy, execution, research, maintenance
project_status: "in_progress"      # planned, in_progress, completed, on_hold, cancelled
priority: "high"                   # critical, high, medium, low
---
```

### Timeline Management
```yaml
---
# Project Timeline
start_date: "2025-07-15"
end_date: "2025-08-14" 
duration_days: 30                  # Auto-calculated or manual override
baseline_start: "2025-07-10"       # Original planned start (for variance tracking)
baseline_end: "2025-08-10"         # Original planned end (for variance tracking)

# Progress Tracking
progress_percent: 65               # 0-100 completion percentage
actual_start: "2025-07-18"        # When work actually began
estimated_completion: "2025-08-20" # Current completion estimate
---
```

### Project Hierarchy
```yaml
---
# Parent/Child Structure
parent_project: "Brand System (2026)"     # Links to parent project
project_phase: "Phase 2: Implementation"  # Which phase this belongs to
work_breakdown_level: 2                   # 1=Project, 2=Phase, 3=Task, 4=Subtask

# Dependencies
depends_on: 
  - "Brand Strategy Framework"             # Must complete before this starts
  - "User Research Analysis"
blocks:
  - "Content Migration"                    # This must complete before these start
  - "QA Testing Phase"

# Milestone Flags
is_milestone: false                        # true for milestone markers
milestone_type: "deliverable"              # gate, deliverable, review, approval
---
```

### Resource Management
```yaml
---
# Team & Resources
assigned_to:
  - "Don Peterson"          # Primary owner
  - "Design Team"           # Supporting resources
  - "External Contractor"   # External resources

estimated_hours: 240        # Total estimated effort
actual_hours: 180          # Hours spent so far
resource_type: "design"    # design, development, strategy, content, research

# Budget Tracking
budget_allocated: 15000
budget_spent: 9500
cost_center: "Marketing"
---
```

### Risk and Quality Management
```yaml
---
# Risk Factors
risk_level: "medium"       # low, medium, high, critical
risk_factors:
  - "Dependency on external vendor"
  - "Tight deadline constraints"
  
# Quality Gates
quality_gates:
  - name: "Design Review"
    date: "2025-07-25"
    status: "passed"       # pending, passed, failed
  - name: "Stakeholder Approval"
    date: "2025-08-05"
    status: "pending"

# Success Criteria
success_metrics:
  - "User satisfaction > 8/10"
  - "Performance improvement > 30%"
  - "On-time delivery within 5 days"
---
```

### Communication and Stakeholders
```yaml
---
# Stakeholder Management
stakeholders:
  - name: "Executive Team"
    role: "Sponsor"
    involvement: "high"
  - name: "Marketing Department"
    role: "End User"
    involvement: "medium"

# Communication Plan
reporting_frequency: "weekly"    # daily, weekly, biweekly, monthly
next_review_date: "2025-07-22"
status_dashboard_url: "https://project-tracker.dclt.org/website-redesign"

# Strategic Alignment
strategic_theme: "Digital Transformation"
kpi_impact:
  - "Website Engagement: +25%"
  - "Conversion Rate: +15%"
  - "Brand Consistency Score: 95%"
---
```

## Advanced Project Types

### Epic/Program Level
```yaml
---
project_type: "epic"
epic_theme: "Brand System Modernization"
epic_objectives:
  - "Establish consistent brand identity"
  - "Improve digital presence"
  - "Enhance stakeholder experience"

child_projects:
  - "Logo Design"
  - "Website Redesign" 
  - "Marketing Materials Update"
  - "Staff Training Program"
---
```

### Sprint/Agile Planning
```yaml
---
project_type: "sprint"
sprint_number: 3
sprint_goal: "Complete homepage wireframe and user testing"
sprint_capacity: 80                # Team capacity in hours
velocity_target: 25               # Story points or tasks
retrospective_date: "2025-07-28"

user_stories:
  - id: "US-101"
    title: "As a visitor, I want clear navigation"
    points: 5
    status: "completed"
  - id: "US-102" 
    title: "As a donor, I want easy giving process"
    points: 8
    status: "in_progress"
---
```

### Research/Discovery Projects
```yaml
---
project_type: "research"
research_method: "user_interviews"    # surveys, interviews, analytics, literature_review
sample_size: 15
research_questions:
  - "What motivates donors to give?"
  - "How do users discover our preserves?"
  
deliverables:
  - "Research findings report"
  - "User persona updates"
  - "Recommendation presentation"

validation_criteria:
  - "Statistical significance > 95%"
  - "Stakeholder buy-in achieved"
---
```

## Schema Benefits for Gantt Visualization

### Automatic Visualizations
- **Hierarchical Structure**: Parent/child relationships create proper project breakdown
- **Dependency Lines**: `depends_on` and `blocks` fields generate dependency arrows
- **Milestone Markers**: `is_milestone: true` creates diamond milestone markers
- **Progress Bars**: `progress_percent` shows completion within task bars
- **Critical Path**: Risk level and dependencies enable critical path calculation

### Color Coding System
- **Status Colors**: Green (completed), Yellow (in_progress), Blue (planned), Red (overdue)
- **Priority Colors**: Critical (dark red), High (orange), Medium (blue), Low (gray)
- **Resource Colors**: Different colors per team/resource type
- **Risk Indicators**: Border colors or icons for high-risk items

### Interactive Features
- **Hover Details**: Full project metadata in tooltips
- **Drill-Down**: Click to expand project phases and subtasks
- **Filtering**: By status, priority, resource, date range
- **Timeline Zoom**: Month, week, day views with appropriate detail levels

## Implementation Notes

### Validation Rules
1. **Date Consistency**: `start_date` < `end_date`, actual vs. planned variance tracking
2. **Dependency Logic**: Circular dependency detection and warnings
3. **Resource Allocation**: Overallocation warnings when resources exceed capacity
4. **Milestone Alignment**: Milestones align with project phases and dependencies

### Data Quality Enhancements
1. **Auto-Calculation**: Duration, variance, critical path, resource utilization
2. **Status Inference**: Auto-update status based on dates and progress
3. **Template Generation**: Schema templates for different project types
4. **Validation Reports**: Data quality issues and recommendations

This enhanced schema enables professional-grade project management visualization while maintaining the automated, markdown-based approach.