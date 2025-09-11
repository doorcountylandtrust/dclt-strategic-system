# — Preserves Explorer

# Preserves Explorer Project Hub

## ✅ Project Purpose

Create a map-based preserve discovery tool that aligns with DCLT's mission, UX best practices, and brand identity—without reliance on Google products.

---

## 🔍 Vision Summary

- **Mission-aligned**, ethical map experience
- **Accessible** across devices and for all users
- Blends **storytelling, filtering, and spatial data**
- Scales toward PWA/mobile-first use in future

---

## 🗺️ Core Features (MVP)

- Interactive map (Leaflet + OpenStreetMap)
- Preserve detail pop-ups with images and CTAs
- Filters (by activity, accessibility, proximity, etc.)
- Mobile-responsive design
- Non-map view option (list/grid toggle)

---

## 🔄 Phase Breakdown

### Phase 1 – MVP Web Map

- Map UI & controls
- Basic filter logic
- Pull data from WordPress CPT
- Embed in Astro/Next frontend

### Phase 2 – Narrative + UX Layer

- Story-based filters
- Featured seasonal highlights
- Visitor personas (tie to Giving, Events, etc.)

### Phase 3 – App-Ready PWA

- Offline trail maps
- Location-aware navigation
- “Plan a trip” features
- Badge or stewardship tracking

---

## 🧭 Technical Options

| Tool | Purpose | Notes |
| --- | --- | --- |
| Leaflet.js | Mapping library | Lightweight, OSS |
| OpenStreetMap | Basemap tiles | Community-built |
| Mapbox | Optional tiles/styling | Custom styles |
| WordPress + ACF | Preserve content | Already in use |
| Astro (frontend) | UI rendering | Fast, modular |
| PWA (later) | Offline access, nav | Future-ready |

---

## 🗺 GIS Integration

We **can  use internal GIS** data:

- Import shapefiles or GeoJSON for preserve boundaries or trails
- Use `Leaflet.geoJSON()` or similar
- Could even expose map overlays like:
    - **Conservation priority zones**
    - **Wildlife corridors**
    - **Habitat types**
- Consider syncing a light GIS layer from your internal database

---

## 🧰 Action Items

- [ ]  Create moodboard & wireframe
- [ ]  Identify top GIS layers to expose
- [ ]  Confirm desired filters and tag taxonomy
- [ ]  Build content model for preserves
- [ ]  Choose mapping tech stack
- [ ]  Scope timeline & internal dev support

[—— Vision & Wireframes ](preserves-explorer/vision-wireframes.md)

[—— Technical Options](preserves-explorer/—— Technical Options 1f82a8cd5755803a87accab8f62b6398.md)

[—— UX Features & Filters Wishlist](preserves-explorer/—— UX Features & Filters Wishlist 1f82a8cd5755802da19cd8ec288266d0.md)

[—— Content Model (Preserve Fields, Icons, Tags)](preserves-explorer/—— Content Model (Preserve Fields, Icons, Tags)%201f82a8cd575580248957e390efdf7ef8.md)

[—— Roadmap & Phases](preserves-explorer/—— Roadmap & Phases 1f82a8cd575580e0ae3ed390269ba60b.md)

[  —— Filter Strategy & Structure](preserves-explorer/—— Filter Strategy & Structure 21e2a8cd5755802da87ed1c671326773.md)

[  —— Event and Stewardship Map Integration](preserves-explorer/—— Event and Stewardship Map Integration 21e2a8cd575580baa073c606d62f19a0.md)

[Developer Brief](preserves-explorer/Developer Brief 1f82a8cd575580a68631f3707ee12dea.md)