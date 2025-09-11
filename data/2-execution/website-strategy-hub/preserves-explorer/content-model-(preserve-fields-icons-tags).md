# —— Content Model (Preserve Fields, Icons, Tags)

**Primary Goal:** Power flexible displays for each preserve while supporting filtering, storytelling, accessibility, and future GIS overlays.

> This flexible structure supports filtering, storytelling, GIS integration, accessibility, and future mobile features. Designed for use in WordPress (via ACF) and headless frontends (Astro, Next.js, etc.).
> 

---

## 🔹 Core Fields

- **Title** – Preserve name
- **Slug** – Auto-generated or custom
- **Excerpt** – One-sentence summary for cards
- **Description** – Full preserve writeup (WYSIWYG)
- **Featured Image** – Main card/hero image
- **Photo Gallery** – Optional carousel (ACF gallery)
- **Trail Map File** – Upload (PDF, GPX, KML)
- **Trail Map Image** – Optional image preview
- **Location (Lat/Lng)** – For map pin (ACF Map or number fields)
- **Address / Directions** – For mobile use
- **Size in Acres** – Display and sorting
- **Date Acquired** – Internal historical data
- **Hide from Public** – True/False toggle

---

## 🎯 Filterable Attributes

- **Activities (multi-select):**
    - Hiking
    - Birding
    - Kayaking
    - Nature Study
    - Photography
- **Accessibility Features (multi-select):**
    - ADA parking
    - Paved trail
    - Benches
    - Guide ropes
- **Preserve Type:** Forest, Wetland, Prairie, etc.
- **Difficulty Level:** Easy, Moderate, Strenuous
- **Trail Length (mi):** For filtering sliders
- **Open Year-Round:** True/False
- **Pet-Friendly:** Boolean
- **Wheelchair Accessible:** Boolean
- **Featured Preserve Tag:** Boolean or Tag
- **Visitor Capacity:** Optional (events, seasonality)

---

## 🧭 GIS-Integrated Fields (optional, scalable)

- **Boundary Overlay (GeoJSON):** Display preserve polygon
- **Trail Overlays (GPX or KML):** Render on map
- **Habitat Layers:** Tag or relational taxonomy
- **Conservation Priority:** Select field (for internal or public badges)
- **Hydrology / Soil / Ecological Layers:** Optional phase 2 overlays
- **Stewardship Projects (GeoJSON):** Optional overlay for restoration, planting, or monitoring areas. Displayed with icon + hover tooltip.
- **Conservation Priority Zone:** Align with internal land protection goals (badge or overlay)
- **Events Overlay:** Link to event system by location; show past/upcoming events with calendar icon or pulse marker.

---

## 🔁 Relational Fields

- **Related Stories** – Posts, articles, or newsletters
- **Events at Preserve** – Connect to event system
- **Nearby Preserves** – Manual or auto via Lat/Lng
- **Species Tags or Biodiversity** – Tag-based taxonomy
- **Events at Preserve:** Connects each preserve to upcoming or past events
- **Related Narratives or Stories:** Link blog posts or articles to preserve for storytelling
- **Preserve Filter Template (optional):** "Copy filters from..." dropdown to ease entry

---

## 🧩 Design & CTA Enhancements

- **Call-to-Action Text** – “Plan Your Visit” / “Volunteer Here”
- **CTA URL** – External link or internal anchor
- **Custom Background Color** – Optional theming
- **Preserve Icon or Illustration** – Custom glyph or image

---

## 🛠 Implementation Notes

- Use **ACF Repeater** for gallery or multi-trail systems
- Use **taxonomy-based filtering** on the frontend
- For **headless builds**, expose all data via REST or GraphQL
- Preserve boundaries and overlays can be rendered via **Leaflet.geoJSON()** or **Mapbox GL**
- Trail layers should follow a standardized naming and file format

---

## 📌 Future Enhancements

- Stewardship Score / Impact Tracker
- Real-time visitor conditions
- Interactive timeline of conservation history
- Badge or challenge system (for app/PWA)

[GIS Integration Notes](%E2%80%94%E2%80%94%20Content%20Model%20(Preserve%20Fields,%20Icons,%20Tags)%201f82a8cd575580248957e390efdf7ef8/GIS%20Integration%20Notes%201f82a8cd575580e0a0f9d6497a044dd4.md)

- **Stewardship Projects (GeoJSON Layer)**
    - Mark reforestation, invasive removal, habitat restoration, etc.
    - Hover popups or icon click = show date, description, partners
    - Optional filter toggle: “Show stewardship activity”
    - Layer styling: Dotted boundary, light blue fill, animated pulse?