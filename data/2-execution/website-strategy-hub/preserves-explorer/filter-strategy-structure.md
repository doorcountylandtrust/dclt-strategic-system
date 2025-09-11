# —— Filter Strategy & Structure

This page tracks all DCLT Preserve Explorer filter types, categorization approach, and UX treatment.

### 🔖 Filter Categories Overview

| Filter | Type | Storage | Editor Control | Frontend UI |
| --- | --- | --- | --- | --- |
| Region | Taxonomy | Native WP | ✅ Add/edit | Chip + Icon |
| Activity | Taxonomy | Native WP | ✅ Add/edit | Chip + Icon |
| Ecology | Taxonomy | Native WP | ✅ Add/edit | Chip + Icon |
| Difficulty | Taxonomy | Native WP | ✅ Add/edit | Chip + Icon |
| Accessibility Features | Meta | ACF Checkbox | ❌ Code-defined | Icon Grid |
| Trail Surface | Meta | ACF Checkbox | ❌ Code-defined | Chip List |
| Facilities | Meta | ACF Checkbox | ❌ Code-defined | Icon Grid |
| Physical Challenges | Meta | ACF Checkbox | ❌ Code-defined | Text List |
| Notable Features | Meta | ACF Checkbox | ❌ Code-defined | Icon + Tooltip |
| Photography | Meta | ACF Checkbox | ❌ Code-defined | Image Icon List |
| Educational | Meta | ACF Checkbox | ❌ Code-defined | Text List |
| Wildlife Spotting | Meta | ACF Checkbox | ❌ Code-defined | Icon Grid |
| Habitat Diversity | Meta | ACF Checkbox | ❌ Code-defined | Text Badge |
| Map Features | Meta | ACF Checkbox | ❌ Code-defined | Mini Icon Map |

---

### ✅ Hybrid Model Justification

We are using:

- **Taxonomies** for dynamic, frequently changing categories that benefit from hierarchy and native WP UI.
- **Meta fields** for static, attribute-like filters that need custom UI, validation, and don’t change often.

---

### 🛠 Admin UX Enhancements

- "Copy Filters from..." dropdown to clone settings from another preserve
- Dynamic meta option manager (Settings page to control meta filter lists without code changes)

---

### 🧪 Future Enhancements

- Analytics on filter use and combinations
- User-saved presets ("Family outing," "Photographer’s picks")
- Smart default filters based on time of year / event proximity

---

### 📌 Notes

- Filter chips on the frontend will be icon-based, accessible, and toggleable
- Filter state managed via URL for shareability
- Preserve popups reflect selected filters (e.g. highlight matching features)

> Designed to balance content editor ease, technical performance, and user-centric interface clarity.
>