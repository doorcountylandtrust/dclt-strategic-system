---
project_id: 8
title: Preserve Explorer – Map Build
status: in_progress
priority: high
owner: Don
stakeholders:
  - Communications
  - Conservation
  - Stewardship
  - Web Development
start_date: 2025-09-20
due_date: 2026-01-15
project_type: web_component
dependencies:
  - Website Overhaul (2025–2026)
tags:
  - website
  - mapping
  - gis
  - storytelling
effort_estimate_hours: 60
budget_estimate_usd: 0
milestones:
  - date: 2025-10-15
    name: Stable React + Leaflet map component in WordPress
  - date: 2025-11-15
    name: Preserve data integrated via CPT + custom fields
  - date: 2025-12-01
    name: Event locations displayed on map
  - date: 2025-12-15
    name: Filter + live summary bar functional
  - date: 2026-01-10
    name: UX refinements (animations, list toggle, mobile testing)
---

## Summary
The Preserve Explorer is an interactive map-based tool for the new DCLT website. It will showcase preserves, trails, events, and stewardship activities in a visually engaging way. The build centers on a React + Leaflet map component embedded within WordPress. 

This task covers the **technical implementation of the map system** — data modeling, rendering, and UX features. Related storytelling, iconography, and event integration are documented elsewhere in the Website Strategy Hub.

## Goals
- Deliver a stable, performant map component that works across devices.
- Connect map markers to preserve CPT entries in WordPress.
- Support storytelling overlays: events, sub-brand icons, animated SVGs.
- Provide a fallback experience (list view, simplified map).
- Ensure maintainability: clean component structure, error handling, minimal tech debt.

## Tasks
- [ ] Finalize data schema for preserves (fields, REST API exposure).
- [ ] Implement React + Leaflet component with SSR-safe imports.
- [ ] Build dynamic map loading (maplibre/leaflet fallback).
- [ ] Integrate custom preserve icons / sub-brand art.
- [ ] Add live filter + summary bar (status, features, events).
- [ ] Add toggle for Map vs. List view.
- [ ] Implement event data overlay (upcoming + past).
- [ ] Test responsive layouts (desktop, mobile, tablet).
- [ ] Run accessibility checks (keyboard nav, color contrast).
- [ ] Document component for future devs.

## Decisions (log)
- 2025-06-04 — Switched from Astro/Headless → pure WordPress with embedded React.
- 2025-06-26 — Map to include events overlay linked to storytelling.
- 2025-07-22 — Live filter summary bar prioritized for Phase 1.
- 2025-09-22 — Animated SVG icons integrated as thematic layer.

## Risks
- Browser performance with many markers or animations.
- GIS data accuracy and sync from stewardship team.
- WordPress editor UX (field entry consistency).
- Staff training on map content updates.

## Notes
- UX comparison: Map vs. List toggle already documented in Strategy Hub.
- Consider future PWA version for offline preserve access.
- Explore analytics tracking for map interactions (heatmap, filter use).