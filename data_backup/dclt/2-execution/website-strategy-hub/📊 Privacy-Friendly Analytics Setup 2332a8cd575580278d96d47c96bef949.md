# 📊 Privacy-Friendly Analytics Setup

*This page documents the tracking configuration, event structure, goals, and reporting practices for the Door County Land Trust website and campaign ecosystem.*

This guide outlines our approach to website analytics that protects user privacy while still giving us actionable insight into how people use our site and engage with content.

### **🔒 Why We’re Not Using Google Analytics**

While Google Analytics (GA4) is a powerful tool, it:

- Collects more user data than we need
- Raises privacy and consent concerns
- Conflicts with our values of transparency and community trust
- Adds technical and legal complexity (e.g. cookie consent banners)

Instead, we are implementing **privacy-first analytics** using [Plausible](https://plausible.io/) or [Fathom](https://usefathom.com/), which offer:

- No cookies or fingerprinting
- No personal data collection
- Simple, focused dashboards
- Full GDPR, PECR, and CCPA compliance
- Easy setup with our WordPress stack

---

## **✅ Goals of Our Analytics Strategy**

- **Respect visitor privacy** while still learning what’s working
- **Track content performance** (pages, events, campaigns)
- **Evaluate user flows** on priority pages (e.g. Preserve Explorer, donation funnel)
- **Identify referrers** (e.g. newsletters, social media, Google)
- **Measure key conversions** (e.g. form submissions, email signups, donations)

---

## **🛠 Recommended Tool:**

## **Plausible Analytics**

**Plausible** is lightweight, open-source, and ideal for mission-driven websites.

### **🔧 Setup Steps**

1. **Create Account**
    - Go to [plausible.io](https://plausible.io/)
    - Sign up with DCLT’s analytics email (e.g. analytics@doorcountylandtrust.org)
2. **Add Website**
    - Enter our main site URL
    - Choose “Enable event goals” during setup
3. **Install Tracking Script**
    - Add the JavaScript snippet to the WordPress head (use a header/footer plugin or your custom theme)
    - OR use the official WordPress plugin
4. **Verify Tracking**
    - Visit the site in an incognito window
    - Confirm in real-time dashboard that your visit is tracked

---

## **🎯 Suggested Event Goals to Track**

| **Goal** | **Method** | **Notes** |
| --- | --- | --- |
| **Newsletter Signup** | Button click or form submission | Class or ID-based trigger |
| **Donation Start / Complete** | URL-based or JavaScript event | Use /donate/thank-you or Stripe redirect |
| **Volunteer Interest** | Form submission | Identify via Formstack, GiveLively, or WPForms |
| **Preserve Map Click** | Custom event | Use JS event hook if React-based |

## **📈 Access + Dashboards**

- **Live Dashboard**: https://plausible.io/doorcountylandtrust.org
- **User Access**: Shared with Comms, Dev, and Board Liaison teams
- **Custom Dashboards**: We can embed views into:
    - Internal Notion pages
    - Executive summaries
    - Campaign wrap-ups

---

## **💡 Advanced Features to Explore Later**

- **UTM tracking** for email and social
- **Funnel reporting**
- **API integration** for dashboard automation
- **Self-hosted option** (if privacy stakes ever increase)