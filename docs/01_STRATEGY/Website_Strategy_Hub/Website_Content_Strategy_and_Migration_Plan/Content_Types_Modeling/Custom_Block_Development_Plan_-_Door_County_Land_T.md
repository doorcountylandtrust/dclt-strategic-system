---
title: Custom Block Development Plan - Door County Land Trust
project_status: in_progress
priority: high
stakeholders:
- '@apply'
- '@apply'
- '@apply'
- '@apply'
- '@apply'
tags:
- brand
- strategy
- fundraising
- conservation
created_date: '2025-09-11'
last_updated: '2025-09-11'
---
# Custom Block Development Plan - Door County Land Trust

## Block Development Priority Order

### Phase 1: Foundation Blocks (Week 1-2)

Essential blocks that establish your design patterns and enable homepage creation.

### Phase 2: Content Blocks (Week 3-4)

Specialized blocks for landowner hub and preserve content.

### Phase 3: Advanced Blocks (Week 5-6)

Complex interactive blocks and integrations.

---

## Phase 1: Foundation Blocks

### 1. Hero Block

**Purpose:** Curved design hero sections with flexible CTAs

**Usage:** Homepage, landowner pages, major landing pages

**ACF Fields:**

php

`*// Block: dclt-hero*
- background_type (radio: image, video, color)
- background_image (image)
- background_video (file) 
- background_color (color_picker) *// Tied to Tailwind theme*
- overlay_opacity (range: 0-80)
- content_alignment (select: left, center, right)
- headline (text)
- subheadline (textarea)
- primary_cta (group)
  - text (text)
  - url (url) 
  - style (select: primary, secondary, landowner, explore)
- secondary_cta (group)
  - text (text)
  - url (url)
  - style (select: primary, secondary, landowner, explore)
- container_width (select: wide, full)
- curved_bottom (true_false) *// Your signature curved design*`

**Block Template Structure:**

php

`// blocks/hero/hero.php
<section class="hero-block relative <?php echo get_field('container_width'); ?>">
    *<!-- Background Layer --><!-- Content Container with Tailwind responsive classes --><!-- CTA Buttons with your established button styles --><!-- Curved SVG bottom if enabled -->*
</section>`

### 2. CTA Block

**Purpose:** Focused call-to-action sections for conversions

**Usage:** Throughout site for landowner actions, donations, volunteering

**ACF Fields:**

php

`*// Block: dclt-cta*
- layout_style (select: centered, split, card-grid)
- background_style (select: brand-green, light-green, white, image)
- background_image (image) *// Conditional on background_style*
- icon (image)
- headline (text)
- description (textarea)
- primary_action (group)
  - text (text)
  - url (url)
  - type (select: button, form, phone, email)
  - salesforce_form_id (text) *// Conditional on type=form*
- secondary_action (group) *// Same structure*
- urgency_indicator (true_false) *// "Limited time" styling*`

### 3. Feature Grid Block

**Purpose:** Services, benefits, process steps with icons

**Usage:** Homepage features, landowner benefits, "ways to help"

**ACF Fields:**

php

`*// Block: dclt-feature-grid*
- section_title (text)
- section_subtitle (textarea)
- grid_columns (select: 2, 3, 4)
- features (repeater)
  - icon (image)
  - icon_style (select: image, brand-icon, number) *// For process steps*
  - title (text)
  - description (textarea)
  - link_url (url)
  - link_text (text)
- background_color (color_picker)
- container_width (select: narrow, content, wide)`

### 4. Stats Block

**Purpose:** Impact numbers and key metrics

**Usage:** Homepage impact, preserve statistics, annual reports

**ACF Fields:**

php

`*// Block: dclt-stats*
- layout (select: horizontal, grid, featured-large)
- background_type (select: transparent, brand, image)
- background_image (image)
- stats (repeater)
  - number (text) *// e.g., "2,847"* 
  - label (text) *// e.g., "Acres Protected"*
  - icon (select: acres, species, volunteers, donations, custom)
  - custom_icon (image) *// Conditional on icon=custom*
  - emphasis (true_false) *// Larger display*
- counter_animation (true_false) *// Count-up effect*`

---

## Phase 2: Content Blocks

### 5. FAQ Accordion Block

**Purpose:** Myth-busting content and common questions

**Usage:** Landowner hub, general FAQ pages, preserve info

**ACF Fields:**

php

