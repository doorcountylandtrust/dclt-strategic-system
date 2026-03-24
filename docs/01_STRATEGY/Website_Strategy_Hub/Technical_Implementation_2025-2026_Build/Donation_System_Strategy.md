---
title: Donation System Strategy
status: active
priority: high
owner: Don
stakeholders:
  - Kristi (Admin/Finance Director)
  - Development Team (Cinnamon Rossman)
  - Communications
tags:
  - donations
  - stripe
  - salesforce
  - architecture
  - website
related_docs:
  - System_Architecture.md
  - ../Website_Content_Strategy_and_Migration_Plan/Information_Architecture/Donate.md
  - ../Website_Content_Strategy_and_Migration_Plan/Wireframes_-_DCLT_Website_Redesign/Donate.md
created_date: 2026-03-23
last_updated: 2026-03-23 (Phase 1 completed, strategy doc synced with implementation)
---

# Donation System Strategy

## Context

This document captures the **operational and integration requirements** for DCLT's donation system, based on a working session with Kristi (Admin & Finance Director) on 2026-03-20. It builds on the existing System Architecture (Stripe + Supabase + Salesforce) and the Donate page IA/wireframe work.

The core question: **replacing GiveLively with a custom Stripe-powered donation flow** while maintaining (or improving) Salesforce integration and donor self-service capabilities.

### Strategic decision: Parallel migration, not a hard cutover

Kristi wants to keep GiveLively (portal, tax receipts, SF pledge scaffolding work today). Don and Cinnamon want to move toward a custom system for UX control, ACH support, and tighter integration. The resolution: **outgrow GiveLively rather than rip it out.**

- All **new donations** route through the custom Stripe flow on the DCLT website
- **Existing GiveLively recurring donors** stay on GiveLively until they naturally lapse or cancel — no forced migration
- GiveLively continues running in parallel as a shrinking legacy system
- Once the custom system has full SF sync depth (recurring records, pledges, GAU allocations) and automated tax receipts, GiveLively can be sunset
- The current recurring donor base is small, so maintaining two systems is low-overhead

**Key question for Kristi:** How many donors actually log into the GiveLively portal each year? If the answer is low, the portal concern largely resolves itself with Stripe Customer Portal + emailed receipts.

**Salesforce coexistence note:** Both systems create Contacts and Opportunities in SF. The Stripe webhook already matches on email when creating Contacts, so a donor who previously gave via GiveLively and later gives via the new form should merge cleanly — but this should be verified before launch.

---

## Current State

### What's already built

**Public donation form** (`dclt-astro-website/src/components/forms/DonationForm.tsx`):
- **Two-step flow**: Step 1 (gift details) → Step 2 (payment method + summary) *(built 2026-03-23)*
- Configurable preset amounts per intent (default: $50/$100/$250/$500; business: $250/$500/$1000/$2500) *(built 2026-03-23)*
- Monthly recurring toggle
- Tribute/memorial gifts (honor/memory type, honoree name, notification email)
- Business gift toggle with organization name field
- ~~Employer matching gift~~ — removed from form per Kristi *(2026-03-23)*
- Payment method selection: Credit/Debit Card, ACH Bank Transfer, Check by Mail, DAF/IRA *(built 2026-03-23)*
- Anonymous donation checkbox
- Cover transaction fees (+3%) checkbox
- Birthday field (optional)
- Campaign tracking via URL params (`?campaign=warner-2025`)
- Intent-based entry points (`?intent=join|renew|tribute|business`)
- Membership tier display (Member/Steward/Guardian based on amount)

**Supporting pages:**
- `/give/` — hub page with 6 giving option cards (Give Today, Give Monthly, Legacy, Business, Tribute, Join/Renew)
- `/give/business-members` — business membership pitch page
- `/give/legacy-giving` — planned giving info (Legacy Circle Challenge, bequests, trusts)
- `/thank-you` — post-donation confirmation

