---
title: Salesforce Field Mapping — Donation Webhook
status: active
owner: Don
created_date: 2026-03-24
last_updated: 2026-03-24
---

# Salesforce Field Mapping — Donation Webhook

What the `stripe-webhook` edge function writes to Salesforce on each donation. This is the source of truth for field names — NPSP field prefixes vary (`npe03__` vs `npsp__`) so always reference this doc, not assumptions.

**Edge function:** `donor-relationships-v2/supabase/functions/stripe-webhook/index.ts`
**SF API version:** v59.0 (hardcoded — see CLAUDE.md for migration note)
**Feature flag:** `SALESFORCE_ENABLED` secret (must be `'true'`)

---

## Contact (created for new donors)

| SF Field | Value | Notes |
|----------|-------|-------|
| `FirstName` | From Stripe checkout | |
| `LastName` | From Stripe checkout | Falls back to 'Unknown' |
| `Email` | From Stripe checkout | Used for dedup (query by email) |
| `Phone` | From Stripe checkout | |
| `MailingStreet` | line1 + line2 | Joined with newline |
| `MailingCity` | From Stripe checkout | |
| `MailingState` | From Stripe checkout | |
| `MailingPostalCode` | From Stripe checkout | |
| `MailingCountry` | From Stripe checkout | |
| `LeadSource` | `'Website'` | |
| `DC_Donor_Source__c` | `'Website donation'` | Custom field, new contacts only |
| `Birthdate` | From form (optional) | |

## Account (updated for new donors)

| SF Field | Value | Notes |
|----------|-------|-------|
| `DC_Account_Type__c` | `'Individual / Household'` | Set on auto-created Household Account |

## Opportunity (one per payment)

| SF Field | Value | Notes |
|----------|-------|-------|
| `Name` | `"{First} {Last} {Designation} {Date}"` | e.g. "John Doe General Fund 2026-03-24" |
| `AccountId` | From Contact's parent Account | |
| `npsp__Primary_Contact__c` | Contact ID | NPSP standard |
| `Amount` | Payment amount (dollars) | |
| `CloseDate` | Today's date | |
| `StageName` | `'Closed Won'` | |
| `Type` | `'Membership'` or `'Donation'` | Membership if amount >= $50 |
| `LeadSource` | `'Website'` | |
| `RecordTypeId` | `012Hp000002NUwIIAW` | Membership record type (only if membership) |
| `DC_Anonymous__c` | Boolean | From form checkbox |
| `CampaignId` | SF Campaign ID | From URL param or intent config |
| `npsp__Tribute_Type__c` | `'In Honor Of'` or `'In Memory Of'` | If tribute gift |
| `npsp__Honoree_Name__c` | Honoree name | If tribute gift |
| `npsp__Honoree_Information__c` | Notification email | If tribute gift |
| `npe03__Recurring_Donation__c` | Recurring Donation ID | If monthly — links Opp to RD |
| `Description` | Multi-line text | Includes Stripe session ID, source, designation, recurring flag |

## Recurring Donation (monthly gifts only)

Created on `checkout.session.completed` when `is_monthly=true`.

| SF Field | Value | Notes |
|----------|-------|-------|
| `npe03__Contact__c` | Contact ID | |
| `npe03__Amount__c` | Monthly amount (dollars) | |
| `npe03__Installment_Period__c` | `'Monthly'` | |
| `npe03__Date_Established__c` | Today's date | |
| `npe03__Open_Ended_Status__c` | `'Open'` | Changed to `'Closed'` on cancellation |
| `npsp__Day_of_Month__c` | Day of month (1-31) | Required by NPSP validation rule |
| `Stripe_Subscription_ID_c__c` | Stripe subscription ID | Custom field (External ID) |
| `npe03__Recurring_Donation_Campaign__c` | SF Campaign ID | If campaign provided |

### On cancellation (`customer.subscription.deleted`):

| SF Field | Value | Notes |
|----------|-------|-------|
| `npe03__Open_Ended_Status__c` | `'Closed'` | |
| `npe03__End_Date__c` | Today's date | |

---

## Supabase Tables Written

