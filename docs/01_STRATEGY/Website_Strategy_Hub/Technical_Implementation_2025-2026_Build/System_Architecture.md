---
title: "DCLT System Architecture"
type: strategy
status: active
updated: 2026-03-03
tags: []
---

# DCLT System Architecture

**Last Updated:** December 2024  
**Status:** Active development  
**Target Launch:** March 1, 2025 (MVP)

---

## Overview

Door County Land Trust's digital infrastructure is built on a unified architecture that separates concerns across four systems:

1. **WordPress** — Content management and public-facing display
2. **Supabase** — Operational database and business logic
3. **Resend** — Transactional and drip email
4. **Salesforce** — CRM and source of truth for constituent records

This architecture allows each system to do what it does best while maintaining a single source of truth for constituent data.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                       │
│                            (WordPress)                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   CONTENT DISPLAY              FORMS                      ADMIN             │
│   ─────────────────           ─────────────────          ──────────────     │
│   • Event listings            • Donation form ✅         • Block editor     │
│   • Event detail pages        • Registration form        • Meta boxes       │
│   • Volunteer page            • Volunteer signup         • CPT management   │
│   • Preserve pages            • Contact form             │                  │
│   • Blog/News                 • Newsletter signup        │                  │
│                                                                             │
│   Theme: Custom blocks, Tailwind CSS, PHP templates                         │
│                                                                             │
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  │ HTTPS POST (JSON)
                                  │ JavaScript fetch to Supabase endpoints
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                       │
│                            (Supabase)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   TABLES                       FUNCTIONS                  TRIGGERS          │
│   ─────────────────           ─────────────────          ──────────────     │
│   • donations ✅              • process_donation ✅      • on_donation      │
│   • registrations             • process_registration     • on_registration  │
│   • volunteers                • process_volunteer        • on_volunteer     │
│   • contacts                  • sync_to_salesforce       • on_contact       │
│   • email_queue               • send_reminder_emails     │                  │
│   • drip_campaigns            │                          │                  │
│                                                                             │
│   Auth: Anon key for public forms, service key for admin/sync               │
│                                                                             │
└───────────────┬─────────────────────────────────┬───────────────────────────┘
                │                                 │
                │ API calls                       │ API calls
                ▼                                 ▼
┌───────────────────────────────┐   ┌─────────────────────────────────────────┐
│           EMAIL               │   │                 CRM                     │
│          (Resend)             │   │             (Salesforce)                │
├───────────────────────────────┤   ├─────────────────────────────────────────┤
│                               │   │                                         │
│   TRANSACTIONAL               │   │   OBJECTS                               │
│   ─────────────────           │   │   ─────────────────                     │
│   • Donation receipts ✅      │   │   • Contact                             │
│   • Registration confirms     │   │   • Campaign                            │
│   • Volunteer welcome         │   │   • Campaign Member                     │
│   • Event reminders           │   │   • Opportunity (donations)             │
│                               │   │   • Volunteer (via Volunteers app)      │
│   DRIP CAMPAIGNS              │   │                                         │
│   ─────────────────           │   │   FIELDS WE SYNC                        │
│   • New donor series          │   │   ─────────────────                     │
│   • Volunteer onboarding      │   │   • Name, Email, Phone                  │
│   • Event follow-up           │   │   • Donor source                        │
│   • Lapsed donor re-engage    │   │   • First interaction date              │
│                               │   │   • Campaign membership                 │
│                               │   │   • Giving history                      │
│                               │   │                                         │
└───────────────────────────────┘   └─────────────────────────────────────────┘
```

---

## System Responsibilities

### WordPress

**Owns:**
- All public-facing content and display
- Content management UI for staff
- SEO, accessibility, performance
- Custom post types (Programs/Events, Preserves)
- Custom blocks and meta boxes
- Form UI (rendering, validation, submission)

**Does NOT own:**
- Data storage for submissions
- Email sending
- Salesforce synchronization
- Business logic for donations, registrations

**Key Files:**
- `/blocks/` — Custom blocks (hero, CTA, stats, feature-grid)
- `/inc/blocks/blocks-init.php` — Block registration
- `functions.php` — Theme setup
- CPTs defined in theme (TBD)

---

### Supabase

**Owns:**
- Operational database for all form submissions
- Business logic (validation, processing)
- Integration orchestration (triggers to email + CRM)
- Scheduled jobs (reminder emails)
- Admin data views (future: hike leader registration lists)

**Does NOT own:**
- Content management
- Public display
- Long-term constituent relationship history (that's Salesforce)

**Database Schema:**

```sql
-- =============================================
-- CONTACTS (unified constituent record)
-- =============================================
CREATE TABLE contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  first_name TEXT,
  last_name TEXT,
  phone TEXT,
  address_line1 TEXT,
  address_city TEXT,
  address_state TEXT,
  address_zip TEXT,
  first_interaction_date TIMESTAMPTZ DEFAULT NOW(),
  first_interaction_source TEXT, -- 'donation', 'registration', 'volunteer', 'newsletter'
  salesforce_contact_id TEXT,
  salesforce_synced_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- DONATIONS ✅ (exists)
