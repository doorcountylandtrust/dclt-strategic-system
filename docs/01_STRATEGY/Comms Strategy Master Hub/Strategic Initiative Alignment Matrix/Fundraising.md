---
title: "Strategic Initiative #9: Fundraising"
project_status: active
priority: critical
stakeholders:
  - Development Director
  - Executive Director
  - Communications
  - Board (100% engagement goal)
tags:
  - website
  - communication
  - strategy
  - fundraising
  - strategic-plan
created_date: '2025-09-11'
last_updated: '2026-01-27'
---

# Fundraising

**Strategic Goal:** Secure resources to protect Door County forever. Launch a capital campaign, grow membership and legacy giving, ensure long-term financial strength. Reach 10% of Door County's population as donors. Achieve 5% Legacy Circle participation among members.

---

## Messaging

**Primary:**
- "Your gift protects the places you love."

**Supporting:**
- "Forever is possible because of your support."
- "Membership starts at $50. Every dollar protects Door County."
- "Join 2,000+ members who believe in this place."

**For New Donors:**
- "This is how you make a difference here."
- "Not a transaction. A relationship."

**For Renewal:**
- "Thank you for another year of protection."
- "Your continued support keeps this land safe."

**For Legacy Giving:**
- "Your love for this place can outlast you."
- "Leave a legacy as lasting as the land."
- "The ultimate gift: forever."

**For Major Gifts / Capital Campaign:**
- "This is the moment. This land won't wait."
- "Transformational gifts. Permanent protection."

---

## Key Metrics (Organizational)

| Metric | Current | 5-Year Target |
|--------|---------|---------------|
| Annual fundraising goal | — | Per Development Plan |
| New donors annually | — | 10% of Door County population giving |
| Donor retention rate | — | Track year-over-year |
| Average gift size | — | Increase |
| Legacy Circle members | — | 5% of membership |
| Unrestricted vs. restricted ratio | — | Balance per plan |
| Board engagement in fundraising | — | 100% |
| Capital campaign progress | — | Per campaign goal |

---

## Website Integration

### Primary Pages

| Page | URL | Status | Purpose |
|------|-----|--------|---------|
| Donate | /donate | ✓ Exists | Primary conversion |
| Give Hub | /give | ✓ Exists | Overview of giving options |
| Ways to Give | /give/ways-to-give | ✓ Exists | Stock, DAF, IRA, etc. |
| Legacy Giving | /give/legacy-giving | ✓ Exists | Planned gifts |
| Business Members | /give/business-members | ✓ Exists | Corporate giving |
| Donor Stories | /give/donor-stories | ⚠ Needed | Social proof |
| Our Supporters | /give/supporters | ⚠ Partial | Recognition |

### User Journeys

**First-time donor:**
1. Visits homepage, sees "Support Our Work" threshold
2. Clicks through to /give or /donate
3. Sees membership tiers ($50 / $250 / $500)
4. Completes Stripe checkout
5. Receives thank-you email
6. Enters welcome series (drip campaign)

**Lapsed donor (renewal):**
1. Receives renewal email with personalized link
2. Clicks through to /donate?intent=renew
3. Sees "Thank you for your continued support"
4. Completes renewal
5. Receives acknowledgment

**Legacy prospect:**
1. Long-time member, 65+
2. Receives legacy-focused appeal or sees footer CTA
3. Visits /give/legacy-giving
4. Reads about bequest, beneficiary designation options
5. Downloads info or contacts staff
6. Has conversation, makes commitment

**Major donor / Capital campaign:**
1. Receives personal outreach from staff/board
2. Visits website to learn more
3. Sees impact stories, land protection progress
4. Has meetings, makes transformational gift
5. Recognized on website (with permission)

### Key CTAs

| CTA Text | Destination | Placement |
|----------|-------------|-----------|
| "Give Now" | /donate | Header, homepage, all pages |
| "Join Us" | /donate?intent=join | Homepage threshold, membership content |
| "Renew Your Membership" | /donate?intent=renew | Email, member portal (future) |
| "Leave a Legacy" | /give/legacy-giving | Footer, Give pages |
| "See Ways to Give" | /give/ways-to-give | Donate page, Give hub |
| "Read Donor Stories" | /give/donor-stories | Give pages |

