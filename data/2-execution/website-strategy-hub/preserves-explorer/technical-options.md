# —— Technical Options

(GIS, Leaftlet, Mapbox, PWA)

# 🧪 Technical Options

## 📁 Data Storage

- GitHub-hosted `.geojson` files (recommended)
- Optional: ACF file upload for non-dev staff

## 🗺 Mapping Libraries

- **Leaflet.js** – Open source, lightweight, ideal for launch
- **Mapbox GL** – Future upgrade for custom styles, if needed

## 📡 Deployment Integration

- Cloudflare Pages for edge delivery
- GitHub Actions as CI/CD

## 📁 Overlay Types (new)

| Layer Type | Format | Notes |
| --- | --- | --- |
| Stewardship Projects | GeoJSON | Optional overlay with icon + popup |
| Event Locations | Lat/Lng or GeoJSON | Tied to event system |
| Conservation Zones | GeoJSON | Optional visibility toggle |