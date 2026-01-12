**Marketing Automation Evaluation & Recommendation

Door County Land Trust — January 2026**

Purpose of This Review

Leadership asked for an evaluation of:
	•	Pardot (Salesforce Marketing Cloud Account Engagement)
	•	HubSpot
	•	Other tools that could help us:
	•	Segment members / donors / prospects
	•	Automate membership renewals
	•	Improve email workflows
	•	Integrate cleanly with Salesforce

This document summarizes findings and presents a best-practice recommendation for DCLT.

⸻

1. The Reality of Enterprise Marketing Tools

Pardot
	•	Cost: $15,000–$180,000 per year
	•	Built for B2B lead scoring, not nonprofits
	•	Heavy setup burden and ongoing maintenance
	•	Does not replace Salesforce; adds a second major system
	•	Overkill for our needs (and our team size)

Conclusion:
Not appropriate for DCLT. Too costly and not aligned with our workflows.

⸻

HubSpot
	•	Nonprofit discount available, but automation + segmentation require higher tiers
	•	Strong email/marketing features
	•	Would create two CRMs (HubSpot + Salesforce), leading to confusion and duplication
	•	Salesforce integration exists but is complex and requires tech upkeep

Conclusion:
Not recommended. Creates parallel systems, increases complexity, and duplicates work.

⸻

2. The Tools We Already Have

DCLT currently operates on:
	•	Salesforce NPSP — official donor database
	•	Constant Contact — mass email delivery
	•	Website forms — intake of newsletters, event sign-ups, and new donors

This is already a valid best-practice stack for a conservation nonprofit.

The weaknesses are not the tools — they are:
	•	Broken or incomplete Salesforce ↔ Constant Contact sync
	•	Lack of automated renewal workflows
	•	No clean way to capture new newsletter signups on our website
	•	Manual segmentation instead of rule-based segmentation

These are fixable without adding a new platform.

⸻

3. What Best-Practice Looks Like for an Organization Our Size

Best-practice for a midsize conservation nonprofit is:

(1) Salesforce stays the system of record

Where donor history, memberships, and household data live.

(2) Constant Contact remains the mass email tool

Where newsletters, announcements, and large sends are managed.

(3) A lightweight automation layer handles the logic

Membership reminders, welcome sequences, segmentation rules —
not additional big platforms.

(4) Reliable sync between systems

Email updates, opt-outs, new donors, and new prospects must move cleanly between tools.

This produces:
	•	Fewer vendors
	•	Lower costs
	•	Less staff training
	•	Higher reliability
	•	A simpler, more accountable system

⸻

4. What DCLT Actually Needs

Instead of new software, the needs are:

A. Fix the Salesforce ↔ Constant Contact sync

The current Zapier integration fails in:
	•	Email updates
	•	List assignments
	•	Opt-outs

These can be rebuilt using:
	•	Direct API sync
	•	Simpler triggers
	•	Clearer segmentation rules

This removes dependence on expensive per-hour consultant fixes.

⸻

B. Add a proper newsletter signup pipeline

Our new website should send signups to:
	•	Salesforce (as Prospects)
	•	Constant Contact (newsletter list)
	•	Internal reporting (for visibility)

This is standard nonprofit practice.

⸻

C. Build automated membership renewal workflows

Salesforce can already:
	•	Track renewal dates
	•	Determine “Current vs Lapsed” members
	•	Trigger renewal reminders

We simply need to:
	•	Connect reminders to a clean workflow
	•	Ensure they deliver through Constant Contact
	•	Close the loop automatically

⸻

D. Establish clear segmentation rules

(Examples)
	•	Current Members
	•	Lapsed Members
	•	Donors but not Members
	•	Prospects with no giving yet
	•	Event participants
	•	Volunteers

Segments should be defined once in Salesforce and synced downstream.

⸻

E. Document the system

Documentation reduces risk and builds organizational continuity:
	•	Data flow
	•	Integration points
	•	How emails are triggered
	•	How segments work
	•	Where lists live
	•	How staff should update records

This ensures clarity regardless of turnover.

⸻

5. Why We Should Not Adopt Pardot or HubSpot

They solve a different problem than the ones we actually have.

Our issues are:
	•	Broken sync
	•	Lack of automation
	•	No web-to-CRM pipeline
	•	Poor segmentation hygiene

Pardot/HubSpot would:
	•	Add a second CRM
	•	Require more staff expertise
	•	Increase vendor dependence
	•	Multiply complexity
	•	Cost significantly more than fixing what we have

The return on investment is simply not there.

⸻

6. Recommended Path Forward

This is the best-practice strategy tailored for DCLT.

Phase 1 — Stabilize the Foundations (High Priority)
	•	Fix Salesforce ↔ Constant Contact sync
	•	Add website newsletter signup
	•	Create clear segmentation rules

Phase 2 — Automate Membership Renewals
	•	Build date-based renewal logic in Salesforce
	•	Deliver reminders via Constant Contact
	•	Track outcomes in Salesforce

Phase 3 — Implement Drip & Stewardship Workflows
	•	New donor welcome series
	•	New member welcome series
	•	Event follow-ups
	•	Prospect nurturing

Delivered via Constant Contact, triggered via CRM logic.

Phase 4 — Document the System
	•	Architecture diagram
	•	Segment definitions
	•	Data flow
	•	Staff instructions
	•	Maintenance playbook

⸻

7. Budget Considerations

Cost of Pardot: $15,000–$180,000 annually

Cost of HubSpot: $5,000–$20,000 annually (after discounts)

Cost to repair and automate our existing system:

Dramatically lower — mostly staff time, minimal vendor fees.

This preserves resources for:
	•	Stewardship
	•	Land acquisition
	•	Membership growth
	•	Development
	•	Communications

⸻

8. Final Recommendation

Do not adopt Pardot or HubSpot.

Instead, follow the roadmap:
	•	Strengthen Salesforce + Constant Contact
	•	Fix the sync
	•	Add web-to-CRM pipelines
	•	Build renewals automation
	•	Document everything

This approach:
	•	Uses tools we already pay for
	•	Reduces complexity
	•	Avoids expensive platforms
	•	Improves internal clarity
	•	Supports long-term organizational stability

This is the most cost-effective, sustainable, and best-practice direction for DCLT.