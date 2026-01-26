---
title: "Strategic Initiative #6: Access, Inclusion, and Cultural Competence"
project_status: active
priority: high
stakeholders:
  - Executive Director
  - All Staff
  - Board
  - Communications
tags:
  - website
  - communication
  - conservation
  - strategic-plan
  - DEIA
created_date: '2025-09-11'
last_updated: '2026-01-27'
---

# Access, Inclusion, and Cultural Competence

**Strategic Goal:** Equip staff and board with knowledge and skills to leverage diverse perspectives. Ensure policies, land management, communications, and programming serve underserved communities. Recognize Indigenous history on the lands we steward.

---

## Messaging

**Primary:**
- "Everyone belongs in nature."

**Supporting:**
- "We're working to remove barriers so all feel welcome on the land."
- "These lands have always been home to many peoples."
- "Conservation is for everyone."

**Land Acknowledgment (draft):**
> "Door County Land Trust recognizes that the lands we steward are the ancestral home of the Menominee, Ojibwe, Potawatomi, and Ho-Chunk peoples. We honor their enduring relationship with this place."

*Note: Final language should be developed with tribal consultation.*

---

## Key Metrics (Organizational)

| Metric | Current | 5-Year Target |
|--------|---------|---------------|
| Staff/board DEIA training completed | — | 100% |
| Accessibility improvements at preserves | — | Track |
| Partnerships with historically excluded communities | — | Increase |
| Representation in photos, stories, programming | — | Audit annually |
| Indigenous history integrated into communications | — | All preserve narratives |

---

## Website Integration

This initiative is primarily an **audit and review** effort, not new page creation.

### Audit Checklist

#### Language Review

| Check | Status | Notes |
|-------|--------|-------|
| Gendered language removed | ⚠ Audit needed | "mankind" → "people", etc. |
| Ability assumptions removed | ⚠ Audit needed | "easy hike" → describe terrain |
| Welcoming tone throughout | ⚠ Audit needed | Not exclusive or jargon-heavy |
| Clear, plain language | ⚠ Audit needed | Accessible reading level |

#### Imagery Review

| Check | Status | Notes |
|-------|--------|-------|
| Diverse people represented | ⚠ Audit needed | Age, race, ability, family types |
| Not tokenizing | ⚠ Audit needed | Authentic, not performative |
| Accessibility visible | ⚠ Audit needed | Show boardwalks, benches, varied access |
| Indigenous imagery | ⚠ Sensitive | Only with consultation and consent |

#### Accessibility (WCAG)

| Check | Status | Notes |
|-------|--------|-------|
| Alt text on all images | ⚠ Audit needed | Descriptive, not decorative |
| Color contrast sufficient | ⚠ Audit needed | AA compliance minimum |
| Keyboard navigation works | ⚠ Audit needed | All interactive elements |
| Screen reader compatible | ⚠ Audit needed | Semantic HTML, ARIA labels |
| Captions on videos | ⚠ Audit needed | When video content exists |

#### Indigenous Context

| Check | Status | Notes |
|-------|--------|-------|
| Land acknowledgment in footer | ⚠ Needed | Draft exists, needs consultation |
| Preserve histories include pre-colonial context | ⚠ Future | Deep Map layer |
| Tribal consultation completed | ⚠ Not started | Required before publishing |
| No appropriation or speculation | — | Ongoing vigilance |

### Primary Pages for Review

| Page | Priority | Focus |
|------|----------|-------|
| Homepage | High | Imagery, welcome tone |
| All preserve pages | High | Trail descriptions, accessibility info |
| Volunteer hub | High | "Everyone welcome" messaging |
| Events & Programs | High | Accessibility notes on events |
| About pages | Medium | Inclusive org description |
| Footer | High | Land acknowledgment placement |

### Content Needs

| Content Type | Status | Notes |
|--------------|--------|-------|
| Land acknowledgment | ⚠ Draft exists | Needs tribal consultation |
| Accessibility info per preserve | ⚠ Partial | In frontmatter, not all complete |
| "Visiting with accessibility needs" page | ⚠ Needed | Centralized resource |
| Indigenous history content | ⚠ Future | Deep Map, with consultation |

### Preserve Accessibility Data

The properties schema already includes:
```yaml
filters:
  accessibility: ["wheelchair-accessible", "stroller-friendly"]
  physical_challenges: ["stairs", "steep-slopes", "uneven-terrain"]
  trail_surface: ["natural", "boardwalk", "gravel", "mowed"]
  facilities: ["parking", "restroom", "kiosk", "bench"]
```

**Gap:** Not all preserves have this data populated. Need audit.

---

## Implementation Approach

### Phase 1: Low-Effort, High-Signal (Now)

- [ ] Add land acknowledgment to footer (after consultation)
- [ ] Audit homepage imagery
- [ ] Review "easy/moderate/difficult" language on preserve pages
- [ ] Add accessibility notes to event descriptions

### Phase 2: Content Audit (Q2)

- [ ] Full language review across all pages
- [ ] Imagery audit with diversity lens
- [ ] WCAG accessibility scan
- [ ] Populate accessibility data for all preserves

### Phase 3: Deep Integration (Post-Launch)

- [ ] Indigenous history in preserve narratives (with consultation)
- [ ] "Visiting with accessibility needs" resource page
- [ ] Tribal partnership content (if relationships develop)
- [ ] Staff/board training reflected in About content

---

## Gaps & Opportunities

### Immediate Gaps
- [ ] No land acknowledgment on website
- [ ] Accessibility info incomplete on preserve pages
- [ ] No centralized accessibility resource
- [ ] Imagery audit not completed

### Strategic Alignment
- [ ] "Signage recognizes historical influences before European settlers" — website should match
- [ ] "Diverse, equitable workplace culture" — About page could reflect
- [ ] Training completion — not website-visible, internal

### Sensitive Considerations
- Indigenous content requires **consultation before publishing**
- Avoid performative gestures without substance
- Land acknowledgment is a beginning, not a checkbox

---

## Related Initiatives

- **#4 Conservation Partnerships** — Tribal partnerships
- **#5 Community Engagement** — Welcoming all community members
- **#7 Volunteers** — Diverse volunteer recruitment

---

## Related Documents

- [[Preserve Explorer Design Document]] — Deep Map Indigenous layer
- [[Properties Content Schema]] — Accessibility fields
- [[Strategic Initiatives in Plain Language]]

---

## Review Cadence

- **Quarterly:** Imagery and language spot-check
- **Annually:** Full accessibility audit, representation review
- **Ongoing:** Tribal consultation progress