### Content Inventory

| Content Type | Status | Notes |
|--------------|--------|-------|
| Donation form | ✓ Exists | Stripe checkout, working |
| Membership tiers | ✓ Exists | $50 / $250 / $500+ |
| Ways to Give page | ✓ Exists | Stock, DAF, IRA |
| Legacy Giving page | ✓ Exists | Review for warmth |
| Donor stories | ⚠ Needed | 3-5 profiles |
| Impact stats | ⚠ Partial | On homepage, could expand |
| Thank-you page | ✓ Exists | /thank-you |
| Welcome email series | ✓ Exists | Drip campaign in place |
| Campaign landing page | ⚠ Future | For capital campaign |
| Supporter recognition | ⚠ Partial | Needs design/content |

### Donation Form Features (Current)

| Feature | Status |
|---------|--------|
| Preset amounts ($50, $100, $250, $500) | ✓ |
| Custom amount | ✓ |
| Monthly giving toggle | ✓ |
| Cover transaction fees option | ✓ |
| Tribute gifts (honor/memory) | ✓ |
| Business gifts | ✓ |
| Employer matching field | ✓ |
| Campaign tracking (URL params) | ✓ |
| Intent-based headlines (join/renew/tribute) | ✓ |
| Anonymous option | ✓ |
| Birthday field (optional) | ✓ |

### Success Metrics (Website-Specific)

| Metric | Tool | Target |
|--------|------|--------|
| Donation page visits | Analytics | Track monthly |
| Donation conversion rate | Analytics + Supabase | Visits → completions |
| Average online gift | Supabase / Stripe | Track quarterly |
| Monthly giving signups | Supabase | Growing % of total |
| Legacy page visits | Analytics | Track, correlate to inquiries |
| Legacy inquiries | Staff tracking | Per strategic plan |
| Email click-through to donate | Resend / Supabase | By campaign |
| Tribute gift volume | Supabase | Track seasonally |

---

## Gaps & Opportunities

### Content Gaps
- [ ] No donor stories page (critical for social proof)
- [ ] No "Why I Give" testimonials
- [ ] No capital campaign landing page (when ready)
- [ ] Supporter recognition page incomplete

### UX Gaps
- [ ] No member portal (renewal, giving history)
- [ ] No "suggested amount" based on past giving
- [ ] No progress thermometer for campaigns

### Conversion Gaps
- [ ] Homepage form captures email but doesn't immediately convert to donor
- [ ] Legacy giving CTA not prominent enough
- [ ] No abandoned cart / incomplete donation recovery

### Strategic Plan Alignment
- [ ] "10% of Door County giving" — need to define and track
- [ ] "100% board engagement" — not website-visible, but could add board giving recognition
- [ ] "5% Legacy Circle" — need clear Legacy Circle definition and promotion

---

## Integration with Donation Form

The current DonationForm.tsx supports:
```
URL Parameters:
- ?amount=100 — Pre-select amount
- ?campaign=warner-2025 — Track campaign source
- ?intent=join|renew|tribute|business — Change headline, auto-open sections
- ?match=true — Show matching gift banner
```

**Campaign IDs in use:**
- `warner-2025` → 701Vo00000ud2GEIAY
- `conservation-stewardship` → 701Vo00000W8abmIAB
- Default (new member) → 701Hp000001SqoKIAS

---

## Related Initiatives

- **#1 Land Protection** — Land Acquisition Fund, project-specific appeals
- **#5 Community Engagement** — Events drive donor acquisition
- **#7 Volunteers** — Volunteer → donor conversion
- **#8 Organizational Capacity** — Fundraising supports staffing

---

## Related Documents

- [[DonationForm.tsx]] — Technical implementation
- [[Campaigns]] — Campaign messaging and tracking
- [[Welcome Email Series]] — New donor nurture
- [[Strategic Initiatives in Plain Language]]

---

## Review Cadence

- **Weekly:** Monitor donation volume (during campaigns)
- **Monthly:** Review conversion rates, average gift
- **Quarterly:** Audit content, plan donor stories
- **Annually:** Full alignment check with Development Plan