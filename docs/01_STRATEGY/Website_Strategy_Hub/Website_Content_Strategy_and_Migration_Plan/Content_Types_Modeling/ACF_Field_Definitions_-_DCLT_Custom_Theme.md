---
title: "\U0001F9E9 ACF Field Definitions \u2013 DCLT Custom Theme"
project_status: in_progress
priority: high
stakeholders:
- ACF Field
- DCLT Custom
- ACF Field
- Door County
- Land Trust
tags:
- fundraising
- conservation
created_date: '2025-09-11'
last_updated: '2025-09-11'
---
# 🧩 ACF Field Definitions – DCLT Custom Theme

# ACF Field Groups - Door County Land Trust

## 1. Global Site Settings (Options Page)

**Location:** Options Page → Site Settings

### Contact & Organization

- **Organization Name** (Text)
- **Tagline** (Text)
- **Phone** (Text)
- **Email** (Email)
- **Address** (Textarea)
- **Hours** (Textarea)

### Social Media

- **Facebook URL** (URL)
- **Instagram URL** (URL)
- **Newsletter Signup URL** (URL)

### Global CTAs

- **Primary Donate Button Text** (Text) - Default: "Donate Now"
- **Primary Donate URL** (URL)
- **Membership Renewal Text** (Text) - Default: "Renew Membership"
- **Membership Renewal URL** (URL)
- **Emergency Alert** (Group)
    - Alert Active (True/False)
    - Alert Text (Text)
    - Alert Link (URL)
    - Alert Type (Select: info, warning, urgent)

### Salesforce Integration

- **Default Lead Source** (Text)
- **Salesforce Endpoint URLs** (Repeater)
    - Form Type (Select: landowner, donor, volunteer, general)
    - Endpoint URL (URL)

---

## 2. Homepage Builder

**Location:** Page Template → Homepage

### Hero Section

- **Background Type** (Radio: image, video)
- **Background Image** (Image) - Large curved hero images
- **Background Video** (File) - Optional MP4
- **Headline** (Text) - Main message
- **Subheadline** (Textarea) - Supporting text
- **Primary CTA** (Group)
    - Button Text (Text)
    - Button URL (URL)
    - Button Style (Select: primary, secondary, landowner)
- **Secondary CTA** (Group)
    - Button Text (Text)
    - Button URL (URL)
    - Button Style (Select: primary, secondary, landowner)

### Mission Statement

- **Mission Text** (Textarea)
- **Mission Image** (Image)

### Featured Preserves

- **Featured Preserve** (Post Object) - Links to preserve posts
- **Preserve Explorer CTA Text** (Text)
- **Show Preserve Stats** (True/False)

### Impact Numbers

- **Impact Stats** (Repeater)
    - Number (Text) - e.g., "2,847"
    - Label (Text) - e.g., "Acres Protected"
    - Icon (Select: acres, species, volunteers, donations)

### Ways to Help Section

- **Section Title** (Text)
- **Help Options** (Repeater)
    - Title (Text)
    - Description (Textarea)
    - Icon (Image)
    - Link URL (URL)
    - Priority (Select: primary, secondary)

---

## 3. Landowner Hub Pages

**Location:** Page Template → Landowner Pages

### Page Header

- **Page Title Override** (Text)
- **Hero Image** (Image)
- **Intro Text** (Textarea)
- **Key Benefits Summary** (Textarea)

### Protection Process

- **Process Steps** (Repeater)
    - Step Number (Number)
    - Step Title (Text)
    - Step Description (Textarea)
    - Step Image (Image)
    - Estimated Timeline (Text)

### Benefits Section

- **Benefit Categories** (Repeater)
    - Category Title (Text) - e.g., "Tax Benefits"
    - Benefits List (Repeater)
        - Benefit Text (Text)
        - Detail Link (URL) - Optional
    - Category Icon (Image)

### FAQ Section

- **Page-Specific FAQs** (Repeater)
    - Question (Text)
    - Answer (WYSIWYG)
    - Category (Select: easements, donation, selling, general)

### Resources & Downloads

- **Resource Downloads** (Repeater)
    - Resource Title (Text)
    - Resource Description (Textarea)
    - File (File) - PDF, etc.
    - Resource Type (Select: guide, form, case-study, legal)

### Contact CTAs

- **Primary Contact CTA** (Group)
    - CTA Title (Text)
    - CTA Description (Textarea)
    - Contact Method (Select: form, phone, email, meeting)
    - Salesforce Form ID (Text)
- **Secondary Resources** (Repeater)
    - Resource Title (Text)
    - Resource URL (URL)
    - Resource Type (Select: calculator, guide, external)

---

## 4. Preserve Custom Post Type

**Location:** Custom Post Type → Preserves

### Basic Information

- **Preserve Name** (Text) - Auto-fills from post title
- **Acreage** (Number)
- **County** (Select: Door County, Other)
- **Access Type** (Select: public, limited, private)
- **Difficulty Level** (Select: easy, moderate, challenging)

### Location & Access

