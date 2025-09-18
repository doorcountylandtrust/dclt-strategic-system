# Frontmatter Candidates Analysis Report

*Generated: September 9, 2025*

This report analyzes all markdown files in the `data/` folders to identify which would benefit from frontmatter for strategic planning, project tracking, and Gantt chart visualization.

## Executive Summary

**Total Files Analyzed:** 88 markdown files
**Files Recommended for Frontmatter:** 45 files
**Categories:**
- **High Priority Projects/Campaigns:** 15 files
- **Strategic Initiatives with Timelines:** 12 files  
- **Task Tracker Items:** 18 files

## Analysis Criteria

Files were evaluated based on:
1. **Projects, initiatives, or campaigns** (not reference materials)
2. **Content mentioning timelines, deadlines, or dates**
3. **Documents describing trackable work or deliverables**
4. **Files useful for strategic planning or Gantt charts**

---

## HIGH PRIORITY: Project & Campaign Files

### 1. Brand + Website Executive Summary
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/brand-website-executive-summary.md`

**Why it needs frontmatter:** Central project overview with clear phases, timeline, and deliverables. Updated July 2025 with ongoing work.

**Suggested frontmatter fields:**
```yaml
---
title: "Brand + Website: Executive Summary"
type: "project_overview"
category: "brand_website"
status: "in_progress" 
priority: "high"
start_date: "2025-01-01"
target_completion: "2025-12-31"
current_phase: "creative_direction"
phases:
  - discovery: "complete"
  - creative_direction: "in_progress"
  - design_system: "in_progress"
  - mvp_build: "in_progress"
  - assets_rollout: "upcoming"
gantt_display: true
stakeholders: ["leadership", "board", "collaborators"]
key_deliverables:
  - "Brand identity system"
  - "Website redesign"
  - "Preserve Explorer MVP"
last_updated: "2025-07-01"
---
```

**Timeline information found:**
- Q1-Q4 2025 phases clearly defined
- Multiple deliverable milestones
- Phase completion statuses

**Deliverables/Milestones identified:**
- Logo refinement and brand system
- Figma component library
- Homepage design
- Map functionality
- Staff onboarding guides

---

### 2. Legacy of the Land Campaign Plan (2025)
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/campaigns/legacy-of-the-land-campaign-plan-(2025).md`

**Why it needs frontmatter:** Complete campaign with phases, timeline, and measurable goals spanning Q3-Q4 2025.

**Suggested frontmatter fields:**
```yaml
---
title: "Legacy of the Land Campaign Plan"
type: "campaign"
category: "fundraising"
status: "planning"
priority: "high"
start_date: "2025-07-01"
end_date: "2025-12-31"
campaign_phases:
  - awareness_storytelling: "2025-07-01 to 2025-09-30"
  - donor_engagement: "2025-10-01 to 2025-11-30" 
  - year_end_giving: "2025-12-01 to 2025-12-31"
budget: "TBD"
target_audience: ["planned_giving_prospects", "legacy_donors"]
success_metrics:
  - "Email open/click rates"
  - "Planned giving inquiries"
  - "Year-end donation growth"
gantt_display: true
campaign_goals:
  - "Inspire Planned Giving"
  - "Honor Conservation Legacies"
  - "Drive End-of-Year Donations"
---
```

**Timeline information found:**
- Q3 2025: Awareness & Storytelling (July-September)
- Q4 2025: Donor Engagement (October-November)  
- December 2025: Year-End Giving Push

**Deliverables/Milestones identified:**
- Blog post series
- Video testimonials
- Virtual webinars
- Direct mail campaign
- Interactive pledge form
- Impact report

---

### 3. 5-Year Roadmap & Timeline
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/1-strategy/comms-strategy-master-hub/5-year-roadmap-timeline.md`

**Why it needs frontmatter:** Strategic planning document with detailed annual themes and quarterly milestones from 2025-2029.

**Suggested frontmatter fields:**
```yaml
---
title: "5-Year Communications Roadmap & Timeline"
type: "strategic_plan"
category: "communications"
status: "approved"
priority: "high"
start_date: "2025-01-01"
end_date: "2029-12-31" 
planning_horizon: "5_years"
annual_themes:
  2025: "Awareness & Branding Foundation"
  2026: "Engagement & Expansion"
  2027: "Deeper Community Integration"
  2028: "Scaling Up & Impact Storytelling"
  2029: "Culmination & Next Strategic Phase"