**Backend** (`donor-relationships-v2/supabase/functions/`):
- `create-checkout-session` — creates Stripe Checkout sessions for donations + tickets; passes all metadata (tribute, business, campaign, anonymous, etc.)
- `stripe-webhook` — handles `checkout.session.completed` + `invoice.paid` (recurring renewals); creates/updates donors + donations in Supabase; optional Salesforce sync (Contacts + Opportunities); thank-you emails via Resend; drip campaign enrollment
- `check-pledge` — records offline check pledges with Salesforce sync

**Salesforce sync** (feature-flagged via `SALESFORCE_ENABLED`):
- Creates/updates Contacts (with `DC_Donor_Source__c: 'Website donation'` on new contacts) *(added 2026-03-23)*
- Sets `DC_Account_Type__c: 'Individual / Household'` on new Accounts *(added 2026-03-23)*
- Creates Opportunities (Closed Won) with custom fields: `DC_Anonymous__c`, tribute info, birthdate
- Record Types: Donation or Membership based on gift_type
- Non-blocking — SF failures are logged but don't stop donation processing

**Stripe configuration:**
- Payment methods: **Card + ACH Direct Debit** (`us_bank_account`) *(ACH enabled 2026-03-23)*
- Webhook events: `checkout.session.completed`, `invoice.paid`, `customer.subscription.deleted`
- Billing address: required
- Phone: collected
- Currency: USD
- Membership minimum: $50

**Recurring gift lifecycle** *(built 2026-03-24)*:
- `checkout.session.completed` (monthly) → creates `npe03__Recurring_Donation__c` in SF + `recurring_donations` row in Supabase
- `invoice.paid` (renewal) → creates new Opportunity linked to existing Recurring Donation
- `customer.subscription.deleted` → closes RD in both SF and Supabase
- Full field mapping: `Salesforce_Field_Mapping.md` (same directory)

### What GiveLively still provides (not yet replaced)
- Donor portal — login, giving history, year-end tax receipts
- GiveLively NPSP package manages:
  - GAU Allocations (e.g., "renewing member dues")
  - Future pledges for recurring gifts
- ~~Recurring Donation records in SF~~ *(now handled by custom system, 2026-03-24)*

### Pain points with GiveLively
- **Cancellation sync is broken**: If a donor cancels in GiveLively, it does NOT remove pledges in Salesforce or update their member status (e.g., from "renewer")
- Limited control over form UX and branding
- No ACH payment option
- Separate system to maintain outside the website

---

## Changes from Kristi Meeting (2026-03-20)

### UX changes to existing form
| Change | Current State | Kristi's Request |
|--------|--------------|------------------|
| **Multi-step form** | Single page → Stripe Checkout redirect | Split into Page 1 (what) → Page 2 (how) |
| **ACH payments** | Not available | Add via Stripe (`us_bank_account`) |
| **Employer match** | Expandable section in form | Remove from form; mention in post-donation email |
| **Business presets** | Same amounts as individual | Different preset amounts for business entry |
| **DAF flow** | Info text directing offline | Already works — consider adding intake form to capture intent |

### Salesforce sync enhancements needed
| Data Point | Current State | What's Needed |
|------------|--------------|---------------|
| Stripe transaction ID | Stored in donation `notes` field | Map to proper SF field (Payment_Number__c or custom) |
| GL identifier | Not synced | Add to Opportunity (for accounting exports) |
| GAU Allocations | Not built | Map gift types → GAUs (e.g., membership → "renewing member dues") |
| Recurring Donation record | Not created in SF | Create `npe03__Recurring_Donation__c` mirroring Stripe subscription |
| Future pledges | Not created | Auto-create pledged Opportunities for upcoming months |
| Payment method type | Not synced | Add Credit/ACH/DAF/Check to Opportunity |
| Check number | Not synced | Add to Opportunity for offline gifts |

### New capabilities needed
| Feature | Priority | Notes |
|---------|----------|-------|
| Two-way cancellation sync | Critical | SF cancel → Stripe cancel (and vice versa) |
| Donor self-service | High | Update card, cancel recurring, view history |
| Year-end tax receipts | Medium | Automated via Supabase/Resend |
| Business membership tiers | Medium | Different amounts, SF Account linking |

---

## Multi-Step Form Design

