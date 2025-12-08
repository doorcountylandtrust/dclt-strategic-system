---
title: "\U0001F333 Digital Giving Tree (Interactive Donor Wall & Story Map)"
project_status: planned
priority: medium
stakeholders:
- Digital Giving
- Interactive Donor
- Story Map
- This immersive
- digital experience
tags:
- brand
- website
- strategy
- fundraising
created_date: '2025-09-11'
last_updated: '2025-09-11'
---
# 🌳 Digital Giving Tree (Interactive Donor Wall & Story Map)

This immersive digital experience turns supporter stories and gifts into a living, zoomable tree — visualizing collective impact, surfacing segmented stories, and inviting participation.

---

## 🎯 Purpose

- Celebrate donors and storytellers in a public, visual, and emotional way
- Build Giving Tuesday momentum through real-time participation
- Serve as a hybrid story archive + donor wall + gamified membership display
- Extend campaign value beyond December (evergreen asset)

---

## 🖥️ Core Features

| Feature | Description |
| --- | --- |
| Interactive Tree | Zoom/pan interface with growing branches + leaves |
| Leaf = Story or Gift | Hover or click to reveal name, quote, amount, or story |
| Archetype Color Coding | Leaf shapes or colors indicate supporter type or tier |
| Filter & Explore | View by month, type, archetype, location |
| Add Your Leaf | Donation or story form adds a new leaf to the tree |
| Mobile Optimized | Fully responsive layout for all devices |

---

## 🪄 Experience Flow

1. Donor gives (or shares story)
2. Chooses archetype (optional)
3. Gets confirmation: “Your leaf has been added”
4. Can see name/quote on the tree and share it

---

## ⚙️ MVP vs Phase 2

| Version | Features |
| --- | --- |
| **MVP** | Flat or static image map with hover/click-to-reveal stories or names |
| **Intermediate** | Zoomable SVG or canvas with batch-updated leaves via Notion or CMS |
| **Advanced** | Real-time tree, custom interactions, CRM-integrated story sync |

---

## 🧱 Platform Options

- WordPress + JavaScript (SVG or Canvas-based)
- React app embedded via iframe or shortcode
- Supabase or Notion as backend for leaf/story storage

---

## 🧠 Story Use Model

Branches = story themes or personas

Leaves = individual stories, gifts, or tagged quotes

Can serve as:

- Story map
- Tier visualizer
- Legacy grove (for planned giving)

---

## 🎨 Style Inspiration

- Natural forms: oak tree, aspen, river willow
- Visual metaphors: roots = legacy, new leaves = growth
- Match to DCLT linocut branding (or minimalist digital badge layer)

---

## 📌 To Do Next

- Decide tree format (MVP image map or interactive SVG)
- Design mockup (or generate visual in Figma)
- Build leaf/story input system (intake form or donation hook)
- Soft-launch with Fall stories, grow through Giving Tuesday

# 🌳 Digital Giving Tree – Annotated Wireframe

This is a layout plan for an interactive storytelling and donor-recognition experience. The tree grows as stories and gifts are added — each “leaf” is a unique supporter, story, or gift.

---

## 🖥️ Layout Overview

The tree fills the screen and is zoomable + pannable. Core elements:

```
┌────────────────────────────────────────────────────────────┐
│ 🌿 Header: Campaign Name + Tagline                         │
│ e.g. "Join the Story of Wild Door County"                  │
│ CTA Button: [Add Your Leaf]                                │
├────────────────────────────────────────────────────────────┤
│                                                            │
│          🟩 Zoomable Interactive Tree Canvas               │
│       (leaves clickable – show name, quote, badge)         │
│                                                            │
│           - Leaf = Supporter or Story                      │
│           - Color = Tier or Archetype                      │
│           - Branches = Themes or Dates                     │
│                                                            │
│          [Explore Filters] – show/hide:                    │
│           ☐ Legacy Stewards ☐ Monthly Donors ☐ Stories     │
│                                                            │
├────────────────────────────────────────────────────────────┤
│ 📍 Footer Navigation                                       │
│  • Learn More • Join Now • See Full Stories • FAQ         │
└────────────────────────────────────────────────────────────┘

```

---

## 🔍 Interaction Details

| Element | Function |
| --- | --- |
| **Hover on Leaf** | Show name + quote or badge |
| **Click Leaf** | Open modal: full story, photo, option to share |
| **Zoom + Pan** | Explore full tree on desktop or mobile |
| **Filters Panel** | Show only certain types (e.g. new members, archetypes, legacy donors) |
| **Add Your Leaf CTA** | Opens form or donation path |
| **Growth Animation (optional)** | Leaves fade/grow in during campaign |

---

## 🎨 Visual Style Notes

- Linocut-style branches + textured leaves (match DCLT brand)
- Soft animation: wind rustle, leaf shimmer
- Earth-tone palette with subtle motion
- Mobile-responsive fallback: stacked leaves + tabbed filters

---

## 🔗 Data Integration

| Data Type | Source |
| --- | --- |
| Name / Initials | Donation form or story intake |
| Quote | Intake form or email CTA |
| Badge/Icon | Based on selected archetype or gift type |
| Tier/Type | Wild Door Sustainer, Legacy, etc. |
| Gift Amount (Optional) | Used to size or cluster leaves |

---

## 🛠 MVP vs Phase 2 Features

| MVP | Phase 2 |
| --- | --- |
| Static image with hover/click modals | Fully interactive zoom/click/real-time tree |
| Manual leaf updates weekly | Live API or webhook-driven leaf growth |
| Filter by color | Tag-based filtering and search |
| “Add a Leaf” link to form | Embed form or inline donation |
| Export tree as image | Share to social, download badge |

---

## 🧪 Next Steps

- [ ]  Generate wireframe image
- [ ]  Decide MVP platform (WordPress embed? React iframe?)
- [ ]  Draft story + donor intake copy
- [ ]  Sketch visual style options

## Related Documents

**Cross-Referenced Documents**
- [[— Fall–Winter 2025 New Member Campaign (Execution Plan)]]
- [[FAQ]]
- [[Giving Tuesday]]


- [[🧰 Messaging Toolkit]]
- [[📢 Campaign Drafts]]
- [[🎨 Visual Storytelling]]

**Thematic Alignment**
- [[Project Communication Templates]] - fu
- [[Messaging & Engagement Research]] - strategy, bra
- [[Brand + Website: Executive Summary]] - fu