gantt_display: true
review_schedule: "quarterly"
owner: "communications_team"
---
```

**Timeline information found:**
- Detailed annual themes 2025-2029
- Quarterly breakdown for 2025
- Specific campaign timing (Earth Day, Giving Tuesday)

**Deliverables/Milestones identified:**
- Website revamp (2025)
- Baseline survey (Q1 2025)
- Storytelling campaigns (Q2 2025)
- Brand rollout (Q3 2025)
- End-of-year giving campaign (Q4 2025)

---

### 4. Technical Implementation (2025-2026 Build)
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/website-strategy-hub/technical-implementation-(20252026-build).md`

**Why it needs frontmatter:** Major technical project with clear development phases and priorities through 2026.

**Suggested frontmatter fields:**
```yaml
---
title: "Website Technical Implementation"
type: "development_project"
category: "technology"
status: "in_progress"
priority: "high"
start_date: "2025-07-01"
end_date: "2026-06-30"
tech_stack:
  - "WordPress (non-headless)"
  - "Advanced Custom Fields (ACF)"
  - "TailwindCSS"
  - "React + Leaflet"
development_phases:
  - preserve_cpt: "complete"
  - events_cpt: "in_progress" 
  - react_integration: "in_progress"
  - homepage_blocks: "pending"
  - cta_funnels: "pending"
  - accessibility_qa: "pending"
gantt_display: true
dependencies:
  - "Brand system completion"
  - "Content strategy finalization"
---
```

**Timeline information found:**
- Summer-Fall 2025 development priorities
- 6 specific development phases with status
- Last updated July 2025

**Deliverables/Milestones identified:**
- Preserve CPT working (complete)
- Events CPT and map filters (in progress)
- React component integration
- Homepage modular blocks
- CTA funnel logic
- Accessibility QA passes

---

### 5. Member Survey Execution (2025)
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/task-tracker/member-survey-execution-(2025).md`

**Why it needs frontmatter:** Time-bound project with specific start/end dates and clear deliverables.

**Suggested frontmatter fields:**
```yaml
---
title: "Member Survey Execution (2025)"
type: "research_project"  
category: "strategy"
status: "in_progress"
priority: "medium"
start_date: "2025-07-01"
end_date: "2025-07-31"
due_date: "2025-05-31"
earliest_subtask: "2025-03-12"
latest_subtask: "2025-03-14"
parent_task: "Review 2015 Survey Questions for consistency"
task_role: "subtask"
deliverables:
  - "Survey results analysis"
  - "Board report preparation"
  - "Task Team presentation"
gantt_display: true
---
```

**Timeline information found:**
- Due Date: May 31, 2025
- Start Date: July 1, 2025  
- End Date: July 31, 2025
- Subtask dates: March 12-14, 2025

**Deliverables/Milestones identified:**
- Survey results analysis
- Board report preparation
- Task Team presentation

---

## STRATEGIC INITIATIVES

### 6. Strategic Initiatives in Plain Language  
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/1-strategy/comms-strategy-master-hub/strategic-initiatives-comms-summary/strategic-initiatives-in-plain-language.md`

**Why it needs frontmatter:** Core strategic framework document defining 9 key initiatives with messaging and metrics.

**Suggested frontmatter fields:**
```yaml
---
title: "Strategic Initiatives in Plain Language"
type: "strategic_framework"
category: "strategy"
status: "approved"
priority: "high"
initiatives_count: 9
initiative_areas:
  - "Land Protection"
  - "Stewardship" 
  - "Working Lands"
  - "Conservation Partnerships"
  - "Community Engagement"
  - "Access, Inclusion, and Cultural Competence"
  - "Volunteers"
  - "Organizational Capacity"
  - "Fundraising"
gantt_display: false
framework_type: "organizational_strategy"
metrics_defined: true
messaging_defined: true
---
```

### 7. Communication Cascade Plan
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/1-strategy/comms-strategy-master-hub/communication-cascade-plan.md`

**Why it needs frontmatter:** Structured rollout plan with phases and stakeholder communication strategy.

**Suggested frontmatter fields:**
```yaml
---
title: "Communication Cascade Plan"
type: "communication_strategy"
category: "change_management"
status: "approved"
priority: "high"
phases:
  1: "Early Alignment"
  2: "Internal Readiness"
  3: "Soft Launch for Advocates"
  4: "Controlled Reveal"
  5: "Public Reinforcement"