-- =============================================
CREATE TABLE donations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID REFERENCES contacts(id),
  stripe_payment_intent_id TEXT UNIQUE,
  amount_cents INTEGER NOT NULL,
  frequency TEXT DEFAULT 'one-time', -- 'one-time', 'monthly'
  designation TEXT, -- 'general', 'land-protection', 'stewardship', etc.
  tribute_type TEXT, -- 'honor', 'memory', NULL
  tribute_name TEXT,
  status TEXT DEFAULT 'pending', -- 'pending', 'completed', 'failed', 'refunded'
  salesforce_opportunity_id TEXT,
  salesforce_synced_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- REGISTRATIONS (new)
-- =============================================
CREATE TABLE registrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID REFERENCES contacts(id),
  
  -- Event reference (WordPress post ID or slug)
  event_id TEXT NOT NULL,
  event_title TEXT NOT NULL,
  event_date DATE NOT NULL,
  
  -- Registration details
  party_size INTEGER DEFAULT 1,
  additional_attendees JSONB, -- Phase 2: [{name, email}, ...]
  notes TEXT,
  
  -- Status tracking
  status TEXT DEFAULT 'registered', -- 'registered', 'waitlist', 'cancelled', 'attended'
  
  -- Salesforce sync
  salesforce_campaign_member_id TEXT,
  salesforce_synced_at TIMESTAMPTZ,
  
  -- Emails
  confirmation_sent_at TIMESTAMPTZ,
  reminder_sent_at TIMESTAMPTZ,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- VOLUNTEERS (new)
