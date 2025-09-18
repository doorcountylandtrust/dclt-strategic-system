---
title: "\u2014 Strategic Initiatives \u2013 Web Integration Build Spec"
project_status: in_progress
priority: medium
stakeholders:
- Strategic Initiatives
- Web Integration
- Build Spec
- Public Hub
- wide Embeds
tags:
- brand
- website
- communication
- strategy
- fundraising
created_date: '2025-09-11'
last_updated: '2025-09-11'
---
# — Strategic Initiatives – Web Integration Build Spec

(Public Hub + Site-wide Embeds)

## PURPOSE
Transform the “Strategic Initiatives in Plain Language” content into a living, interactive web layer that:

- Lives on its own /strategy hub page.
- Appears in context-appropriate spots across the site.
- Uses non-linear web navigation to connect initiatives with stories, preserves, events, volunteer roles, and giving opportunities.
- Stays accurate over time with clear ownership and review cycles.
- Presents the strategic plan                                ([[Website Strategy Hub]]) in a **public-facing, plain-language, fun, and friendly format**.

---

1. VISUAL & STORYTELLING APPROACH
- The hub and embeds should function as an **interactive infographic** rather than a static list.
- Each initiative should be represented visually (iconography, photography, illustration, or short video loops).
- Incorporate **scroll-based storytelling (“scrollytelling”)** to reveal goals, metrics, and stories as the user moves through the page.
- Use **progress visuals** (animated counters, progress bars, milestone markers) to display metrics instead of static numbers.
- Pair every metric or goal with a short human-centered story or example.
- Ensure visuals are **accessible**:
    - Provide text equivalents for all key visuals.
    - Keep animations optional or subtle; provide pause controls if necessary.
    - Maintain full keyboard and screen reader compatibility.
- Tone should remain **inviting and clear**, with active verbs and direct, relatable language.
- Design should make it easy for users to jump directly to the initiatives that interest them (non-linear exploration).

---

## CONTENT MODEL

Taxonomy: initiative (9 terms)

- Land Protection
- Stewardship
- Working Lands
- Conservation Partnerships
- Community Engagement
- Access, Inclusion, and Cultural Competence
- Volunteers
- Organizational Capacity
- Fundraising

Custom fields per initiative term:

- goal (long text)
- messages (multi-line text or array)
- metrics_labels (array)
- icon (string: SVG or lucide icon name)
- color_token (string: Tailwind token)
- slug_override (string, optional)

Attach taxonomy to: post (stories/news), preserve (CPT), event (CPT), volunteer_role (CPT), optionally page.

---

## PAGE IA

/strategy (Hub page):

- Hero: “Strategic Initiatives in Plain Language”
- Accordion grid: 9 initiatives (Goal, Messaging, Metrics) – expandable.
- Related work strip: auto-pulls content tagged to each initiative.
- CTA band: “Back this work” (Donate, Volunteer, Join).

/strategy/{initiative-slug} (Optional detail pages):

- Full initiative narrative.
- Related stories/events/volunteer roles filtered by taxonomy.
- How you can help (initiative-specific CTAs).

---

## REUSABLE BLOCKS

InitiativeBadge: tiny pill (icon + name) linking to initiative page.

InitiativeEmbed: Goal + Messaging + compact Metrics.

InitiativeGrid: Grid of selected initiatives.

InitiativeRelated: Auto-query related content by initiative.

KPIList: Metrics list for initiative.

---

## CROSS-SITE EMBEDDING STRATEGY

Homepage: “Our Work” grid → 9 initiatives; related stories carousel.

Preserve pages: InitiativeBadges showing linked initiatives (“This preserve advances: Stewardship, Land Protection”).

Volunteer hub: Filter volunteer roles by initiative; embed Volunteer initiative messaging.

Events: InitiativeBadges on event cards; filter events by initiative.

Donate/Join pages: Dynamic copy block: “Your gift powers {initiative},” rotating.

News/Stories: Initiative chips under headlines; click-through to initiative pages.

Footer: Mini-strategy strip linking to /strategy.

---

## GOVERNANCE

Initiative content – Owner: Communications – Update every 6 months – Trigger: Strategic plan updates.

Taxonomy tags on content – Owner: All content editors – Update ongoing – Trigger: New story/event/preserve.

Review metrics – Owner: Development/Analytics – Update every 6 months – Trigger: Annual report cycle.

---

## MEASUREMENT PLAN

Track clicks on InitiativeBadges and InitiativeEmbeds (GA4 custom events).

Build /strategy-dashboard to show:

- Number of tagged content per initiative.
- Traffic to initiative pages.
- CTA conversions from initiative blocks.

---

## IMPLEMENTATION CHECKLIST

Development:

- Create initiative taxonomy in code.
- Add custom fields to taxonomy terms.
- Attach taxonomy to relevant CPTs.
- Build reusable Gutenberg blocks for Badge, Embed, Grid, Related, KPIList.
- Style according to brand system.
- Ensure accessibility for accordions and dynamic blocks.

Design:

- Wireframe /strategy hub (desktop + mobile) with infographic/scrollytelling elements.
- Define color/icon for each initiative.
- Create compact + full-width embed styles.

Content:

- Load initiative content into taxonomy fields.
- Tag existing stories/events/preserves with initiatives.
- Draft “How you can help” CTAs per initiative.

---

## VISUAL REFERENCE / WIREFRAME NOTES

![image.png](%E2%80%94%20Strategic%20Initiatives%20%E2%80%93%20Web%20Integration%20Build%20Sp%2024c2a8cd575580079f18cf2e2d444086/image.png)

---

## USER FLOW EXAMPLE

1. Visitor lands on Preserve detail page for a new acquisition.
2. Sees InitiativeBadges for “Land Protection” and “Community Engagement.”
3. Clicks “Land Protection” → /strategy/land-protection.
4. Reads Goal/Messaging → sees recent stories & “Donate to Protect Land” CTA.
5. Donates or signs up for volunteer role.

---

## ACCESSIBILITY & TONE

- All accordions must be keyboard navigable and use ARIA attributes.
- Icons are decorative unless essential to meaning.
- Keep messaging plain and direct.
- Avoid euphemisms; use clear verbs like protect, restore, partner, engage.

---

[[Strategic Initiatives in Plain Language|to see the Public Facing language see this document.]]

![image.png](%E2%80%94%20Strategic%20Initiatives%20%E2%80%93%20Web%20Integration%20Build%20Sp%2024c2a8cd575580079f18cf2e2d444086/image%201.png)

## Related Documents

**Cross-Referenced Documents**
- [[Website Strategy Hub]]
- [[Conservation Partnerships]]
- [[Working Lands]]


- [[Comms Strategy Master Hub]]
- [[2026 Budgeting]]
- [[Mission, Values & Brand Voice]]

**Thematic Alignment**
- [[Project Communication Templates]] - commu
- [[Messaging & Engagement Research]] - commu
- [[Other Brands for Research]] - co