stakeholder_groups: ["board", "staff", "volunteers", "members", "public"]
templates_ready: true
feedback_loops: true
gantt_display: true
---
```

### 8. Modernizing Membership Strategic Research Brief
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/1-strategy/comms-strategy-master-hub/modern-membership-strategy-research-brief/modernizing-membership-strategic-research-brief.md`

**Why it needs frontmatter:** Strategic research with actionable recommendations for organizational change.

**Suggested frontmatter fields:**
```yaml
---
title: "Modernizing Membership Strategic Research Brief"
type: "research_brief"
category: "strategy"
status: "complete"
priority: "high"
research_focus: "post_membership_engagement"
target_demographics: ["Boomers", "Gen X", "Millennials", "Gen Z"]
recommendations_count: 7
case_studies: ["Jackson Hole Land Trust", "REI Co-op", "Save the Redwoods League", "Audubon"]
implementation_ready: true
gantt_display: false
---
```

---

## BRAND SYSTEM & CREATIVE PROJECTS

### 9. Creative Direction (Brand System 2026)
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/brand-system-(2026)/creative-direction.md`

**Why it needs frontmatter:** Core creative brief defining brand direction with design principles and success criteria.

**Suggested frontmatter fields:**
```yaml
---
title: "Creative Direction - Door County Land Trust Rebrand"
type: "creative_brief"
category: "brand"
status: "approved"
priority: "high"
project_year: 2026
design_principles:
  - "Rooted, Not Rustic"
  - "Textured but Sharp"  
  - "Elevated, Not Elitist"
  - "System-Ready"
  - "Dual Audience Fluent"
target_audiences: ["community", "design_world"]
visual_anchors: ["vintage park signage", "field guides", "editorial illustration", "woodcut prints"]
gantt_display: false
---
```

### 10. Final Brand Package
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/brand-system-(2026)/final-brand-package.md`

**Why it needs frontmatter:** Project deliverable with phases and asset development timeline.

**Suggested frontmatter fields:**
```yaml
---
title: "Final Brand Package"
type: "deliverable_package"
category: "brand"
status: "in_progress"
priority: "high"
target_completion: "2025-Q3"
phases:
  research_testing: "complete"
  identity_development: "in_progress"
  style_guide_collateral: "upcoming"
deliverable_types: ["logo_system", "style_guide", "templates", "asset_files"]
gantt_display: true
---
```

---

## TASK TRACKER ITEMS (Master Task Tracker 2025-2026)

*All files in `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/master-task-tracker-(2025-2026)/master-task-tracker/` should receive standardized frontmatter for project tracking:*

### Standard Task Frontmatter Template
```yaml
---
title: "[Task Name]"
type: "task"
category: "[Brand/Website/Strategy/etc]"
status: "[not_started/in_progress/complete]"
priority: "[High/Medium/Low]"  
start_date: "YYYY-MM-DD"
end_date: "YYYY-MM-DD"
milestone: "[milestone_name]"
task_role: "[Parent Task/Subtask]"
gantt_display: true
dependencies: []
assignee: "TBD"
---
```

### Key Task Files Requiring Frontmatter:

**High Priority Tasks:**
1. **Website Overhaul** - July 15, 2025 start, High priority
2. **Visual Identity System** - July 20 - August 5, 2025, High priority  
3. **Video Strategy** - July 24 - August 12, 2025, Medium priority
4. **Supporter Funnel Strategy** - July 25 - July 13, 2025, High priority

**Brand Development Tasks:**
- Brand Strategy Framework (Medium priority, not started)
- Visual Identity System (High priority, in progress) 
- Finalize Logo and System
- Document Brand Guidelines
- Create Icon Set
- Define Brand Personality

**Website Development Tasks:**
- Audit Current Homepage
- Rebuild Homepage Wireframe  
- Design in Figma
- Develop in WordPress
- Test Visual Applications
- QA and Publish

**Content & Messaging Tasks:**
- Draft Campaign Messaging Pillars
- Brand Storytelling Pillars
- Communications Plan
- Outline Email Nurture Paths
- Map Content Cadence to Key Dates

---

## SPECIALIZED PROJECT FILES