### `donors`
| Column | Source |
|--------|--------|
| `first_name`, `last_name`, `email`, `phone` | Stripe checkout |
| `address_line1/2`, `city`, `state`, `postal_code`, `country` | Stripe checkout |
| `source` | `'website'` |
| `donor_type` | `'individual'` |
| `status` | `'active'` |

### `donations`
| Column | Source |
|--------|--------|
| `donor_id` | FK to donors |
| `amount` | Payment amount |
| `donation_date` | Today |
| `designation` | From form (default: `'unrestricted'`) |
| `method` | `'online'` |
| `gift_type` | `'membership'` if >= $50, else `'donation'` |
| `is_anonymous` | From form |
| `is_recurring` | `true` if monthly |
| `stripe_subscription_id` | Stripe sub ID (monthly only) |
| `stripe_payment_intent_id` | Stripe PI ID (one-time only) |
| `tribute_type` | `'honor'` or `'memory'` |
| `honoree_name` | From form |
| `tribute_notify_email` | From form |
| `notes` | Stripe session/invoice ID |

### `recurring_donations`
| Column | Source |
|--------|--------|
| `donor_id` | FK to donors |
| `stripe_subscription_id` | Stripe subscription ID (unique) |
| `amount` | Monthly amount |
| `designation` | From form |
| `gift_type` | From form |
| `status` | `'active'` → `'cancelled'` on cancel |
| `started_at` | Today |
| `cancelled_at` | Set on cancellation |
| `sf_recurring_donation_id` | SF Recurring Donation record ID |
| `metadata` | Full Stripe checkout metadata (JSON) |

---

## Webhook Events Handled

| Stripe Event | Handler | What It Does |
|-------------|---------|-------------|
| `checkout.session.completed` | `handleDonationPayment` | Creates donor, donation, recurring_donations (if monthly), SF Contact + Opportunity + Recurring Donation |
| `invoice.paid` | `handleInvoicePaid` | Creates renewal donation, SF Opportunity linked to existing Recurring Donation |
| `customer.subscription.deleted` | `handleSubscriptionCancelled` | Updates recurring_donations status, closes SF Recurring Donation |

---

## Email

| Email | From | Trigger |
|-------|------|---------|
| Donation thank-you | `donate@doorcountylandtrust.org` | On `checkout.session.completed` (if `AUTO_THANK_YOU_ENABLED=true`) |
| Monthly renewal thank-you | `donate@doorcountylandtrust.org` | On `invoice.paid` (if `AUTO_THANK_YOU_ENABLED=true`) |

---

## Supabase Secrets Required

| Secret | Purpose |
|--------|---------|
| `STRIPE_SECRET_KEY` | Stripe API key (`sk_test_` or `sk_live_`) |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret (`whsec_`) — must match the active endpoint |
| `SALESFORCE_ENABLED` | `'true'` to enable SF sync |
| `SALESFORCE_CLIENT_ID` | SF Connected App ID |
| `SALESFORCE_USERNAME` | SF API user |
| `SALESFORCE_PRIVATE_KEY` | PEM key for JWT auth |
| `SALESFORCE_LOGIN_URL` | `https://login.salesforce.com` |
| `RESEND_API_KEY` | Resend email API key |
| `AUTO_THANK_YOU_ENABLED` | `'true'` to send confirmation emails |
| `DCLT_SECRET_KEY` | Supabase service role key |

---

## NPSP Field Prefix Guide

DCLT's Salesforce org uses mixed NPSP prefixes. Always verify field names in SF Object Manager before coding.

| Object | Common Prefix | Example |
|--------|--------------|---------|
| Recurring Donation fields | `npe03__` | `npe03__Amount__c`, `npe03__Contact__c` |
| Recurring Donation (some fields) | `npsp__` | `npsp__Day_of_Month__c` |
| Opportunity tribute fields | `npsp__` | `npsp__Tribute_Type__c` |
| Opportunity RD lookup | `npe03__` | `npe03__Recurring_Donation__c` |
| Custom DCLT fields | `DC_` | `DC_Anonymous__c`, `DC_Account_Type__c` |
| Custom one-off fields | No prefix | `Stripe_Subscription_ID_c__c` |
