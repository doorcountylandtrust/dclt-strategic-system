import os
import shutil

# Resolve paths relative to repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = os.path.join(REPO_ROOT, "data", "dclt", "02_EXECUTION")

# Mapping rules: keyword → destination folder
RULES = {
    # Dashboards
    "Task Tracker": "00 Dashboards",
    "Master Task Tracker": "00 Dashboards",
    "Progress Dashboard": "00 Dashboards",

    # Projects
    "Brand System": "10 Projects",
    "Website Strategy Hub": "10 Projects",

    # Operations
    "Campaigns": "20 Operations",
    "Content & Campaign Calendar": "20 Operations",

    # Pipelines
    "Content & Storytelling Pipeline": "40 Pipelines",
}

# Container descriptions
DESCRIPTIONS = {
    "00 Dashboards": "# Dashboards\n\nMeta views of work: task trackers, progress dashboards, milestone boards.\n",
    "10 Projects": "# Projects\n\nMajor initiatives with start/end dates and subtasks (e.g. Rebrand, Website Redesign).\n",
    "20 Operations": "# Operations\n\nOngoing, recurring workstreams (campaigns, appeals, renewals, calendars).\n",
    "30 Calendars": "# Calendars\n\nTime-driven outputs (publication schedules, ad buys, annual rhythms).\n",
    "40 Pipelines": "# Pipelines\n\nFlows of ideas → drafts → final outputs (e.g. Content & Storytelling Pipeline).\n",
}

# Ensure container folders exist and add README.md if missing
for folder, description in DESCRIPTIONS.items():
    path = os.path.join(BASE_DIR, folder)
    os.makedirs(path, exist_ok=True)
    readme_path = os.path.join(path, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(description)
        print(f"Created {readme_path}")

# Walk files/folders in Execution root
for item in os.listdir(BASE_DIR):
    if item.startswith(("0", "1", "2", "3", "4")):
        continue  # skip container folders
    if item in ["README.md"]:
        continue

    src = os.path.join(BASE_DIR, item)
    moved = False

    for keyword, dest in RULES.items():
        if keyword in item:
            dest_path = os.path.join(BASE_DIR, dest, item)
            print(f"Moving {item} → {dest}/")
            shutil.move(src, dest_path)
            moved = True
            break

    if not moved:
        print(f"[SKIPPED] {item} (no rule matched)")