- **Address** (Text)
- **GPS Coordinates** (Group)
    - Latitude (Text)
    - Longitude (Text)
- **Parking Information** (Textarea)
- **Access Instructions** (WYSIWYG)

### Preserve Details

- **Short Description** (Textarea) - For cards/previews
- **Full Description** (WYSIWYG)
- **Key Features** (Repeater)
    - Feature Name (Text) - e.g., "Rare orchids", "Lake frontage"
    - Feature Description (Textarea)
- **Wildlife Highlights** (Repeater)
    - Species Name (Text)
    - Description (Textarea)
    - Best Viewing Season (Select)

### Images & Media

- **Hero Image** (Image)
- **Image Gallery** (Gallery)
- **Trail Map** (Image)
- **Video Tour** (File)

### Visiting Information

- **Hours** (Text)
- **Seasonal Access** (WYSIWYG)
- **Rules & Restrictions** (WYSIWYG)
- **What to Bring** (Repeater)
    - Item (Text)
    - Required/Recommended (Select)

### Conservation Story

- **Protection Date** (Date Picker)
- **Protection Method** (Select: easement, donation, purchase)
- **Conservation Story** (WYSIWYG)
- **Donor Recognition** (Text) - If public
- **Stewardship Needs** (Textarea) - Internal use

### React App Integration

- **Preserve ID** (Text) - Links to React explorer
- **Featured in Explorer** (True/False)
- **Explorer Data Sync** (Message) - Instructions for staff

---

## 5. Story/Project Custom Post Type

**Location:** Custom Post Type → Conservation Stories

### Story Details

- **Story Type** (Select: stewardship, acquisition, volunteer, impact)
- **Related Preserve** (Post Object) - Links to preserve if applicable
- **Story Date** (Date Picker)
- **Featured Story** (True/False) - For homepage

### Content

- **Excerpt** (Textarea) - For previews
- **Story Content** (WYSIWYG)
- **Key Takeaway** (Text) - Main point for social sharing

### Media

- **Featured Image** (Image)
- **Image Gallery** (Gallery)
- **Before/After Images** (Group)
    - Before Image (Image)
    - After Image (Image)
    - Comparison Description (Text)

### Impact Metrics

- **Quantifiable Impact** (Repeater)
    - Metric Type (Select: acres, species, volunteers, funds)
    - Number (Text)
    - Description (Text)

---

## 6. Donation/Support Pages

**Location:** Page Template → Support Pages

### Donation Options

- **Donation Levels** (Repeater)
    - Amount (Text)
    - Impact Description (Text)
    - Suggested For (Text) - e.g., "Monthly supporters"

### Membership Information

- **Membership Levels** (Repeater)
    - Level Name (Text)
    - Annual Cost (Number)
    - Benefits List (Repeater)
        - Benefit (Text)
    - Member Count Goal (Number)

### Recognition

- **Donor Recognition Levels** (Repeater)
    - Recognition Level (Text)
    - Minimum Gift (Number)
    - Recognition Description (Text)

---

## 7. Global Components (Flexible Content)

### Reusable Block Types

- **Hero Section**
- **CTA Block**
- **Feature Grid**
- **FAQ Accordion**
- **Statistics Display**
- **Story Highlight**
- **Preserve Preview**
- **Contact Form**
- **Newsletter Signup**
- **Social Media Links**

### Content Block Settings

Each block includes:

- **Background Type** (Select: none, color, image)
- **Background Color** (Color Picker) - Tied to Tailwind theme
- **Container Width** (Select: narrow, content, wide, full)
- **Spacing** (Select: small, medium, large, custom)

---

## Field Group Location Rules

### Homepage Builder

- Page Template = Homepage

### Landowner Hub

- Page Template = Landowner Hub OR
- Post Taxonomy = Landowner Resources

### Preserve Fields

- Post Type = Preserves

### Story Fields

- Post Type = Conservation Stories

### Support Pages

- Page Template = Donation/Support OR
- Page Parent = Support (for child pages)

### Global Settings

- Options Page = Site Settings

---

## Additional Considerations

### Performance

- Use conditional logic to show/hide field groups based on selections
- Set up field group loading only where needed
- Consider local JSON for field sync across environments

### User Permissions

- Limit Options Page access to administrators
- Allow editors to manage content but not structure
- Create custom capabilities for preserve vs story management

### Salesforce Integration Fields

- Include hidden fields for source tracking
- Add utm parameter capture
- Set up lead scoring based on engagement type

### Accessibility

- Ensure all image fields require alt text
- Include heading level selections for proper document structure
- Add aria-label options for complex interactive elements

## Related Documents

**Cross-Referenced Documents**
- [[Volunteers]]
- [[Stewardship]]
- [[—— Content Types & Modeling]]


- [[Comms Strategy Master Hub]]
- [[2026 Budgeting]]
- [[Mission, Values & Brand Voice]]

**Thematic Alignment**
- [[Project Communication Templates]] - membership, stewardship, fu
- [[Messaging & Engagement Research]] - co
- [[Brand + Website: Executive Summary]] - co