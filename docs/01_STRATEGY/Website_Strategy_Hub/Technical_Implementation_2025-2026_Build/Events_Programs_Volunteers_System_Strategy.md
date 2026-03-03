---
title: "Events, Programs & Volunteers System Strategy"
type: strategy
status: active
updated: 2026-03-03
tags: []
---

# Events, Programs & Volunteers System Strategy

**Last Updated:** December 2024  
**Stakeholder Meeting:** December 12, 2024  
**Participants:** Paige (Community Conservation Coordinator), Don (Developer)  
**Hard Deadline:** Guided programs registration live by March 1, 2025

**Architecture Reference:** See `System_Architecture.md` for technical implementation details.

---

## Executive Summary

DCLT is building a custom registration and volunteer management system integrated with its existing infrastructure: WordPress (content), Supabase (data), Resend (email), and Salesforce (CRM). This replaces the current Give Lively-based event registration, which requires double-entry and lacks proper Salesforce integration.

**Core problems being solved:**
1. Double-entry for events (website + Give Lively)
2. Manual registration list management and distribution to hike leaders
3. Poor Salesforce integration
4. Volunteer signup buried and disconnected from Salesforce Volunteers app
5. No automated confirmations or reminders

**Approach:** Custom build using existing Supabase + Resend infrastructure, with WordPress handling display and Salesforce as the CRM sync target.

---

## Current State & Pain Points

### Events/Programs

| Pain Point | Impact |
|------------|--------|
| Events created twice (website + Give Lively) | Staff time, sync errors |
| Registration exports poorly formatted | Manual cleanup required |
| Hike leaders can't self-serve registration lists | Coordinator bottleneck |
| No user accounts — repeat visitors re-enter info | Poor UX, incomplete data |
| No automated confirmation/reminder emails | Manual sends or missed communications |
| Can't track if registrant is first-time or returning | Limits donor journey insights |
| Accessibility info not prominent | Visitors unsure if they can participate |

### Volunteers

| Pain Point | Impact |
|------------|--------|
| Signup buried in Contact or Give sections | Hard to find, poor conversion |
| Manual entry into Salesforce Volunteers app | Staff time (Amy) |
| No automated welcome email | Inconsistent onboarding |
| No digital volunteer manual sign-off | Paper process or skipped entirely |
| Limited volunteer stories/promotion | Harder to recruit diverse volunteers (youth, families) |

---

## Requirements

### Events & Programs

#### Information Architecture
- **Events** (Annual Gathering, fundraisers, galas) may need separate handling from **Programs** (guided hikes, workshops, Science on Tap)
- Different audiences, different user journeys
- Implementation: Single CPT with "Event Type" taxonomy for filtering

#### Event Listing (At a Glance)
- Title
- Location (preserve name)
- Date & Time
- Free or Fee indicator
- One-sentence description

#### Event Detail Page
- Full description (what will be discussed, why attend)
- Accessibility info: trail length, conditions, difficulty
- What to bring/wear
- Rules (e.g., no dogs)
- Family-friendly tag
- Members-only flag (with membership CTA)
- Registration button (one click to form)

#### Registration Flow
1. Visitor sees event (website, email, social)
2. One click to registration form
3. Form collects: name, email, phone, party size
4. On submit → data posts to Supabase
5. Supabase creates/updates contact record
6. Supabase inserts registration record
7. Supabase triggers confirmation email via Resend
8. Supabase syncs to Salesforce (Contact + Campaign Member)
9. User sees confirmation on page

#### Staff/Leader Features (Phase 2)
- Hike leaders can view and download their own registration lists
- Capacity tracking with "Sold Out" or "Waitlist" indicators
- Automated waitlist management

#### Display Options
- List view with filters (event type, date, location, audience)
- Calendar view (Phase 2)

#### Future Considerations (Phase 3)
- Phenology-based alerts: "Wildflowers are blooming — join us Saturday"
- iNaturalist / citizen science integration
- Pop-up events with short notice

---

### Volunteers

#### Information Architecture
- Dedicated Volunteer page, prominent in navigation
- Clear pathway from homepage and Take Action section

#### Page Content
- Overview of volunteer program
- Position descriptions (on-page or downloadable)
- Clear expectations for communication/response times
- Volunteer stories and quotes
- Photos of volunteers in action
- Dynamic content: recent volunteer stories from blog (Phase 2)

#### Signup Flow
1. Simple form on Volunteer page
2. Form collects: name, email, phone, interests, availability
3. On submit → data posts to Supabase
4. Supabase creates/updates contact record
5. Supabase inserts volunteer record
6. Supabase triggers welcome email via Resend
7. Supabase syncs to Salesforce Volunteers app
8. Staff notification (Paige) for new signups
9. User sees confirmation on page

#### Maintenance
- Form easily updated as volunteer needs change
- Page content manageable by staff without developer

---

## Technical Implementation

### WordPress Responsibilities
- `dclt_program` Custom Post Type
- Taxonomies: Event Type, Location (Preserve)
- Meta box with fields: date, time, location, fee amount, capacity, accessibility info, family-friendly, members-only, what to bring, rules
- Archive template with filtering
- Single event template with registration form
- Volunteer page template with signup form
- Form UI (client-side validation, submission handling)