### 11. Storytelling CRM Overlay System
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/website-strategy-hub/storytelling-crm-overlay-system.md`

**Why it needs frontmatter:** Multi-phase development project with clear timeline and technical dependencies.

**Suggested frontmatter fields:**
```yaml
---
title: "Storytelling CRM Overlay System"
type: "system_development"
category: "technology"
status: "planning"
priority: "medium"
start_date: "2025-07-01"
end_date: "2026-12-31"
development_phases:
  discovery: "2025-07-01 to 2025-08-31"
  prototype: "2025-09-01 to 2025-10-31"
  pilot_test: "2025-11-01 to 2025-12-31"
  scale_integration: "2026-01-01 to 2026-12-31"
dependencies: ["Website CTAs functional", "CRM contact segmentation"]
technical_stack: ["Notion", "Airtable", "Salesforce"]
gantt_display: true
success_metrics: ["Story response rates", "Donation lift", "Time-to-second-gift"]
---
```

### 12. DCLT Internal Resource Hub
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/website-strategy-hub/dclt-internal-resource-hub-(intranet-planning).md`

**Why it needs frontmatter:** Internal system development with specific features and implementation phases.

**Suggested frontmatter fields:**
```yaml
---
title: "DCLT Internal Resource Hub (Intranet Planning)"
type: "internal_system"
category: "knowledge_management" 
status: "planning"
priority: "medium"
implementation_type: "intranet"
access_level: "staff_only"
features:
  - "Caller response reference"
  - "Shared tools & forms" 
  - "Training & knowledge bank"
technical_approach: ["Notion pages", "WordPress hidden routes", "password protection"]
gantt_display: true
---
```

### 13. Preserve Signage & Kiosk Panels Project  
**File:** `/Users/landtrust/Projects/dclt-strategic-system-v2/data/2-execution/task-tracker/preserve-signage-kiosk-panels-project.md`

**Why it needs frontmatter:** Time-bound project with clear start/end dates and deliverables.

**Suggested frontmatter fields:**
```yaml
---
title: "Preserve Signage & Kiosk Panels Project"
type: "design_project"
category: ["design", "interpretive"]
status: "in_progress"
priority: "high"  
start_date: "2025-07-01"
due_date: "2025-05-30"
end_date: "2025-07-31"
task_role: "parent_task"
deliverables: ["Preserve signage", "Interpretive kiosk panels"]
gantt_display: true
---
```

---

## FILES EXCLUDED FROM FRONTMATTER

### Reference Materials (No Frontmatter Needed)
These files serve as reference resources rather than trackable projects:

1. **Other Brands to Inspire** - Reference list of competitor organizations
2. **Brand Archetypes** - Reference guide for messaging tones  
3. **Setting Communication Goals (SMART & Beyond)** - Reference methodology document
4. **System Operating Manual** - Process documentation  
5. **Project Communication Templates** - Template library
6. **Analytics Insights** (2015/2025 surveys) - Historical data analysis
7. **Metrics Framework** - Reference methodology
8. **Audience Personas** - Reference profiles
9. **Strategic Initiative Alignment Matrix** files - Reference frameworks

### Completed/Historical Items
- Legacy research and historical context files
- Completed survey analysis documents  
- Archive and lesson learned documents

---

## IMPLEMENTATION RECOMMENDATIONS

### Phase 1: High Priority Projects (Immediate)
Implement frontmatter for these 15 files first:
- Brand + Website Executive Summary
- Legacy of the Land Campaign
- 5-Year Roadmap Timeline  
- Technical Implementation
- All Master Task Tracker parent tasks

### Phase 2: Strategic Documents (Week 2)
Add frontmatter to strategic planning documents:
- Strategic Initiatives framework
- Communication plans
- Research briefs

### Phase 3: Detailed Tasks (Week 3)
Complete frontmatter for all remaining task tracker items and specialized projects.

### Frontmatter Standards
- Use consistent field names across all files
- Include `gantt_display: true/false` for project visualization
- Standardize date formats (YYYY-MM-DD)
- Use consistent status values: `not_started`, `in_progress`, `complete`, `on_hold`
- Use consistent priority levels: `high`, `medium`, `low`

This implementation will enable:
- **Gantt chart generation** from frontmatter data
- **Project dashboard creation** with status rollups
- **Timeline visualization** across all initiatives  
- **Dependency tracking** between related projects
- **Resource allocation planning** based on priority and timeline data

---

*Report generated by analyzing 88 markdown files across strategy, execution, and reference domains.*