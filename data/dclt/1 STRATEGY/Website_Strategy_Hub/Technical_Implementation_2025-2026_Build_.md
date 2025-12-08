---
title: "\u2014 Technical Implementation ()"
project_status: planned
priority: low
stakeholders:
- Technical Implementation
- Last updated
- This document
- outlines the
- technical approach
tags:
- brand
- website
- strategy
- fundraising
- conservation
created_date: '2025-09-11'
last_updated: '2025-09-11'
---
# — Technical Implementation 
(2025–2026 Build)

*Last updated: July 2025*

This document outlines the technical approach for the Door County Land Trust website redesign, following our pivot away from Astro + headless WordPress to a custom, sustainable WordPress-based architecture.

---

### **🧭 Purpose**

To build a fast, accessible, and staff-manageable website using:

- A **custom WordPress theme**
- Tailored content types and modular blocks
- Embedded **React components** (e.g., Preserve Explorer)
- A flexible system for long-term maintainability and onboarding

---

## **🧩 Technology Stack**

### **✅ CMS & Backend**

- **WordPress** (non-headless)
- **Advanced Custom Fields (ACF)** for structured content
- **Custom Post Types**:
    - Preserves
    - Events (planned)
    - Possibly Stories or Impact Highlights
- **Plugins** (planned minimal stack):
    - ACF Pro
    - WPGraphQL (for internal tools only)
    - Formstack, WPForms or Gravity Forms (legacy forms)
    - GiveWP or GiveLively (donations, external for now)
    - Custom plugin for Preserve Explorer map

---

### **🎨 Frontend**

- **Custom Theme** using:
    - TailwindCSS for design system consistency
    - WordPress-native template files and partials (page-preserve.php, etc.)
    - Reusable component classes that match our Figma tokens
- **Interactive Elements**:
    - React + Leaflet embedded in template for Preserve Explorer
    - JS-based overlays for filters, events, and user interactivity
- **Accessibility Goals**:
    - All pages must meet WCAG 2.1 AA standards
    - Navigation, maps, and CTAs fully keyboard-navigable
    - Responsive font sizes and flexible layout containers

---

### **🗂️ Content & Layout Strategy**

- **Homepage & Modular Sections**:
    - Built with reusable layout blocks (Hero, Grid, CTA, Timeline, etc.)
    - Blocks mapped to real CTAs in our supporter funnels
    - Allows future swapping or reordering without dev help
- **Preserve Detail Pages**:
    - Pulled from CPTs with fields for acreage, trail maps, access notes
    - Map links or embedded views as needed
- **Dynamic Funnels**:
    - Landing pages for Donors, Landowners, Volunteers
    - “Choose Your Path” routing based on persona needs or interests

---

## **🚀 Deployment Plan**

- **Environment**:
    - Local + staging + production WordPress environments
    - GitHub repo for theme + plugin version control
    - Tailwind compiled using a build pipeline (Vite or WP Scripts)
- **Fallbacks**:
    - Minimal plugin dependency = easier recovery if site breaks
    - No headless system = faster fixes and no rebuild pipeline dependencies
- **Editor Support**:
    - WP dashboard will expose structured content fields
    - Editors will not need to manage layout or CSS
    - Documentation for basic edits and when to escalate to dev support

---

## **🛠️ Dev Priorities (Summer–Fall 2025)**

1. ✅ Preserve CPT working and visible on site
2. 🟡 Add events CPT and test filters on map
3. 🟡 Finalize React component integration for map filtering
4. 🔲 Build homepage with modular blocks
5. 🔲 Develop “Join / Renew / Donate” funnel with CTA logic
6. 🔲 Begin QA passes for accessibility and mobile responsiveness

---

## **🔐 Sustainability & Handoff Plan**

- **Codebase will be cleanly structured and documented**
- **README** includes:
    - Local dev setup
    - ACF field mappings
    - File routing conventions
    - Tailwind design token references
- **Slack or internal doc for “What to do if…” scenarios**
- **Eventually:** Add GitHub Actions to test accessibility and broken links

## **🧱 Theme Strategy: Custom vs Pre-Made**

As part of implementation planning, we evaluated whether to use a **custom-built theme** or a **pre-made theme + page builder combo**.

### **Option 1:**

### **Custom Theme (Chosen Direction)**

- Built from scratch with Tailwind, ACF, and WordPress templates
- Matched exactly to our content model and Figma designs
- Minimal plugin dependency = faster, cleaner, more secure
- Long-term maintainability, onboarding-friendly

✅ **We chose this path** for flexibility, accessibility control, and future-proofing.

---

### **Option 2:**

### **Pre-Made Theme + Page Builder (e.g., Elementor, Kadence, Blocksy)**

- Faster initial build
- Visual editor for staff
- But:
    - Often adds visual bloat
    - Can introduce accessibility issues
    - Plugin lock-in risk
    - Harder to maintain a clean, modular system

🧠 **Considered as fallback** if timelines or staffing required rapid page deployment.

---

### **Why This Matters**

We’re designing this site not just to launch, but to **evolve over time** — content, visuals, and user experience.

A custom theme gives us the creative and structural freedom to do that without rebuilding again in 2 years.

| **Criteria** | **Custom Theme** | **Builder Theme (Kadence / Elementor)** |
| --- | --- | --- |
| **Initial Build Speed** | 🚧 Slower (but cleaner) | ⚡ Faster to launch with templates |
| **Performance** | ⚡ Fast, minimal bloat | 🐢 Often slower due to scripts, layout bloat |
| **Accessibility Control** | ✅ Full control | ❌ Risk of non-compliant elements |
| **Brand Fidelity** | 🎯 Matches Figma (wireframe software) exactly | 🎨 Approximate or requires overrides |
| **Editor Friendliness** | 🟡 Good with ACF, docs | ✅ Very easy (drag & drop UI) |
| **Plugin Lock-in** | 🔓 None | 🔒 High (hard to migrate away later) |
| **Technical Overhead** | 🛠 Requires dev support  | 🧩 Easier to manage short term |
| **Long-Term Cost** | 💰 Lower (no paid builder) | 💸 Higher (licensing, rebuilds, support) |
| **Future Flexibility** | ♻️ Easy to scale, adapt | 📦 Often constrained by builder ecosystem |

---

## **📎 Related Pages**

- 🔗 [Preserve Explorer Dev Log](https://www.notion.so/paste-link)
- 🔗 [Figma Design System Overview](https://www.notion.so/paste-link)
- 🔗 [Modular Content Blocks](https://www.notion.so/paste-link)
- 🔗 [Website Roadmap 2025–2026](https://www.notion.so/paste-link)

[— Retired Approach - Astro + Headless WP Technical Implementation](%E2%80%94%20Technical%20Implementation%20(2025%E2%80%932026%20Build)%202302a8cd575580208f20c94bcf644264/%E2%80%94%20Retired%20Approach%20-%20Astro%20+%20Headless%20WP%20Technical%201c42a8cd575580f090dcf295a699da68.md)

## Related Documents

**Cross-Referenced Documents**
- [[Website Strategy Hub]]
- [[Volunteers]]
- [[— Retired Approach - Astro + Headless WP Technical Implementation ()]]


- [[Comms Strategy Master Hub]]
- [[2026 Budgeting]]
- [[Mission, Values & Brand Voice]]

**Thematic Alignment**
- [[Project Communication Templates]] - strategy, bra
- [[Messaging & Engagement Research]] - fu
- [[Other Brands for Research]] - co