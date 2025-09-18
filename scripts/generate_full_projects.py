#!/usr/bin/env python3
import os
import frontmatter
from datetime import date

# Root directories
PROJECTS_ROOT = "data/dclt/02_EXECUTION/10_Projects"
OUTPUT_DIR = os.path.join(PROJECTS_ROOT, "dashboards")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Frontmatter helper
def make_frontmatter(id, title, status, priority, start, end, notes, parent=None):
    fm = f"""---
project_id: {id}
title: {title}
start_date: {start}
end_date: {end}
status: {status}
priority: {priority}
notes: {notes}
created_date: {date.today()}
"""
    if parent:
        fm += f"parent_project_id: {parent}\n"
    fm += "---\n"
    return fm

# Example projects + subtasks (trim or expand as needed)
PROJECTS = [
    {
        "id": "001",
        "title": "Brand System (2026)",
        "status": "active",
        "priority": "high",
        "start_date": "2025-09-01",
        "end_date": "2026-05-30",
        "notes": "Major rebrand initiative, includes logo + moodboards.",
        "subtasks": [
            ("001a", "Moodboard Evaluation", "completed"),
            ("001b", "Logo Draft Round 1", "in-progress"),
            ("001c", "Focus Group Analysis", "planning"),
        ]
    },
    {
        "id": "002",
        "title": "Website Overhaul (2025–2026)",
        "status": "active",
        "priority": "high",
        "start_date": "2025-07-01",
        "end_date": "2026-02-28",
        "notes": "Full redesign including Preserve Explorer and content migration.",
        "subtasks": [
            ("002a", "Wireframes - Homepage", "completed"),
            ("002b", "Preserve Explorer Map Build", "in-progress"),
            ("002c", "Content Migration Plan", "planning"),
        ]
    },
]

# -------------------------------
# Step 1: Generate project + subtask files
# -------------------------------
for project in PROJECTS:
    proj_dir = os.path.join(PROJECTS_ROOT, project["title"].replace(" ", "_").replace("–", "-"))
    os.makedirs(proj_dir, exist_ok=True)

    # Project file
    proj_file = os.path.join(proj_dir, f"{project['title'].replace(' ', '_')}.md")
    if not os.path.exists(proj_file):
        with open(proj_file, "w") as f:
            f.write(make_frontmatter(
                project["id"],
                project["title"],
                project["status"],
                project["priority"],
                project["start_date"],
                project["end_date"],
                project["notes"]
            ))
            f.write("\n# " + project["title"] + "\n\n")
            f.write(project["notes"] + "\n")

    # Subtasks
    subtasks_dir = os.path.join(proj_dir, "subtasks")
    os.makedirs(subtasks_dir, exist_ok=True)

    for sid, stitle, sstatus in project["subtasks"]:
        sub_file = os.path.join(subtasks_dir, f"{stitle.replace(' ', '_')}.md")
        if not os.path.exists(sub_file):
            with open(sub_file, "w") as f:
                f.write(make_frontmatter(
                    sid,
                    stitle,
                    sstatus,
                    "medium",
                    "TBD",
                    "TBD",
                    f"Subtask of {project['title']}",
                    parent=project["id"]
                ))
                f.write("\n# " + stitle + "\n\n")
                f.write(f"Linked to parent project: {project['title']} ({project['id']})\n")

# -------------------------------
# Step 2: Generate HTML dashboard
# -------------------------------
rows = []
for root, _, files in os.walk(PROJECTS_ROOT):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                post = frontmatter.load(f)
                meta = post.metadata
                title = meta.get("title", file)
                status = meta.get("status", "unknown")
                priority = meta.get("priority", "unknown")
                start = meta.get("start_date", "")
                end = meta.get("end_date", "")
                notes = meta.get("notes", "")
                parent = meta.get("parent_project_id", None)

                # Style subtasks slightly indented
                if parent:
                    title = f"↳ {title}"
                rows.append(f"""
                <tr>
                    <td>{title}</td>
                    <td>{status}</td>
                    <td>{priority}</td>
                    <td>{start}</td>
                    <td>{end}</td>
                    <td>{notes}</td>
                </tr>
                """)

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>DCLT Projects Dashboard</title>
<style>
body {{
  font-family: Arial, sans-serif;
  margin: 20px;
}}
h1 {{
  text-align: center;
}}
table {{
  border-collapse: collapse;
  width: 100%;
}}
th, td {{
  border: 1px solid #ddd;
  padding: 8px;
}}
th {{
  background-color: #f4f4f4;
  text-align: left;
}}
tr:nth-child(even) {{
  background-color: #f9f9f9;
}}
</style>
</head>
<body>
<h1>DCLT Projects Dashboard</h1>
<table>
<tr>
  <th>Project</th>
  <th>Status</th>
  <th>Priority</th>
  <th>Start</th>
  <th>End</th>
  <th>Notes</th>
</tr>
{''.join(rows)}
</table>
</body>
</html>
"""

output_file = os.path.join(OUTPUT_DIR, "Projects_Dashboard.html")
with open(output_file, "w") as f:
    f.write(html)

print("✅ Dashboard generated:", output_file)