### Supabase Responsibilities
- `registrations` table (see System_Architecture.md for schema)
- `volunteers` table
- Edge functions for form processing
- Triggers for email and Salesforce sync
- `email_queue` table for scheduled reminders (Phase 2)

### Resend Responsibilities
- `registration-confirmation` email template
- `registration-reminder-2day` template (Phase 2)
- `registration-reminder-day` template (Phase 2)
- `volunteer-welcome` email template

### Salesforce Sync
- Registration → Contact + Campaign Member
- Volunteer → Contact + Volunteer record (Volunteers app)
- First interaction source tracked for donor journey

---

## MVP Scope (March 1, 2025)

### In Scope

**WordPress:**
- [ ] `dclt_program` CPT with taxonomies
- [ ] Meta box for all event fields
- [ ] Archive template (list view, basic filters)
- [ ] Single event template (full detail + registration form)
- [ ] Registration form (name, email, phone, party size)
- [ ] Volunteer page with signup form

**Supabase:**
- [ ] `registrations` table
- [ ] `volunteers` table
- [ ] Registration processing function
- [ ] Volunteer processing function
- [ ] Confirmation email triggers
- [ ] Salesforce sync

**Email:**
- [ ] Registration confirmation template
- [ ] Volunteer welcome template

### Explicitly NOT in MVP
- User accounts (returning visitors still re-enter info)
- Waitlists and capacity enforcement
- Reminder emails (2-day and day-of)
- Hike leader self-service portal
- Calendar view
- Recurring event auto-generation
- Full party name/address collection (just party size)
- Volunteer manual digital sign-off

---

## Roadmap

### Phase 1: MVP (January–February 2025)

| Week | Milestone |
|------|-----------|
| 1 | CPT + taxonomies + meta box registered |
| 2 | Meta box UI complete, saving/loading works |
| 3 | Archive template (semantic HTML, filters) |
| 4 | Single template + registration form UI |
| 5 | Supabase tables + edge functions |
| 5 | Registration → Supabase → Resend → Salesforce |
| 6 | Volunteer page + form → Supabase flow |
| 7 | Testing with real events |
| 8 | Staff training (Paige) |
| 9 | Buffer / edge cases / launch |
| **March 1** | **Guided programs live** |

### Phase 2: Enhancement (March–May 2025)

- [ ] Reminder email system (`email_queue` + scheduled Supabase function)
- [ ] Waitlist logic + capacity enforcement
- [ ] "Sold Out" display on listings
- [ ] Hike leader registration list view (custom CRM admin or Supabase dashboard)
- [ ] Additional attendee name collection
- [ ] Calendar view option

### Phase 3: Optimization (June–December 2025)

- [ ] User accounts (recognize returning visitors by email)
- [ ] Pre-filled forms for recognized users
- [ ] Volunteer manual acknowledgment flow
- [ ] Phenology alert system (interest list + notifications)
- [ ] Volunteer stories widget (pulls from blog)
- [ ] iNaturalist/citizen science exploration

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Staff time per event setup | Reduced by 50%+ |
| Hike leader list requests to Paige | Reduced (Phase 2: zero) |
| Registration → Salesforce sync | 100% automated |
| Confirmation email delivery | 100% automated, < 1 minute |
| Volunteer signup → Salesforce | 100% automated |
| Time from signup to welcome email | < 1 minute |

---

## Stakeholders & Decisions

| Decision | Owner | Status |
|----------|-------|--------|
| Technical approach | Don | ✅ Decided: Custom build |
| Salesforce field mapping | Paige + Cinnamon/Sara | Pending |
| Event type taxonomy values | Paige | Pending |
| Volunteer interest options | Paige | Pending |
| Annual Gathering registration | Amy/Kristi | Separate scope |

---

## Open Questions

- [ ] What event types should be in taxonomy? (Guided Hike, Workshop, Science on Tap, Fundraiser, Annual Gathering, Workday, etc.)
- [ ] What preserves/locations should be in taxonomy? (Or pull from Preserves CPT?)
- [ ] Salesforce Campaign — one campaign per event, or per program type?
- [ ] Volunteer interest categories — what are the options?
- [ ] Should Annual Gathering use same system or remain separate?

---

## Appendix: Stakeholder Meeting Notes

### From Paige (Community Conservation Coordinator)

**Current frustrations:**
- Still not automated — checking multiple places for registration accuracy
- Only captures primary registrant, not full party names
- Formatting issues with Give Lively exports
- Sending lists to hike leaders is manual and time-consuming

**2026 programming plans:**
- Guided hikes (ongoing)
- Hybrid workshops (classroom/online + field)
- Pop-up phenology events (spring wildflowers, sucker migration)
- Alert list for time-sensitive natural events
- Workdays may move to website (currently email list works well)
- Science on Tap (recurring)

**Seasonal patterns:**
- Most programming announced just before spring
- Winter is limited (mainly Science on Tap)

**Event types:**
- Free and paid (guest expert hikes ~$10 fee)
- Registration required preferred
- Family-friendly vs. adult-focused
- Members-only for some events

**Volunteer page needs:**
- Separate from Contact and Give
- Automated welcome email
- Eventually: digital manual sign-off before activation
- Auto-populate Salesforce Volunteers app (currently manual via Amy)
- Position descriptions on page or downloadable
- Volunteer stories and photos
- Easy to update

---

*Document maintained by: Don*  
*Next review: Post-Phase 1 launch (March 2025)*