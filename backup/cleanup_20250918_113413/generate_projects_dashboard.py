import os
import frontmatter

# Define base directories
project_dir = os.path.join("data", "dclt", "02_EXECUTION", "10_Projects")
output_dir = os.path.join(project_dir, "Dashboards")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, "Projects_Dashboard.html")

rows = []
for fname in os.listdir(project_dir):
    if fname.endswith(".md"):
        path = os.path.join(project_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
            rows.append({
                "title": post.get("title", fname),
                "status": post.get("status", ""),
                "priority": post.get("priority", ""),
                "start_date": post.get("start_date", ""),
                "end_date": post.get("end_date", ""),
                "notes": post.get("notes", "")
            })

# Build HTML
html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Projects Dashboard</title>
<style>
table {border-collapse: collapse; width: 100%;}
th, td {border: 1px solid #aaa; padding: 8px; text-align: left;}
th {background: #ddd;}
</style>
</head>
<body>
<h1>Projects Dashboard</h1>
<table>
<tr><th>Project</th><th>Status</th><th>Priority</th><th>Start</th><th>End</th><th>Notes</th></tr>
"""

for row in rows:
    html += f"<tr><td>{row['title']}</td><td>{row['status']}</td><td>{row['priority']}</td><td>{row['start_date']}</td><td>{row['end_date']}</td><td>{row['notes']}</td></tr>\n"

html += "</table></body></html>"

# Save
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Dashboard written to: {os.path.abspath(output_file)}")
print(f"📂 Found {len(rows)} project files.")