`*// Block: dclt-faq*
- section_title (text)
- section_intro (textarea)
- faq_items (repeater)
  - question (text)
  - answer (wysiwyg)
  - category (select: easements, donation, selling, general)
  - featured (true_false) *// Show expanded by default*
- allow_multiple_open (true_false)
- search_filter (true_false) *// Enable FAQ search*`

### 6. Process Steps Block

**Purpose:** Step-by-step processes for landowner actions

**Usage:** Conservation easement process, donation process, getting started

**ACF Fields:**

php

`*// Block: dclt-process-steps*
- process_title (text)
- process_intro (textarea)
- layout (select: vertical, horizontal, timeline)
- steps (repeater)
  - step_number (number) *// Auto-increment option*
  - step_title (text)
  - step_description (textarea)
  - step_image (image)
  - estimated_time (text) *// "2-4 weeks"*
  - step_cta (group)
    - text (text)
    - url (url)
- next_steps_cta (group) *// Overall process CTA*`

### 7. Preserve Preview Block

**Purpose:** Bridge between WordPress and React Preserve Explorer

**Usage:** Homepage, preserve-related content

**ACF Fields:**

php

`*// Block: dclt-preserve-preview*  
- display_type (select: featured-single, grid, map-view)
- featured_preserve (post_object: preserves) *// Single preserve*
- preserve_grid (post_object: preserves, multiple) *// Multiple preserves*
- show_explorer_cta (true_false)
- explorer_cta_text (text)
- grid_columns (select: 2, 3, 4) *// For grid display*
- show_preserve_stats (true_false) *// Acreage, access type, etc.*`

### 8. Story Highlight Block

**Purpose:** Feature conservation stories and project updates

**Usage:** Homepage, story pages, preserve pages

**ACF Fields:**

php

`*// Block: dclt-story-highlight*
- layout (select: card, banner, split)
- featured_story (post_object: conservation_stories)
- manual_content (group) *// Alternative to post_object*
  - title (text)
  - excerpt (textarea)
  - image (image)
  - read_more_url (url)
- background_style (select: white, light-green, image)
- show_date (true_false)
- show_category (true_false)`

---

## Phase 3: Advanced Blocks

### 9. Contact Form Block

**Purpose:** Salesforce-integrated forms with smart routing

**Usage:** Throughout site for different contact purposes

**ACF Fields:**

php

`*// Block: dclt-contact-form*
- form_title (text)
- form_description (textarea)
- form_type (select: general, landowner, volunteer, donor)
- salesforce_endpoint (text) *// Auto-populated based on form_type*
- required_fields (checkbox: name, email, phone, organization, message, interest_type)
- custom_fields (repeater) *// Additional fields as needed*
  - field_label (text)
  - field_type (select: text, textarea, select, checkbox)
  - field_options (textarea) *// For select/checkbox*
  - field_required (true_false)
- success_message (textarea)
- redirect_url (url) *// Optional redirect after submission*
- privacy_notice (wysiwyg)`

### 10. Resource Downloads Block

**Purpose:** Guides, forms, and educational materials

**Usage:** Landowner hub, resource pages

**ACF Fields:**

php

`*// Block: dclt-resources*
- section_title (text)  
- section_intro (textarea)
- layout (select: list, grid, featured)
- resources (repeater)
  - resource_title (text)
  - resource_description (textarea)
  - resource_file (file)
  - resource_type (select: guide, form, case-study, legal, other)
  - resource_image (image) *// Thumbnail*
  - download_tracking (true_false) *// Analytics event*
- require_email (true_false) *// Gated downloads*`

### 11. Newsletter Signup Block

**Purpose:** Email list building with Salesforce integration

**Usage:** Footer, content pages, after donation

**ACF Fields:**

php

`*// Block: dclt-newsletter*
- layout (select: inline, banner, modal-trigger)
- headline (text)
- description (textarea) 
- button_text (text)
- success_message (text)
- signup_incentive (group) *// Optional lead magnet*
  - incentive_text (text)
  - incentive_file (file)
- frequency_note (text) *// "Monthly newsletter"*
- privacy_compliance (wysiwyg) *// GDPR, etc.*`

---

## Block Development Technical Approach

### 1. Block Registration Structure

php

