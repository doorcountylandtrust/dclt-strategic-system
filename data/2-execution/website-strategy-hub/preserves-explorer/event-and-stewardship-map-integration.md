# —— Event and Stewardship Map Integration

## 🎯 Purpose

Design and implement a system that integrates **events** and **stewardship projects** into the Preserve Explorer map, enhancing storytelling, relevance, and community engagement.

---

## 📌 Use Cases

### 🗓️ Events

- Public walks, talks, or volunteer days at specific preserves
- Display past and future events contextually on the map
- Tie into Event system (e.g. Custom Post Type or integration)

### 🌱 Stewardship Projects

- On-the-ground work (e.g., invasive removal, planting)
- Show location-based context for conservation efforts
- Educate visitors on why this preserve matters now

---

## 🧩 System Components

### 1. **Data Storage**

- Event Post Type
    - Fields: Date, Title, Preserve (relational), Location (optional), Description, Image
- Stewardship Activity Post Type (or Repeater Field)
    - Fields: Title, Date Range, Preserve, GeoJSON or static point, Type (e.g., planting)

### 2. **Frontend Display**

- Toggleable layers for Events and Stewardship
- Hover / click = popup with key info (title, date, CTA)
- Dynamic badges or icon overlays (e.g., shovel, leaf)
- Events integrated into popup of Preserve if relevant
- Optional: Events panel toggle in UI like filters

### 3. **Filter Integration**

- Map toggle for events/stewardship on/off
- Optional filters:
    - "Preserves with upcoming events"
    - "Preserves with active restoration"

---

## 🧠 Design Principles

- Prioritize clarity and context
- Events/stewardship should enhance—not overwhelm—the preserve experience
- Accessibility-minded (screen reader-friendly, color contrast)

---

## 🧰 Technical Notes

- Can use Leaflet layer groups to toggle these dynamically
- Consider lazy-loading events and stewardship based on viewport
- REST API endpoints can expose Event + Stewardship data
- GeoJSON hoverable areas for project locations (like overlays)

---

## ✨ Future Ideas

- Stewardship Timelines: interactive view of a preserve’s progress
- Volunteer Badging / Recognition
- Add photos/testimonials from past events
- Layer events by theme (e.g., birding vs. trail work)
- Stewardship "stories" with mini-narrative modal popups

---