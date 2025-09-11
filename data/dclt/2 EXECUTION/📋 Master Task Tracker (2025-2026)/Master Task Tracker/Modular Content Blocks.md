---
title: "\u2014\u2014 Modular Content Blocks"
project_status: planned
priority: medium
stakeholders:
- Modular Content
- Define reusable
- content components
- that will
- appear across
tags:
- website
- strategy
- fundraising
- conservation
created_date: '2025-09-11'
last_updated: '2025-09-11'
---
# —— Modular Content Blocks

## Purpose

Define reusable content components that will appear across multiple pages on the new DCLT website. These blocks are the building units of page templates, campaigns, and story-driven layouts.

---

## 🔄 Block Inventory

| Block Name | Description | Appears On | Source Content Type | Notes |
| --- | --- | --- | --- | --- |
| Hero (Image + Headline + CTA) | Full-width hero section with overlay text | Homepage, Campaign Page | Campaign, Story, CTA | Often dynamic or configurable |
| Featured Story Block | Pulls a single story w/ image, excerpt, CTA | Homepage, Sidebar, Preserve pages | Story | Could be filtered by category or tag |
| CTA Panel (Join, Give, Volunteer) | Modular call-to-action block w/ icon and button | Global (sidebar, footer, inline) | Supporter CTA | May be context-aware |
| Preserve Card Grid | Tiled visual layout with short preserve data | Explore page, Homepage | Preserve | Needs filtering logic |
| Program / Events Block | Upcoming events in list or card format | Homepage, Explore pages | Event / Program | Optional RSVP button |
| Testimonial Quote Block | Highlighted quote, name, role | Campaign, Homepage, Donate | Story | Could tie to donor or volunteer persona |
| Statistic / Impact Panel | Number + description + icon (e.g., 8,000 acres protected) | Homepage, About, Campaign | Annual Report, Project | Reusable in multiple places |
| Map Embed Block | Interactive map or location graphic | Explore, Preserve detail | Conservation Map Tool | Could filter dynamically |
| Related Content Block | Cross-links to related content | Preserve, Story, Project | All | Logic: tag or related field |
| Accordion / FAQ Block | Expandable Q&A section | Visitor Info, About, Strategic Plan                               | All | Use for quick clarity sections |

---

## 🧭 Page Template Mapping (Example: Homepage)

1. Hero Block
2. Featured Story
3. Preserve Grid (Top 3–6)
4. CTA Panel (Give/Join)
5. Events Block (Upcoming)
6. Impact Stats
7. Testimonial
8. Footer with newsletter signup

---

## 🛠️ Implementation Notes

- Blocks should be **modular in WordPress**, either via:
    - ACF Flexible Content
    - ACF Block-based editor
    - Or separate CPTs fetched dynamically
- Match each block with a **GraphQL fragment** in Astro for clean querying and rendering

[  ——— Master Modular Block Field Definitions](%E2%80%94%E2%80%94%20Modular%20Content%20Blocks%201f12a8cd57558061a6c9d9314be3cd49/%E2%80%94%E2%80%94%E2%80%94%20Master%20Modular%20Block%20Field%20Definitions%201f12a8cd575580708d65d0deb83f009f.csv)

## Related Documents

**Cross-Referenced Documents**
- [[Website Strategy Hub]]
- [[Campaigns]]
- [[— Website Content Strategy and Migration Plan]]


- [[Comms Strategy Master Hub]]
- [[2026 Budgeting]]
- [[Mission, Values & Brand Voice]]

**Thematic Alignment**
- [[Project Communication Templates]] - strategy, website, fu
- [[Messaging & Engagement Research]] - co
- [[Brand + Website: Executive Summary]] - co