---
title: "Donate"
description: "Support Door County's wild places. Your gift protects land, restores habitat, and keeps nature accessible for everyone."
template: page
navigation_title: "Donate"
section: give
status: draft
sme_review_needed: true
last_updated: 2024-12-11
blocks:
  - hero
  - impact-amounts
  - donation-form-embed
  - trust-signals
  - other-ways
---

<!-- 
SME FLAGS FOR CHARITABLE GIVING DIRECTOR:
- [ ] Confirm suggested amounts and impact statements
- [ ] Decide: Keep Give Lively or move to Stripe?
- [ ] Confirm form can handle: one-time/monthly toggle, tribute option, fund designation
- [ ] Which fund designations to offer? (General, Stewardship, Land Acquisition, specific campaigns?)
- [ ] Active campaigns to feature? (Camp Cuesta still active?)
- [ ] Monthly giving program name? ("Evergreen Giving" from legacy, or rename?)
-->

---

# HERO

**Headline:** Protect What You Love

**Subheadline:** Your gift keeps Door County wild — today and for generations to come.

**Background:** Nature image (forest, shoreline, or preserve landscape)

**No buttons in hero** — the form IS the action

---

# IMPACT AMOUNTS

<!-- Visual display showing what different gift levels accomplish. Not a form yet — just context before the form. -->

## Your Gift at Work

| Amount | Impact |
|--------|--------|
| **$50** | Plants 10 native trees in a restored habitat |
| **$100** | Maintains one mile of public trails for a year |
| **$250** | Funds invasive species removal on one acre |
| **$500** | Supports water quality monitoring across three preserves |
| **$1,000** | Protects one acre of critical wildlife habitat |

<!-- 
SME FLAG: These impact statements are illustrative. Need real, defensible numbers from staff.
-->

*Every gift, of any size, helps protect Door County's exceptional lands and waters.*

---

# DONATION FORM

<!-- 
This section embeds the actual form. Design notes:

FORM REQUIREMENTS:
1. Amount selector: Suggested amounts ($50, $100, $250, $500, $1,000, Other)
2. Frequency toggle: One-time / Monthly
3. Optional: Tribute (In honor of / In memory of)
4. Optional: Fund designation dropdown
5. Donor info: Name, Email, Address
6. Payment: Card / ACH
7. Single "Donate" button

MONTHLY GIVING NUDGE:
When user selects an amount, show: "Make it monthly — $25/month = $300/year of impact"

FORM SHOULD NOT:
- Require account creation
- Ask unnecessary questions
- Have multiple pages/steps if avoidable
-->

**Form embed location**

<!-- 
SME FLAG: 
- If staying with Give Lively: need single unified campaign, not 7 separate buttons
- If moving to Stripe: need developer integration estimate
- Form must be mobile-optimized
-->

---

# TRUST SIGNALS

<!-- Small, understated section below the form -->

**Your donation is tax-deductible.** Door County Land Trust is a 501(c)(3) nonprofit organization. Tax ID: 39-1561423

**Secure giving.** Your information is encrypted and never shared.

**Questions?** Call (920) 746-1359 or email giving@doorcountylandtrust.org

---

# OTHER WAYS TO GIVE

<!-- Brief links, not competing CTAs — for people who arrived here but need something else -->

Looking for other ways to support our work?

- **[Become a Member](/take-action/join-renew)** — Join our community of land protectors
- **[Give Stock](/give/ways-to-give#stock)** — Donate appreciated securities
- **[Planned Giving](/give/legacy-giving)** — Include DCLT in your estate plans
- **[Business Partnerships](/give/business-giving)** — Corporate giving opportunities
- **[Mail a Check](#mail)** — P.O. Box 65, Sturgeon Bay, WI 54235

---

# PAGE NOTES

## UX Principles Applied

1. **Single focus** — One action (donate), not seven buttons
2. **Impact first** — Show what gifts accomplish before asking
3. **Reduce friction** — Minimal fields, no account required
4. **Respect choice** — Monthly nudge, not pressure
5. **Trust signals** — Tax ID, security, contact info visible
6. **Exit paths** — Other giving options for those who need them, but not competing

## What This Replaces

The legacy page with 7 campaign buttons is replaced by:
- One smart form that handles designations
- Campaign-specific landing pages (if needed) that funnel TO this form
- A "Ways to Give" hub for complex gift types

## Technical Decisions Needed

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Payment platform | Give Lively / Stripe / other | Evaluate cost vs. features |
| Form location | Embedded vs. redirect | Embedded preferred (less friction) |
| Fund designations | Dropdown vs. separate pages | Dropdown in form, with "General" as default |
| Campaign pages | Keep separate or sunset | Sunset inactive, keep 1-2 active max |

---