### Page 1 — What they're giving
- Donation amount (preset + custom) — presets change for business entry
- Frequency: One-time or Monthly
- Memorial/tribute toggle + honoree name + notification email
- "This gift is from a business or organization" toggle + org name field
- Anonymous giving checkbox
- Cover transaction fees checkbox

### Page 2 — How they're giving
- Payment method selection:
  - Credit/debit card (Stripe Checkout)
  - ACH bank transfer (Stripe Checkout with `us_bank_account`)
  - DAF — skips Stripe, shows EIN/instructions + optional intake form
  - Check — existing check-pledge flow
- Donor info fields (name, email, address)
- Submit → Stripe Checkout (or check-pledge/DAF flow)

**Implementation note:** The existing `DonationForm.tsx` has all the field logic already. The refactor is primarily a UI restructure — splitting the single form into two visual steps, not rebuilding field logic.

---

## Salesforce Integration Requirements

### What must sync from Stripe/Supabase to Salesforce

| Data Point | SF Object | SF Field | Notes |
|------------|-----------|----------|-------|
| Donation amount | Opportunity | Amount | Per transaction |
| Stripe transaction ID | Opportunity | Payment_Number__c or custom | Kristi needs this for reconciliation |
| Payment method | Opportunity | Payment_Method__c | Credit, ACH, DAF, Check |
| Check number (if applicable) | Opportunity | Check_Number__c | For offline gifts |
| GL identifier | Opportunity | GL_Code__c or similar | Accounting integration — review existing SF fields |
| Recurring gift setup | npe03__Recurring_Donation__c | Multiple fields | Mirrors Stripe subscription |
| GAU Allocation | Allocation__c | GAU__c | e.g., "renewing member dues" — assigned per gift type |
| Future recurring pledges | Opportunity | StageName = Pledged | Auto-created for upcoming months |
| Anonymous flag | Opportunity | DC_Anonymous__c | Already synced |
| Tribute/memorial | Opportunity | NPSP tribute fields | Already synced |
| Business name | Account or Opportunity | Organization_Name__c | Business memberships |

### Field audit needed
- [ ] Review existing Opportunity custom fields in SF for GL identifiers
- [ ] Confirm field names for payment number, check number
- [ ] Map GAU allocation logic — which gift types map to which GAUs
- [ ] Confirm how business memberships are handled (Account vs. Contact level)

---

## Recurring Gift Lifecycle (Critical)

This is the hardest integration challenge. Must handle the full lifecycle:

### Creating recurring gifts
1. Donor selects "Monthly" on form
2. Stripe creates a Subscription (already works)
3. Supabase records donation with `is_recurring: true` (already works)
4. **NEW:** SF gets Recurring Donation record + first Opportunity + future pledged Opportunities
5. **NEW:** GAU allocation applied to each

### Processing renewals
1. Stripe fires `invoice.paid` webhook (already works)
2. Webhook creates new donation record in Supabase (already works)
3. **NEW:** SF gets new Opportunity linked to Recurring Donation + GAU allocation

### Updating payment method
- Donor needs a way to update their credit card
- Options:
  - Stripe Customer Portal (hosted by Stripe, minimal custom work)
  - Custom self-service page on DCLT website
  - Salesforce Experience Cloud portal (if building one)

### Canceling recurring gifts — TWO-WAY SYNC REQUIRED
**Donor cancels (via website/portal):**
1. Cancel Stripe subscription
2. Supabase updates recurring gift status
3. SF: Cancel Recurring Donation, remove future pledged Opportunities, update member status

**Staff cancels in Salesforce:**
1. SF trigger or flow detects cancellation
2. Calls Supabase edge function or direct Stripe API
3. Stripe subscription canceled
4. Supabase updated

This two-way sync was the #1 pain point with GiveLively.

---

## Donor Self-Service: The GiveLively Gap

GiveLively's donor portal provides:
- Login + view all giving history
- Year-end tax receipt generation
- Update payment method
- Cancel recurring gifts

### Options to replace this