-- =============================================
CREATE TABLE volunteers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contact_id UUID REFERENCES contacts(id),
  
  -- Volunteer details
  interests TEXT[], -- ['trail-work', 'hike-leader', 'office', 'events']
  availability TEXT, -- free text or structured
  experience TEXT,
  
  -- Status
  status TEXT DEFAULT 'new', -- 'new', 'contacted', 'active', 'inactive'
  manual_reviewed BOOLEAN DEFAULT FALSE,
  
  -- Salesforce sync
  salesforce_volunteer_id TEXT,
  salesforce_synced_at TIMESTAMPTZ,
  
  -- Emails
  welcome_email_sent_at TIMESTAMPTZ,
  
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- EMAIL QUEUE (for scheduled sends)
-- =============================================
CREATE TABLE email_queue (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  recipient_email TEXT NOT NULL,
  recipient_name TEXT,
  template_id TEXT NOT NULL, -- 'registration-reminder', 'volunteer-welcome', etc.
  template_data JSONB,
  scheduled_for TIMESTAMPTZ NOT NULL,
  sent_at TIMESTAMPTZ,
  status TEXT DEFAULT 'pending', -- 'pending', 'sent', 'failed'
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- INDEXES
-- =============================================
CREATE INDEX idx_contacts_email ON contacts(email);
CREATE INDEX idx_contacts_salesforce ON contacts(salesforce_contact_id);
CREATE INDEX idx_registrations_event ON registrations(event_id);
CREATE INDEX idx_registrations_date ON registrations(event_date);
CREATE INDEX idx_email_queue_scheduled ON email_queue(scheduled_for) WHERE status = 'pending';
```

---

### Resend

**Owns:**
- All outbound email delivery
- Email templates
- Deliverability, bounce handling

**Does NOT own:**
- Email scheduling logic (that's Supabase)
- Subscriber lists (that's Supabase + Salesforce)

**Email Templates Needed:**

| Template ID | Trigger | Content |
|-------------|---------|---------|
| `donation-receipt` | On donation complete | Thank you, amount, tax info |
| `registration-confirmation` | On registration create | Event details, what to bring |
| `registration-reminder-2day` | Scheduled, 2 days before | Event reminder, details |
| `registration-reminder-day` | Scheduled, morning of | Final reminder |
| `volunteer-welcome` | On volunteer signup | Welcome, next steps, expectations |
| `volunteer-manual-ack` | Phase 2 | Manual sign-off request |

---

### Salesforce

**Owns:**
- Long-term constituent relationship history
- Donor records and giving history
- Campaign tracking
- Volunteer management (via Volunteers app)
- Staff workflows and reporting

**Does NOT own:**
- Real-time data capture (that's Supabase)
- Email sending (that's Resend)
- Public display (that's WordPress)

**Sync Patterns:**

| Supabase Event | Salesforce Action |
|----------------|-------------------|
| New contact | Create/update Contact |
| New donation | Create Opportunity, link to Contact |
| New registration | Create Campaign Member, link to Contact + Campaign |
| New volunteer | Create Volunteer record (Volunteers app) |

**Field Mapping:** (confirm with Cinnamon/Sara)

```
Supabase contacts.email        → Salesforce Contact.Email
Supabase contacts.first_name   → Salesforce Contact.FirstName
Supabase contacts.last_name    → Salesforce Contact.LastName
Supabase contacts.phone        → Salesforce Contact.Phone
Supabase contacts.first_interaction_source → Salesforce Contact.Donor_Source__c (?)
```

---

## Data Flow Examples

### Donation Flow ✅ (Built)

```
1. User fills donation form on WordPress
2. JS submits to Stripe → payment intent created
3. On success, JS posts to Supabase edge function
4. Supabase:
   a. Find or create contact record
   b. Insert donation record
   c. Trigger: send receipt via Resend
   d. Trigger: sync to Salesforce (Contact + Opportunity)
5. User sees confirmation on WordPress
```

### Registration Flow (To Build)

```
1. User views event detail page on WordPress
2. User fills registration form
3. JS posts to Supabase edge function
4. Supabase:
   a. Find or create contact record
   b. Insert registration record
   c. Trigger: send confirmation via Resend
   d. Trigger: sync to Salesforce (Contact + Campaign Member)
   e. Queue reminder emails (2 days before, day of)
5. User sees confirmation on WordPress
```

### Volunteer Flow (To Build)

```
1. User visits Volunteer page on WordPress
2. User fills signup form
3. JS posts to Supabase edge function
4. Supabase:
   a. Find or create contact record
   b. Insert volunteer record
   c. Trigger: send welcome email via Resend
   d. Trigger: sync to Salesforce Volunteers app
   e. Notify staff (Paige) of new signup
5. User sees confirmation on WordPress
```

---

## Security Considerations

### API Keys & Access

| System | Public Access | Admin Access |
|--------|---------------|--------------|
| WordPress | Read (pages, posts, events) | WP admin login |
| Supabase | Anon key (insert only, limited tables) | Service key (server-side only) |
| Resend | None | API key (server-side only) |
| Salesforce | None | OAuth (server-side only) |
| Stripe | Publishable key (client) | Secret key (server-side only) |

### Row Level Security (Supabase)

```sql
-- Public can insert registrations, but not read others'
ALTER TABLE registrations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can register" ON registrations
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Only service role can read" ON registrations
  FOR SELECT USING (auth.role() = 'service_role');
```

---

## Implementation Phases

### Phase 1: MVP (January–February 2025)

**WordPress:**
- [ ] `dclt_program` CPT + meta boxes
- [ ] Archive template (list view, basic filters)
- [ ] Single event template
- [ ] Registration form component
- [ ] Volunteer page + form

**Supabase:**
- [ ] `contacts` table (if not exists)
- [ ] `registrations` table
- [ ] `volunteers` table
- [ ] Edge functions for form processing
- [ ] Resend integration (confirmation emails)
- [ ] Salesforce sync (Contact, Campaign Member, Volunteer)

**NOT in Phase 1:**
- Reminder emails (scheduled)
- Waitlists
- User accounts
- Hike leader portal
- Calendar view

### Phase 2: Enhancement (March–May 2025)

- [ ] Reminder email system (email_queue + scheduled function)
- [ ] Waitlist logic
- [ ] Capacity tracking / sold out display
- [ ] Hike leader registration list view
- [ ] Additional attendee name collection
- [ ] Calendar view option

### Phase 3: Optimization (June–December 2025)

- [ ] User accounts (recognize returning visitors)
- [ ] Volunteer manual acknowledgment flow
- [ ] Phenology alert system
- [ ] iNaturalist integration exploration

---

## Workstream Ownership

| Component | Chat/Workstream | Status |
|-----------|-----------------|--------|
| WordPress theme, blocks, CPT | Content/IA Chat | Active |
| Supabase schema, functions | Custom CRM Chat | Active |
| Stripe integration | Donations Chat | ✅ Complete |
| Salesforce sync | Donations Chat / CRM Chat | In Progress |
| Resend templates | CRM Chat | Active |

---

## Environment & Deployment

### WordPress
- **Dev:** Local or staging environment (your machine)
- **Prod:** TBD hosting (bring in-house from contractor)

### Supabase
- **Dev:** Supabase project (dev/staging)
- **Prod:** Same project or separate prod project

### Credentials to Manage
- [ ] Supabase anon key (public, safe for client-side)
- [ ] Supabase service key (server-side only, NEVER in client code)
- [ ] Resend API key
- [ ] Salesforce OAuth credentials
- [ ] Stripe publishable + secret keys

---

## Open Questions

- [ ] Salesforce field mapping — confirm with Cinnamon/Sara
- [ ] Volunteer signup notification — email to Paige, or Salesforce task?
- [ ] Event ID reference — use WordPress post ID, slug, or separate UUID?
- [ ] Domain ownership — resolved? Credentials secured?
- [ ] Hosting decision — where does prod WordPress live?

---

## Related Documents

- `Events_Programs_Volunteers_System_Strategy.md` — Requirements and roadmap
- `Website_IA_Map_v2.md` — Information architecture
- (Future) `Salesforce_Field_Mapping.md`
- (Future) `Email_Templates.md`

---

*Document maintained by: Don*  
*Next review: After Phase 1 launch (March 2025)*