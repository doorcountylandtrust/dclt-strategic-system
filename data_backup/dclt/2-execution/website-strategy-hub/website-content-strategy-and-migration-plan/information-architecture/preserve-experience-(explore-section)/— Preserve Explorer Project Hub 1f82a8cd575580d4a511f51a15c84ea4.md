# — Preserve Explorer Project Hub

## **✅ Project Purpose**

Create a map-based preserve discovery tool that aligns with DCLT’s mission, accessibility goals (see ♿ section), UX best practices, and brand identity—without reliance on Google products.

---

## **🔍 Vision Summary**

- **Mission-aligned**, ethical map experience
- **Accessible** across devices and for all users
- Blends **storytelling, filtering, and spatial data**
- Scales toward PWA/mobile-first use in future
- Supports **dual exploration modes**: Map View and List View

---

## **🗺️ Core Features (MVP)**

- Interactive map (Leaflet + OpenStreetMap)
- Preserve detail pop-ups with images and CTAs (panel overlay)
- Filters (by activity, accessibility, proximity, etc.)
- Mobile-responsive design
- **List View** option for alternate browsing experience
- Users can explore preserves via either **Map View** (spatial-first) or **List View** (detail-first)

---

## **♿ Inclusive Experience Goals**

We recognize that not all members of our community can physically visit our preserves. Whether due to age, disability, geographic distance, or other factors, these individuals still deserve access to the stories, ecosystems, and meaning of these lands.

The Preserve Explorer aims to offer a **rich, dignified digital experience** that:

- Evokes the sensory beauty and serenity of each preserve
- Builds emotional connection through storytelling, photography, sound, and narrative design
- Offers accessibility features that respect different bodies, minds, and devices
- Encourages stewardship and learning for **all**, regardless of ability to be on-site

This is not just a map. It’s a **portal to belonging**—for everyone.

---

## **🔄 Phase Breakdown**

### **Phase 1 – MVP Web Map**

- Map UI & controls
- Basic filter logic
- Pull data from WordPress CPT
- Embed in Astro/Next frontend
- Panel overlay behavior for preserve detail (no page reload)
- List View layout with matching filter system

### **Phase 2 – Narrative + UX Layer**

- Story-based filters
- Featured seasonal highlights
- Visitor personas (tie to Giving, Events, etc.)
- Inclusive storytelling tools:
    - Audio descriptions
    - Visual cues and terrain previews
    - “Can’t visit?” virtual experience modes

### **Phase 3 – App-Ready PWA**

- Offline trail maps
- Location-aware navigation
- “Plan a trip” features
- Badge or stewardship tracking

---

## **🧭 Technical Options**

| **Tool** | **Purpose** | **Notes** |
| --- | --- | --- |
| Leaflet.js | Mapping library | Lightweight, OSS |
| OpenStreetMap | Basemap tiles | Community-built |
| Mapbox (optional) | Custom tile styling | Optional layer |
| WordPress + ACF | Preserve content | Already in use |
| React (frontend) | UI rendering | Fast, modular |
| PWA (later) | Offline access, nav features | Future-ready |

## **🗺 GIS Integration**

We **can use internal GIS** data:

- Import shapefiles or GeoJSON for preserve boundaries or trails
- Use Leaflet.geoJSON() or similar
- Could even expose map overlays like:
    - **Conservation priority zones**
    - **Wildlife corridors**
    - **Habitat types**
- Consider syncing a light GIS layer from your internal database

---

## **🧰 Action Items**

- Create moodboard & wireframe
- Identify top GIS layers to expose
- Confirm desired filters and tag taxonomy
- Build content model for preserves
- Choose mapping tech stack
- Scope timeline & internal dev support

---

### **UX Note: Map vs List View Modes**

- **List View** supports browsing by detail-first (facts, filters)
- **Map View** supports location-first exploration (spatial awareness, proximity)
- Panel overlay design supports in-place detail without full navigation

See full rationale in [🧠 UX + Interaction Design Decisions Log →](https://www.notion.so/your-link-here)

---

## **📎 Linked Resources**

[—— Vision & Wireframes](https://www.notion.so/1f82a8cd575580e59efbfe70b0442529?pvs=21)

[—— Technical Options](https://www.notion.so/1f82a8cd5755803a87accab8f62b6398?pvs=21)

[—— UX Features & Filters Wishlist](https://www.notion.so/1f82a8cd5755802da19cd8ec288266d0?pvs=21)

[—— Content Model (Preserve Fields, Icons, Tags)](https://www.notion.so/1f82a8cd575580248957e390efdf7ef8?pvs=21)

[—— Roadmap & Phases](https://www.notion.so/1f82a8cd575580e0ae3ed390269ba60b?pvs=21)

[—— Filter Strategy & Structure](https://www.notion.so/21e2a8cd5755802da87ed1c671326773?pvs=21)

[—— Event and Stewardship Map Integration](https://www.notion.so/21e2a8cd575580baa073c606d62f19a0?pvs=21)

[🛠 Developer Brief](https://www.notion.so/1f82a8cd575580a68631f3707ee12dea?pvs=21)

See full rationale in 

[🧠 UX + Interaction Design Decisions Log](../../../%F0%9F%A7%A0%20UX%20+%20Interaction%20Design%20Decisions%20Log%202382a8cd575580aa9dbfc85329587cca.md)