| Option | Pros | Cons |
|--------|------|------|
| **Stripe Customer Portal** | Built-in, minimal dev work, handles payment updates + cancellations | Limited branding, no giving history view, no tax receipts |
| **Custom portal on DCLT website** | Full control, branded, could show giving history from Supabase | Significant dev effort, security responsibility |
| **Salesforce Experience Cloud** | Full CRM data, could show everything | Licensing cost, separate URL/branding, implementation complexity |
| **Hybrid: Stripe Portal + email receipts** | Low effort for payment management, auto-receipts via Resend | No single "donor dashboard" — distributed experience |

### Recommendation (to discuss)
Start with **Stripe Customer Portal** for payment management + a **year-end tax receipt email** automated via Supabase/Resend. Defer a full donor dashboard until there's clear demand. This covers Kristi's operational needs without a large portal build.

---

## Kristi's Reporting Needs

### Current reporting sources
- **Stripe dashboard** — recurring gift information, transaction details
- **GiveLively admin** — custom question responses
- **Salesforce** — Opportunities, Recurring Donations, Allocations, Pledges

### What the new system needs to provide
- Stripe transaction IDs on every SF Opportunity (for reconciliation)
- GL identifiers on Opportunities (for accounting exports)
- Clear recurring vs. one-time distinction
- GAU allocations applied consistently
- Ability to see future recurring gift schedule (pledges)

---

## DAF (Donor-Advised Fund) Flow

The existing form already handles DAF by showing offline instructions (EIN: 39-1561423, mailing address, phone). Enhancements to consider:

1. Add optional intake form: donor name, fund provider, expected amount, expected date
2. Store as "pending DAF" in Supabase so Kristi can watch for incoming funds
3. Manual reconciliation when funds arrive
4. No Stripe involvement — this flow is purely informational + tracking

---

## Business Membership Flow

**Already built:** Business gift toggle with organization name field, intent-based entry (`?intent=business`, SF Campaign ID: `701Vo00000vtXk6IAE`), and a `/give/business-members` pitch page.

**Still needed:**
- Different preset donation amounts when business toggle is active
- SF: create or link to Account record (not just Contact)
- Business membership tier definitions from Kristi

### Open questions
- What are the business membership tiers and amounts?
- Does the `/give/business-members` page need to link directly to `/donate?intent=business` with business-specific amounts?

---

## Open Questions

### Architecture
- [ ] Stripe Customer Portal vs. custom portal vs. SF Experience Cloud — which path for donor self-service?
- [ ] Two-way SF sync mechanism — SF Flow calling a webhook? Scheduled sync?
- [ ] ACH setup in Stripe — any special account configuration needed?

### Salesforce
- [ ] Audit Opportunity custom fields for GL, payment number, check number
- [ ] Map GAU allocation rules by gift type
- [ ] How are business memberships currently structured in SF?
- [ ] What SF automations exist today for member status changes?

### UX
- [ ] Business membership tiers and preset amounts
- [ ] DAF intake form fields — what does Kristi want captured?
- [ ] Post-donation email content — include employer match info here?

### Operations
- [ ] Year-end tax receipt process — automated or manual today?
- [ ] Who handles DAF reconciliation when funds arrive?
- [ ] Training plan for Kristi on new system vs. GiveLively

---

## Implementation Phases

### Phase 1: Form UX + ACH — Ship the new donation entry point ✅ (2026-03-23)
GiveLively stays running. All new website donations route through the custom form.
- [x] Restructure `DonationForm.tsx` into two-step flow (what → how)
- [x] Add ACH (`us_bank_account`) to Stripe checkout payment methods in `create-checkout-session`
- [x] Remove employer match section from form
- [x] Make preset amounts configurable by intent/campaign (business: $250/$500/$1000/$2500)
- [x] Add `DC_Donor_Source__c` and `DC_Account_Type__c` to Salesforce sync for new contacts/accounts
- [x] ACH enabled in Stripe Dashboard + end-to-end test (verified in Supabase, Salesforce, Constant Contact)
- [ ] Move Stripe transaction ID from `notes` to proper SF Opportunity field in `stripe-webhook`
- [ ] Verify SF Contact deduplication: confirm that a donor who previously gave via GiveLively merges cleanly when they give via the new Stripe flow (match on email)
- [ ] Enable Stripe receipt emails (Dashboard toggle) for monthly renewal receipts
- [ ] Confirm business membership preset amounts with Kristi

