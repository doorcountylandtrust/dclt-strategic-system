# 🧠 UX + Interaction Design Decisions Log

## Click vs Hover - Subnav Interaction Decision

### **🧠 Decision**

Use **click to reveal** for desktop sub-navigation menus (instead of hover-to-reveal behavior).

---

### **💬 Rationale**

- **Predictability:** Users can control the interaction more precisely; avoids accidental activation from passing cursor movement.
- **Consistency:** Mobile and tablet already require click/tap. Using click on desktop unifies behavior across devices.
- **Accessibility:** Hover states don’t exist on touchscreens and can introduce cognitive load for users with motor or visual impairments.
- **User Control:** Click to reveal respects intentional interaction. Avoids “menu surprise” when users are navigating quickly.
- **Evidence from user frustration:** Team members (incl. Comms) report personal annoyance with hover menus when quickly moving the cursor — common and valid UX complaint.

---

### **🦾 Accessibility Notes**

- Click-based menus are:
    - Easier to make **keyboard-accessible**
    - More **screen reader-compatible**
    - Less likely to interfere with **focus order or skip navigation**
- Hover-only menus fail **WCAG 2.1 Guideline 1.4.13 (Content on Hover or Focus)** if not implemented carefully.

---

### **🔁 Reversal Criteria**

We are open to reverting to hover behavior **only if:**

- Analytics or user testing show confusion or drop-off
- Stakeholders present a compelling case with accessibility-safe implementation
- A hybrid interaction model (click-to-open with hover cues) becomes justified and testable

---

### **📚 References & Inspiration**

- [Nielsen Norman Group – Hover Menus](https://www.nngroup.com/articles/mega-menus-work-well/)
- [WCAG 2.1 Guidelines – Content on Hover or Focus](https://www.w3.org/WAI/WCAG21/Understanding/content-on-hover-or-focus.html)
- [Inclusive Components – Menus](https://inclusive-components.design/menus-menu-buttons/)

## **List View vs. Map View**

**Date:** July 22, 2025

**Owner:** LandComm

**Status:** Resolved

---

### **🎯 Problem**

Users in List View and Map View may have different goals. We need to decide:

- Whether List View should behave like Map View
- If filters should persist
- How to support both spatial and detail-oriented browsing

---

### **🧭 Insight**

**Map View users** are in a *“where is it?”* mindset

→ Spatial relevance, trip planning, location-first thinking

**List View users** are in a *“what is it?”* mindset

→ Content detail, attribute filtering, side-by-side comparison

These modes reflect different user **intent** and **cognitive framing**.

---

### **✅ Decisions**

| **Area** | **Decision** |
| --- | --- |
| Filters | Filters will persist in List View |
| Detail View | Clicking a List Item will open the same overlay panel as Map View (not a separate page) |
| Spatial Awareness | Each card will include a **“View on Map”** button or location label |
| Canonical URLs | Preserve detail pages will still exist for SEO, but users primarily explore through the panel overlay |

---

### **🔄 Implications**

- This avoids fragmenting UX into two disjointed systems
- Maintains app-like continuity across all modes
- Supports both exploratory and decision-focused user journeys
- Sets a pattern that can be reused in other DCLT interfaces

---

### **🔗 Related**

- [UX System: Design Paradigms Log](https://www.notion.so/notion-link-if-you-have-it)
- [Preserve Explorer – Wireframes](https://www.notion.so/link)
- [Preserve Explorer – IA Map](https://www.notion.so/link)

## Breadcrumb Retention Rationale

We’re retaining a persistent breadcrumb component on all pages (including Preserve Detail) for the following reasons:

- **Spatial consistency**: Keeping the breadcrumb in the same location across views builds user trust and predictability.
- **Cognitive orientation**: Even on pages with a clear visual title (e.g. “Bear Creek”), the breadcrumb reinforces site structure and provides a fast return path to "All Preserves."
- **Avoids visual jumpiness**: Removing it from some pages would cause the main content area to shift vertically, which creates dissonance and breaks flow.
- **Low visual weight, high utility**: The design is minimal and subordinate to the header, so it doesn’t compete for attention but remains useful.

📍Design is touch-friendly, viewport-aligned, and consistent with the site’s overall grid and hierarchy.

### Heuristic: Visibility of System Status

Breadcrumbs contribute to the user's understanding of “where they are” within the system at all times—especially useful in map-based navigation, where entry points may vary. This reinforces the user's mental model of site structure and provides reassurance through persistent orientation cues.