`*// functions.php or blocks/init.php*
function dclt_register_blocks() {
    $blocks = [
        'hero',
        'cta', 
        'feature-grid',
        'stats',
        'faq',
        'process-steps',
        'preserve-preview',
        'story-highlight',
        'contact-form',
        'resources',
        'newsletter'
    ];
    
    foreach ($blocks as $block) {
        register_block_type(__DIR__ . '/blocks/' . $block);
    }
}
add_action('init', 'dclt_register_blocks');`

### 2. Shared Block Assets

**CSS Architecture:**

scss

`*// blocks/shared/block-base.scss*
.dclt-block {
  @apply relative; *// Base Tailwind classes*
  
  *// Consistent spacing system*
  &.spacing-small { @apply py-8; }
  &.spacing-medium { @apply py-16; }  
  &.spacing-large { @apply py-24; }
  
  *// Container widths matching your design tokens*
  .container-narrow { @apply max-w-3xl mx-auto px-4; }
  .container-content { @apply max-w-6xl mx-auto px-4; }
  .container-wide { @apply max-w-7xl mx-auto px-4; }
}`

### 3. Block Template Structure

php

`*// blocks/hero/block.json*
{
  "name": "dclt/hero",
  "title": "DCLT Hero Section",
  "description": "Curved hero section with CTAs",
  "category": "dclt-blocks",
  "icon": "cover-image",
  "keywords": ["hero", "banner", "cta"],
  "acf": {
    "mode": "preview",
    "renderTemplate": "hero.php"
  },
  "supports": {
    "align": ["wide", "full"],
    "anchor": true
  }
}`

### 4. JavaScript for Interactive Blocks

javascript

`*// blocks/shared/block-interactions.js// FAQ accordions, stats counters, form validation// Preserve accessibility (focus management, ARIA)// Performance optimizations (lazy loading, intersection observer)*`

---

## Block Category Organization

### Custom Block Category

php

`*// Create DCLT block category*
function dclt_block_categories($categories) {
    return array_merge($categories, [
        [
            'slug'  => 'dclt-blocks',
            'title' => 'Door County Land Trust',
            'icon'  => 'admin-site-alt3'
        ]
    ]);
}
add_filter('block_categories_all', 'dclt_block_categories');`

### Block Patterns

Create block patterns for common page layouts:

- **Landowner Landing Page Pattern** - Hero + Process Steps + CTA + FAQ
- **Preserve Page Pattern** - Hero + Story + Stats + Contact
- **Homepage Pattern** - Hero + Features + Stats + Stories + Newsletter

---

## Development Workflow

### 1. Block Development Order

1. **Hero Block** - Establish visual patterns and curved design system
2. **CTA Block** - Critical for conversions, test Salesforce integration
3. **Feature Grid** - Homepage needs, reusable component
4. **Stats Block** - Impact demonstration
5. **FAQ Block** - Landowner hub requirement
6. **Process Steps** - Landowner conversion content
7. **Preserve Preview** - React app integration
8. **Story Highlight** - Content marketing
9. **Contact Form** - Lead generation
10. **Resources** - Content organization
11. **Newsletter** - List building

### 2. Testing Strategy

- **Content Creator Testing** - Staff can easily add/edit content
- **Accessibility Testing** - Screen readers, keyboard navigation
- **Mobile Responsive** - All blocks work on mobile
- **Performance Testing** - Fast loading, optimized images
- **Salesforce Integration** - Forms submit correctly

### 3. Documentation for Staff

Create simple guides for each block showing:

- When to use this block
- How to configure settings
- Content best practices
- Examples of good usage

---

## Integration Considerations

### Salesforce Forms

- Build reusable form handler that routes to different Salesforce endpoints
- Include UTM parameter capture for source tracking
- Add progressive enhancement for JavaScript-disabled users

### Preserve Explorer Bridge

- Ensure consistent styling between WordPress and React app
- Plan for data synchronization between preserve posts and React data
- Create smooth transitions between main site and explorer

### Performance Optimization

- Lazy load images in grid blocks
- Use Intersection Observer for animation triggers
- Optimize ACF queries to avoid N+1 problems
- Implement block-level caching where appropriate

## Related Documents

**Cross-Referenced Documents**
- [[Volunteers]]
- [[—— Content Types & Modeling]]
- [[Hero]]


- [[Comms Strategy Master Hub]]
- [[2026 Budgeting]]
- [[Mission, Values & Brand Voice]]

**Thematic Alignment**
- [[Project Communication Templates]] - strategy, bra
- [[Messaging & Engagement Research]] - marketi
- [[Brand + Website: Executive Summary]] - co