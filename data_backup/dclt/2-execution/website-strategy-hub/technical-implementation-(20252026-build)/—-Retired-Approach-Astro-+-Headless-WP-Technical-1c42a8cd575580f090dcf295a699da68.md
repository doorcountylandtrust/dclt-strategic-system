# — Retired Approach - Astro + Headless WP Technical Implementation

### 📛 Project Title

**Door County Land Trust: Web Redesign & Strategic Communications Revamp**

## 🔥 PURPOSE

The project modernizes the Door County Land Trust’s public presence with:

- A **redesigned, user-friendly website**
- Integrated storytelling, data, and visual hierarchy
- A **milestone-based communications strategy** tied to segmented audiences
- Robust use of **GraphQL, WordPress (headless)** and **Astro** for frontend delivery

## 🧩 TECHNOLOGY STACK

### CMS & Backend

- **WordPress** (running in Docker)
    - Custom fields for preserves (trail map image, alt text, acres, description)
    - Media library uploads (maps and images)

### Frontend

- **Astro** static site generator
- **GraphQL** via WPGraphQL plugin
- **Typescript** for type-safe data querying
- **TailwindCSS** for styling
- Uses `astro.config.mjs` proxy config to bridge between Astro and WordPress for image display

## 📂 FILE STRUCTURE SNAPSHOT

- `/astro-frontend/src/pages/preserves.astro`
- `/astro-frontend/src/lib/graphql.ts`
- `/website/docker-compose.yml`
- `/website/uploads.ini` (used to override `upload_max_filesize`)
- WordPress and MySQL Docker containers
- WPGraphQL + WPGraphiQL plugins installed

## 🧠 FUNCTIONAL GOALS

1. **Explore Preserves**
    - List of preserves with title, acreage, description, and trail map image
    - Optional alt text for accessibility
2. **Preserve Detail Pages** (planned)
    - Individual preserve pages with deeper content
3. **Segmented Calls-to-Action**
    - Dynamic based on user interest (e.g., land donor, hiker, birder, supporter)
4. **Interactive Map & Data Filters**
    - Long-term: A map-based preserve browser with filtering by activity and location

## 🧵 MESSAGING STRATEGY

1. **5 Milestones of Nonprofit Communications**
    - Inspired by the training transcript you uploaded
    - Content aligned with organizational growth, capacity, and audience maturity
2. **Targeted Personas**
    - Retiree conservationists
    - Families visiting Door County
    - Young outdoor recreation seekers
    - Local supporters/donors
3. **Storytelling**
    - “Stewardship as a journey” motif
    - Each preserve is framed as part of a larger ecological mission

## 🧰 ANALYTICS & TRACKING

- **Planned**: Google Analytics, possibly privacy-focused alternatives (e.g., Plausible)
- **Goal**: Measure engagement per preserve, per CTA, per referrer channel

## ⚙️ CURRENT OBSTACLES (solved or in-progress)

| Issue | Status |
| --- | --- |

| GraphQL working, but image `mediaItemUrl` not rendering | ✅ Solved via Astro proxy config |
| --- | --- |

| WordPress image uploads >2MB fail | ✅ Solved with `uploads.ini` override |
| --- | --- |

| User didn’t have admin rights to see WPGraphiQL | ✅ Resolved by adding `manage_options` & `administrator` role |
| --- | --- |

| Alt text not always provided in trail map uploads | ⚠️ Still requires fallback/default string |
| --- | --- |

| Astro image tag rendered but image not displaying | ✅ Solved with correct URL and proxy |
| --- | --- |

| 404 when using mediaItemUrl in Astro | ✅ Resolved with `.replace('http://localhost:8000', '')` in image URL |
| --- | --- |

| CORS/image issues | ✅ Solved via local proxying |
| --- | --- |

## ✅ CHECKLIST SUMMARY

| Feature | Status |
| --- | --- |

| Astro rendering preserve list | ✅ Working |
| --- | --- |

| WPGraphQL data fetch for `preserveFields` | ✅ Working |
| --- | --- |

| Image URLs injected via GraphQL | ✅ Working |
| --- | --- |

| Images displaying on frontend | ✅ Working via proxy |
| --- | --- |

| WPGraphQL & GraphiQL plugins installed | ✅ Working |
| --- | --- |

