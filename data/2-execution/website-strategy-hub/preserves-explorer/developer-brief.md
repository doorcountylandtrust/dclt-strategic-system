# Developer Brief

*Last updated: June 26, 2025*

> This doc summarizes finalized content, structure, and tech decisions from the strategy, UX, and GIS planning process. It’s intended for use during development of the
> 
> 
> **Preserves Explorer**
> 

## **✅ GOALS**

- Create a map-based interface to explore DCLT preserves
- Showcase preserve data from WordPress (CPT + ACF)
- Load GIS overlays (boundaries, trails, projects) without Google tools
- Implement advanced filters (activity, accessibility, difficulty, etc.)
- Embed storytelling and stewardship narratives
- Integrate preserve-based events and show them spatially
- Uphold DEIA and accessibility standards throughout

---

## **🧱 CONTENT MODEL (Preserve CPT)**

**Key ACF Fields:**

- title, slug, excerpt, description
- featured_image, photo_gallery, trail_map_file
- location (lat/lng), address, size_in_acres, date_acquired
- activities (multi-select): Hiking, Birding, etc.
- accessibility_features: ADA Parking, Paved Trail, etc.
- preserve_type, difficulty_level, trail_length
- boundary_overlay (GeoJSON)
- trail_overlays (GPX/KML)
- related_stories (relational)
- events_at_preserve (relational)
- stewardship_projects (repeater or relational CPT)
- conservation_priority_zone (boolean or taxonomy)
- featured_preserve (boolean for homepage/UI)
- hide_from_public (true/false)

➡️ See full schema: [—— Content Model (Preserve Fields, Icons, Tags)](%E2%80%94%E2%80%94%20Content%20Model%20(Preserve%20Fields,%20Icons,%20Tags)%201f82a8cd575580248957e390efdf7ef8.md)

---

## **🌍 GIS INTEGRATION**

**Data Formats:**

- .geojson for preserve boundaries, stewardship areas, and events
- .gpx or .kml for trails (optional)

**Storage:**

- GitHub repo under /data/preserves/, /data/stewardship/, /data/events/

**Frontend Rendering:**

- Use Leaflet.js
- Render boundaries/trails on hover or click
- L.geoJSON() used to render all spatial overlays
- Add optional highlight, glow, or icon changes when filters are applied

**Planned Overlays:**

- Preserve boundaries
- Trail lines (optional)
- Stewardship project zones
- Event pins or areas
- Conservation priority zones (optional phase 2)

---

## **⚙️ TECH STACK**

| **Layer** | **Tool** |
| --- | --- |
| CMS | WordPress + ACF |
| Frontend | Astro |
| Mapping | Leaflet.js |
| Storage | GitHub + Cloudflare Pages |
| GIS Authoring | QGIS or [GeoJSON.io](http://geojson.io/) |
| Data Access | REST API or WPGraphQL |

➡️ No Google Maps. Ethical, privacy-first tech stack.

---

## **🔍 FILTERS TO IMPLEMENT (PHASED)**

### **✅ Phase 1 Filters (MVP)**

- Activities (multi-select)
- Accessibility features (multi-select)
- Difficulty level (single)
- Trail length (slider)
- Region (if taxonomized)
- Ecology type

### **🧩 Phase 2 Filters (UX Layer)**

- Story-based groupings (e.g. “Peaceful Hikes”, “Best for Families”)
- Featured / seasonal highlight toggle
- Map view toggles: Events / Stewardship / Stories
- Filter memory across sessions

### **🌱 Future Filters (Phase 3+)**

- Visitor capacity or popularity level
- Conservation priority status
- DEIA lens toggle (e.g. history, interpretation, land justice overlays)
- “Plan your trip” multi-stop planner

---

## **🔄 ROADMAP – PHASES**

### **🛠 Phase 1 – MVP**

- Build Leaflet map component
- Show preserve markers (lat/lng)
- Fetch and render .geojson overlays
- Base filter logic (unstyled UI ok)
- Basic list/grid toggle
- Pull content from WordPress CPT

### **🧩 Phase 2 – Narrative + UX Enhancements**

- Curated categories & themes
- Story-based UI overlays (seasonal, editorial)
- Stewardship project overlays with hover interaction
- Visual UI refinements, iconography, transitions
- Mobile drawer for filters and map interaction

### **📱 Phase 3 – App-Ready (PWA)**

- Offline trail maps
- Location-aware trail nav / geofencing
- Badge or challenge system (gamified stewardship)
- Volunteer check-in and event tracking
- “My Preserves” saved list

---

## **📦 COMPONENT STRATEGY**

- Map: MapContainer, MapMarkers, OverlayLayer, PopupCard
- Filter bar: FilterChips, DrawerUI, LiveCountBar
- Sidebar/list: PreserveListItem, PreserveDetailCard
- Data structure: shared preserve.json model and modular GeoJSON loaders
- Icons: Tailwind-compatible SVG set for accessibility + filtering

---

## **🧪 TEST DATA**

- Use kangaroo-lake.geojson, osprey-bluff.geojson, and clay-banks.geojson
- Add at least 1 event and 1 stewardship project for visual QA
- Ensure fallback image and text are used when optional fields are missing

---

## **🧠 EDITOR UX ENHANCEMENTS**

- Add “Copy Filters From…” dropdown to streamline data entry
- Reuse meta box UI for all fields to ensure consistency
- Optional taxonomy hybrid for region, activity, ecology, difficulty
- Create admin Settings Page to manage filter terms dynamically (no code)

---

## **📌 FUTURE SCALABILITY NOTES**

- Add optional integration with iNaturalist or external trail APIs
- Build /api/events.geojson endpoint for dynamic frontend mapping
- Consider integrating map into homepage as “Explore” card or overlay
- Real-time storytelling toggles: “Then & Now”, “Land Restoration Journey”
- Expose conservation impact metrics by preserve in the future