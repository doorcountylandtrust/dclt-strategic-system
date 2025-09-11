# GIS Integration Notes

# 🌍 GIS Integration Plan – Preserves Explorer

This document outlines how DCLT can integrate internal GIS data with the public-facing Preserves Explorer experience—without relying on Google.

---

## ✅ 1. Use Cases

| Use Case | Description | Public/Internal |
| --- | --- | --- |
| Preserve Boundaries | Show polygon overlays for each preserve | ✅ Public |
| Trail Routes | Visual trail overlays for visitors | ✅ Public |
| Conservation Layers | Priority habitats, wetlands, threatened areas | 🔒 Internal or toggleable |
| Visitor Navigation | Mobile GPS-based orientation | ✅ Public |
| Ecological Overlays | Enrich preserve storytelling | Mixed |

---

## 🗂️ 2. Data Format & Source of Truth

**Preferred file formats:**

- `.geojson` – best for frontend mapping (Leaflet-native)
- `.kml`, `.gpx` – export from GPS tools
- `.shp` – convert via QGIS or ogr2ogr
- Mapbox tilesets – optional for raster/vector layers

**Maintain a single “source of truth” folder** in Dropbox, Google Drive, or Git repo:

## 🧱 3. Frontend Tech Stack

| Tool | Purpose |
| --- | --- |
| Leaflet.js | Open-source map rendering |
| Turf.js | Geospatial filtering, measurement |
| Mapbox GL | Optional – custom styles/tiling |
| PWA Wrapper | Future phase – for mobile GPS maps |

➡️ **Recommendation:** Start with Leaflet + GeoJSON. Simple, lightweight, and mission-aligned.

---

## 🧩 4. Overlay Logic

**How the map will work:**

1. Load base map (OpenStreetMap)
2. Fetch preserve markers from WordPress (CPT)
3. When user selects a preserve:
    - Load boundary (GeoJSON)
    - Load trail overlay (optional)
    - Add as interactive layers with custom styles
4. Optional toggle: show ecological or conservation overlays

---

## 🛠️ 5. Storage & Access Options

| Storage Type | Pros | Cons |
| --- | --- | --- |
| WordPress ACF File Field | Easy for staff to manage | Not optimized for scale |
| Mapbox Tilesets | High performance + style | Paid after free tier |
| GitHub Repo (static files) | Fully controlled & versioned | Requires dev involvement |
| **Cloudflare R2 or S3** | Fast, CDN-backed, works with GIS tilesets | Setup + cost after tier
 |

➡️ **MVP Recommendation:** Upload `.geojson` files via ACF for each preserve.

---

## 🧪 6. Testing & Validation Tools

- [GeoJSON.io](https://geojson.io/) – Quick web-based editor
- [QGIS](https://qgis.org/) – Open-source GIS desktop software
- [Mapshaper](https://mapshaper.org/) – Format conversion + simplification

---

## 🎨 7. Design Integration Tips

- Match trail/boundary lines to brand (e.g. linocut style)
- Use subtle animations or layer fades
- Add hover/tooltip info for trail names or habitat features
- Only show legends if overlays become complex

---

## 📅 8. Phased Implementation Timeline

| Phase | Features Included |
| --- | --- |
| Phase 1 | Preserve boundaries + trail routes (GeoJSON) |
| Phase 2 | Styled base map, habitat overlays, mobile support |
| Phase 3 | GPS-based navigation, offline access, live alerts |

---

## ✅ Next Steps

- [ ]  Identify 1–2 preserves for pilot overlays
- [ ]  Export boundary + trail overlays as `.geojson`
- [ ]  Upload sample files to ACF or shared folder
- [ ]  Prototype Leaflet map with toggleable layers
- [ ]  Design visual styles for overlays
- [ ]  Integrate into preserve detail pages via slug