| Dockerized WordPress + MySQL stack | ✅ Running |
| --- | --- |

| TailwindCSS layout styling | ✅ Implemented |
| --- | --- |

| Accessibility via `altText` | ✅ Partial — fallback message needed |
| --- | --- |

| Proxy configuration in Astro | ✅ Required and implemented |
| --- | --- |

## 🔮 NEXT STEPS

1. **Refactor site structure for preserve detail pages**
2. Add **search, filtering, and map-based browsing**
3. Layer in **campaign storytelling** from milestone framework
4. Add **structured donation CTAs** per audience segment
5. Optimize images via Astro image support (`<Image />` component or similar)
6. Use Google Analytics or Plausible for engagement tracking

[—— Tech Stack & Architecture](%E2%80%94%20Retired%20Approach%20-%20Astro%20+%20Headless%20WP%20Technical%201c42a8cd575580f090dcf295a699da68/%E2%80%94%E2%80%94%20Tech%20Stack%20&%20Architecture%201c42a8cd575580d6b3b5ec4c3b2da64d.md)

## **🔐 SUSTAINABILITY & HANDOFF PLAN**

### **🧯 1. Fallback System for Continuity**

- **Goal**: Ensure public site visibility even if Astro stack breaks.
- **Plan**: Maintain a lightweight WordPress theme (GeneratePress or similar) that reads from the same ACF fields. Only needs to support preserve list view and basic pages.
- **Status**: Planned — stub out theme folder with page-preserve.php, archive-preserve.php.

---

### **📣 2. Editor Training & Visibility**

- **Last Deployed**: Add a field to the WordPress dashboard showing “Last deployed at: [timestamp]” via a custom WP widget.
- **Notion Doc**: Editor guide to explain:
    - How edits in WP become visible on the public site
    - Delay between publishing and seeing updates
    - What to do if something doesn’t show up (rebuild trigger, Slack ping)
- **Status**: In progress

---

### **🔁 3. Deployment & Rebuild Controls**

- **Trigger Button**: Add GitHub Action or Cloudflare Pages UI button to “Force rebuild site”
- **Failure Alerts**: Slack or GitHub email alerts for failed builds (coming from CI logs or webhook errors)
- **Status**: CI working; alerting not yet configured

---

### **📘 4. Developer Onboarding & Documentation**

- **README Includes**:
    - Local dev setup (Astro + WP Docker)
    - Folder structure overview
    - How the GraphQL schema maps to Astro components
    - How to modify ACF fields + see them in GraphQL
- **Code Comments**: Inline docs especially around:
    - GraphQL queries in lib/graphql.ts
    - Astro routing and getStaticPaths()
    - WP media proxy handling
- **Status**: Initial README in place; needs expansion

---

### **🛡️ 5. Low-Lift QA & Automation**

- **Automated Checks (via GitHub Actions)**:
    - ✅ Lighthouse score >90 on performance, accessibility
    - ✅ HTML syntax validation (e.g., [html-validate](https://html-validate.org/))
    - ✅ Broken image/link detection
- **Future**: axe-core integration for accessibility snapshot testing
- **Status**: Manual for now — automation planned

---

## **🧩 Decision Framework**

This project intentionally trades “WordPress-as-usual” maintainability for long-term:

- Performance (Astro + CDN)
- Creative control (Tailwind, custom markup)
- Flexibility (GraphQL queries to power any interface)

But to sustain this model, we’re mitigating risk with:

- 🔁 Fallback theme
- 📘 Clear onboarding docs
- 🔐 Visibility into build & deployment
- 🛠️ Emergency overrides

---

## **🤝 Succession-Ready Philosophy**

This site assumes a “**product mindset**,” even though it’s nonprofit-focused:

- Built to last
- Built to be handed off
- Built to be transparent and repairable

> “A good handoff isn’t just a manual—it’s a system that keeps running when the original dev is gone.”
> 

---

## **👣 Next Sustainability Steps (add to backlog)**

- Scaffold fallback WP theme layout (barebones but functional)
- Build “Last deployed at” WP dashboard widget
- Add GitHub Action or Cloudflare build trigger button
- Expand README with real-world example walkthroughs (preserve image, CTA logic, etc.)
- Add Lighthouse + HTML validation to GitHub Actions