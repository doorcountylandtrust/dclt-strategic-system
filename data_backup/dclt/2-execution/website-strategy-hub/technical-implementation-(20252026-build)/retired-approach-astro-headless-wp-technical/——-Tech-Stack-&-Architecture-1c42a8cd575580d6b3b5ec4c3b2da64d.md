# —— Tech Stack & Architecture

| **Layer** | **Tool/Platform** | **Purpose** | **Why This Choice** | **Notes** |
| --- | --- | --- | --- | --- |
| 
CMS
 | 
WordPress (Headless)
 | 
Content editing & data source
 | 
Familiar, open-source, flexible with ACF
 | 
Admin-only; not exposed to public
 |
| 
API Bridge
 | 
WPGraphQL + WPGraphQL for ACF
 | 
Structured content delivery
 | 
Flexible queries, nested relationships, strong Astro support
 | 
REST avoided due to rigidity
 |
| 
Frontend Builder
 | 
Astro
 | 
Static site generator
 | 
Fast, modern, content-focused; supports islands architecture
 | 
Pulls content at build-time
 |
| 
Component Framework
 | 
TailwindCSS (optional)
 | 
UI styling system
 | 
Utility-first, scalable design system
 | 
Could swap if custom CSS preferred
 |
| 
Source Control
 | 
GitHub
 | 
Version control & collaboration
 | 
Stable, familiar, portable
 | 
Central hub for project history
 |
| 
CI/CD
 | 
GitHub Actions
 | 
Build automation & deployments
 | 
Integrates directly with GitHub
 | 
Triggers builds on commits or webhooks
 |
| 
Hosting/CDN
 | 
Cloudflare Pages
 | 
Edge-deployed static site
 | 
Anti-DDoS, open-web ethos, portable
 | 
Serves final site from 250+ locations
 |
| 
Preview Builds
 | 
GitHub PR Previews → Cloudflare
 | 
QA before publish
 | 
Ensures approval workflow before public deployment
 | 
Manual or automated trigger options
 |
| 
Build Trigger
 | 
WP Webhooks → GitHub
 | 
Initiates build on content edits
 | 
Syncs WordPress edits with static rebuilds
 | 
Can add approval step before prod
 |
| 
Admin Experience
 | 
WordPress + ACF Blocks
 | 
Content management UI
 | 
Low-friction for non-tech users
 | 
Can document workflows for each team
 |
| 
Dev Environment
 | 
LocalWP + Astro Dev Server
 | 
Local development
 | 
Easy WP setup, fast local builds
 | 
Optionally Dockerized later
 |
| 
Content Modeling
 | 
ACF Field Groups + CPTs
 | 
Structured content types
 | 
Custom schemas for preserves, events, staff, etc.
 | 
Document field types + GraphQL mapping
 |
| 
Forms
 | 
Formstack
 | 
Custom forms & submissions
 | 
Secure, accessible, Salesforce-ready
 | 
Already integrated; DCLT standard
 |
| 
Search
 | 
Pagefind
 | 
Static site search
 | 
Lightweight, fast, privacy-respecting, static-site friendly
 | 
Pairs perfectly with Astro builds
 |
| 
Accessibility
 | 
axe-core, Lighthouse, manual QA
 | 
A11y testing & compliance
 | 
WCAG 2.1 auditing, automated + manual checks
 | 
Add GitHub CI + manual checklist, skip links, semantic HTML
 |
| 
Analytics
 | 
Plausible or Matomo (optional)
 | 
Privacy-friendly analytics
 | 
Avoids Google tracking, respects user privacy
 | 
Lightweight, self-hostable if needed
 |

Update for 20250421

I’ve already built out GraphQL queries, a preserves page, and layout components in Astro. Tailwind is working. I want to continue with:

- Dynamic route templates (e.g., /preserves/[slug].astro)
- Additional pages (About, Contact, Support)
- Light placeholder styling
- Planning for design handoff (Figma)