### Phase 2: Salesforce Sync Depth — Match what GiveLively does in SF (2026-03-24)
This is what earns Kristi's trust in the new system.
- [x] Create Recurring Donation records in SF on Stripe subscription creation
- [x] Link initial + renewal Opportunities to Recurring Donation
- [x] Handle `customer.subscription.deleted` (close RD in SF + Supabase)
- [x] `recurring_donations` table in Supabase (bridges Stripe sub IDs → SF RD IDs)
- [x] Store `stripe_subscription_id` + `stripe_payment_intent_id` on donations
- [x] Fix donation confirmation email from address
- [x] Salesforce Field Mapping doc created (`Salesforce_Field_Mapping.md`)
- [ ] Create forward-pledged Opportunities for recurring gifts
- [ ] Add GAU Allocation logic by gift type
- [ ] Add GL identifier to Opportunity sync
- [ ] Add payment method type to Opportunity
- [ ] Stripe Customer Portal integration for new recurring donors (update card, cancel)

### Deferred (decided 2026-03-23)
- **Branded monthly receipt emails via Resend** — using Stripe's built-in receipt emails for now; upgrade to custom branded emails later when volume justifies it
- **Donor self-service portal** — staff handles cancellation/payment update requests for now; revisit when request volume warrants it
- **Stripe Elements (embedded payment)** — currently redirecting to Stripe Checkout; Don wants payment to feel on-site eventually; significant refactor, defer until core donation flow is stable

### Phase 3: GiveLively Sunset Prep
Only needed once the custom system has full SF parity and existing GiveLively recurring donors have largely lapsed.
- [x] Stripe `customer.subscription.deleted` webhook → SF Recurring Donation cancel + pledge cleanup *(built in Phase 2)*
- [ ] Two-way cancellation sync: SF cancel → Stripe cancel (deferred — only needed once GiveLively is gone and all recurring is on Stripe)
- [ ] Year-end tax receipt automation via Supabase/Resend (replaces GiveLively portal's tax receipt feature)
- [ ] DAF intake form (optional — capture donor intent for tracking)
- [ ] Business membership Account linking in SF
- [ ] Confirm GiveLively recurring donor count is at zero (or offer one-time migration)
- [ ] Cancel GiveLively subscription

---

## Key Files Reference

### dclt-astro-website (public site)
- `src/components/forms/DonationForm.tsx` — main donation form component
- `src/pages/donate.astro` — donate page
- `src/pages/give/index.astro` — giving hub
- `src/pages/give/business-members.astro` — business membership page
- `src/pages/give/legacy-giving.astro` — planned giving page
- `src/pages/thank-you.astro` — post-donation confirmation

### donor-relationships-v2 (backend)
- `supabase/functions/create-checkout-session/index.ts` — Stripe checkout session creation
- `supabase/functions/stripe-webhook/index.ts` — webhook handler (donation processing, SF sync, emails)
- `supabase/functions/check-pledge/index.ts` — offline check pledge recording

### dclt-strategic-system-v2 (strategy)
- `docs/01_STRATEGY/Website_Strategy_Hub/Technical_Implementation_2025-2026_Build/System_Architecture.md` — overall tech stack
- `docs/01_STRATEGY/Website_Strategy_Hub/Website_Content_Strategy_and_Migration_Plan/Information_Architecture/Donate.md` — page IA
- `docs/01_STRATEGY/Website_Strategy_Hub/Website_Content_Strategy_and_Migration_Plan/Wireframes_-_DCLT_Website_Redesign/Donate.md` — wireframe

---

## Related Documents

- [System Architecture](System_Architecture.md) — Overall tech stack and data flow
- [Donate Page IA](../Website_Content_Strategy_and_Migration_Plan/Information_Architecture/Donate.md) — Page structure and content strategy
- [Donate Page Wireframe](../Website_Content_Strategy_and_Migration_Plan/Wireframes_-_DCLT_Website_Redesign/Donate.md) — Visual layout
- [Website Functionality Wishlist](Website_Functionality_Wishlist.md) — DAF integration noted
