---
title: Website Redesign Release Plan
type: execution
project: website-redesign
status: active
owner: Don
created: 2026-01-12
updated: 2026-01-12
target_launch: 2026-05
related:
  - smart-goal-website-launch
  - website-tech-stack
tags:
  - website
  - project-plan
  - timeline
---

# Website Redesign Release Plan

**Target soft launch:** May 2026  
**Internal review:** April 2026

## Technical Goals

- **Performance:** <100KB initial page load
- **Accessibility:** WCAG AA compliance
- **Mobile-first:** Responsive design for all devices

---

## Completed Work

| Component | Status |
|-----------|--------|
| Site Navigation & Information Architecture | ✓ Complete |
| Preserve Detail Pages with Interactive Maps | ✓ Complete (15 preserves) |
| Donation System (Stripe + Salesforce) | ✓ Complete |
| Newsletter Pipeline (Supabase → Salesforce → Constant Contact) | ✓ Complete |
| Programs & Registration System | ✓ Complete |
| Admin Dashboard for Program Registrations | ✓ Complete |
| Salesforce Campaign Integration | ✓ Complete |
| Waitlist & Capacity Management | ✓ Complete |
| Confirmation & Reminder Emails (Resend) | ✓ Complete |
| Page Templates (About, Give, Visit, What We Do, Take Action) | ✓ Complete |

---

## Timeline

### Q1: Core Completion (Jan–Mar 2026)

| Timeframe | Task | Owner |
|-----------|------|-------|
| Jan | Homepage design and build | Don |
| Jan–Feb | Modular blocks (Hero, CTA Grid, Feature Grid, Stats, Resource List) | Don |
| Feb | Design system documentation (Figma) | Don |
| Feb–Mar | Mobile responsiveness polish | Don |
| Mar 1 | Programs system goes live | Don/Paige |

### Q2: Content & Launch (Apr–May 2026)

| Timeframe | Task | Owner |
|-----------|------|-------|
| Apr | Full content migration from WordPress | Don |
| Apr | Preserve content audit & enhancement | Don |
| Late Apr | Internal staff review & feedback | All Staff |
| Early May | Final QA: accessibility (AA), performance (<100KB), mobile | Don |
| Mid-May | DNS transition & soft launch | Don |
| Late May | Staff training & handoff documentation | Don |

### Q3: Post-Launch & Hubs (Jun–Jul 2026)

| Timeframe | Task | Owner |
|-----------|------|-------|
| Jun | Post-launch fixes, SEO, performance tuning | Don |
| Jun–Jul | Landowner Hub (expanded Protect Your Land experience) | Don |
| Jul | Volunteer Hub (expanded volunteer resources & signup) | Don |
| Jul | Advanced map filters & preserve tagging UI | Don |

### Q4: Documentation & Governance (Aug–Dec 2026)

| Timeframe | Task | Owner |
|-----------|------|-------|
| Aug–Sep | Full system documentation | Don |
| Sep–Oct | Establish content governance & maintenance workflows | Don |
| Nov–Dec | Year-end performance report & analytics review | Don |

---

## Success Indicators

- **Engagement:** 20% higher engagement on key pages (Protect Your Land, Become a Member, Preserves)
- **Clarity:** 15% reduction in email questions due to clearer page content
- **Independence:** Website fully maintained in-house without vendor dependency
- **Performance:** Initial page load under 100KB, Lighthouse score 90+
- **Accessibility:** WCAG AA compliance verified

---

## Key Benefits

- **Organizational Control:** DCLT owns all code, data, and hosting. No vendor lock-in.
- **Cost Reduction:** Eliminates WordPress hosting fees and plugin costs. Cloudflare hosting is free.
- **Performance:** Static site loads faster than WordPress, improving visitor experience and SEO.
- **Integrated Systems:** Donations, registrations, and newsletter all sync directly to Salesforce.
- **Modern Programs System:** Replaces manual registration tracking with automated confirmations, waitlists, and reminders.

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Timeline slippage | Medium | Core features complete; remaining work is content & polish |
| Single technical resource | Medium | Documentation in Q4; modern stack is maintainable |
| Content migration delays | Low | Can launch with core content; add secondary pages post-launch |

---

## Immediate Next Steps (January)

1. Complete homepage design and build
2. Build modular content blocks for page flexibility
3. Test and deploy reminder email system
4. Begin content audit for migration priorities

---

## Files

- [Release Plan (Word doc)](./website-release-plan.docx) — For sharing externally