---
title: "Strategic Initiative #2: Stewardship"
project_status: active
priority: high
stakeholders:
  - Stewardship Director
  - Land Protection Director
  - Communications
tags:
  - website
  - communication
  - conservation
  - strategic-plan
created_date: '2025-09-11'
last_updated: '2026-01-27'
---

# Stewardship

**Strategic Goal:** Increase the monitoring and management of lands and waters under DCLT's care. Uphold high standards for maintenance and restoration. Balance recreational access to ensure people and nature thrive.

---

## Messaging

**Primary:**
- "Caring for the lands we protect is a forever promise."

**Supporting:**
- "Restoring nature, one acre at a time."
- "Protection is just the beginning. Stewardship is the long work."
- "We don't just save land. We care for it."

**For Visitors:**
- "These trails don't maintain themselves."
- "Every bench, every bridge, every cleared path—that's stewardship."

**For Donors:**
- "Your gift keeps these lands healthy for generations."
- "Stewardship is the forever cost of forever protection."

**For Volunteers:**
- "This is where your work shows up."
- "Pull garlic mustard. Clear a trail. Restore a prairie. This is stewardship."

---

## Key Metrics (Organizational)

| Metric | Current | 5-Year Target |
|--------|---------|---------------|
| Acres restored or maintained | — | Track annually |
| Invasive species managed (acres) | — | Track annually |
| Volunteer stewardship hours | — | Increase |
| Prescribed burns completed | — | Track annually |
| Baseline inventories completed | — | 100% new, 50% existing |
| Management plans revised | — | All properties |
| Bear Creek infrastructure | — | Complete with public access |

---

## Website Integration

### Primary Pages

| Page | URL | Status | Purpose |
|------|-----|--------|---------|
| Stewardship | /what-we-do/stewardship | ✓ Exists | Explainer |
| Preserves (all) | /properties | ✓ Exists | Trail info, maps |
| Individual Preserve Pages | /properties/[slug] | ✓ Exists | Specific stewardship context |
| Volunteer | /take-action/volunteer | ✓ Exists | Stewardship workdays |
| Hunting Program | /what-we-do/hunting-program | ✓ Exists | Managed access |

### User Journeys

**Visitor wanting to understand the work:**
1. Visits preserve, sees trail in good condition
2. Wonders "who maintains this?"
3. Visits /what-we-do/stewardship
4. Reads about restoration, invasive management, volunteer work
5. Either donates or signs up to volunteer

**Donor wanting to see impact:**
1. Receives appeal mentioning stewardship needs
2. Clicks through to stewardship page or preserve page
3. Sees before/after restoration photos
4. Understands ongoing cost of "forever"
5. Gives to stewardship fund (if designated option exists)

**Volunteer seeking hands-on work:**
1. Wants to do something physical, outdoors
2. Finds stewardship workday on events page
3. Registers, shows up, removes invasive species
4. Sees direct impact of their work
5. Returns, becomes regular volunteer

### Key CTAs

| CTA Text | Destination | Placement |
|----------|-------------|-----------|
| "See how we care for the land" | /what-we-do/stewardship | Homepage, What We Do |
| "Join a workday" | /visit/events-programs (filtered) | Stewardship page, Volunteer hub |
| "Explore our preserves" | /properties | Stewardship page |
| "Support stewardship" | /donate | Stewardship page (if fund exists) |

### Content Inventory

| Content Type | Status | Notes |
|--------------|--------|-------|
| Stewardship explainer page | ✓ Exists | Review for depth |
| Before/after restoration photos | ⚠ Needed | Oak Bluff, others |
| Stewardship stories (field notes) | ⚠ Needed | Recurring content type |
| Interactive preserve maps | ✓ Exists | Leaflet implementation |
| Trail condition updates | ⚠ Future | Could add status to preserve pages |
| Invasive species guide | ⚠ Future | Educational content |
| Prescribed burn explainer | ⚠ Needed | Why we burn, safety, ecology |
| Volunteer impact stats | ⚠ Needed | Hours, acres, visible results |

### Preserve Page Integration

Each preserve page should reflect stewardship:

| Element | Status | Notes |
|---------|--------|-------|
| Trail info (miles, difficulty) | ✓ Exists | In frontmatter |
| Facilities (parking, kiosk) | ✓ Exists | In filters |
| Restoration status | ⚠ Needed | "Active prairie restoration" |
| Stewardship history | ⚠ Future | Deep Map layer |
| Recent work completed | ⚠ Future | "Trail rerouted Fall 2025" |

### Success Metrics (Website-Specific)

| Metric | Tool | Notes |
|--------|------|-------|
| Stewardship page visits | Analytics | Baseline, track growth |
| Preserve page visits | Analytics | Most-visited preserves |
| Workday event registrations | Supabase | Filter by event_type |
| Time on preserve pages | Analytics | Engagement signal |
| Map interactions | Analytics (if tracked) | Clicks, zooms |

---

## Gaps & Opportunities

### Content Gaps
- [ ] No before/after restoration gallery
- [ ] No "Field Notes" or stewardship blog series
- [ ] No prescribed burn explainer
- [ ] No stewardship-specific volunteer recruitment

### UX Gaps
- [ ] Preserve pages don't show current restoration projects
- [ ] No way to filter preserves by "recently improved"
- [ ] No trail condition/closure alerts

### Storytelling Gaps
- [ ] Stewardship is invisible unless you look for it
- [ ] Homepage doesn't mention ongoing care
- [ ] Donation form doesn't have stewardship fund option (if applicable)

### Deep Map Opportunity
The Preserve Explorer design document includes:
> "Human Time: restoration work, ongoing stewardship, recent acquisitions"

Stewardship stories are the "Living Time" layer of the Deep Map.

---

## Related Initiatives

- **#1 Land Protection** — Stewardship follows acquisition
- **#3 Working Lands** — Restoration plans for acquired ag land
- **#7 Volunteers** — Stewardship workdays are primary volunteer activity
- **#5 Community Engagement** — Stewardship visible through events, stories

---

## Related Documents

- [[Preserve Explorer Design Document]] — Map integration, Deep Map vision
- [[Properties Content Collection]] — Preserve frontmatter schema
- [[Volunteers]] — Workday recruitment
- [[Strategic Initiatives in Plain Language]]

---

## Review Cadence

- **Monthly:** Check workday registrations
- **Quarterly:** Audit preserve pages, plan restoration stories
- **Annually:** Review against strategic plan, update management plan status