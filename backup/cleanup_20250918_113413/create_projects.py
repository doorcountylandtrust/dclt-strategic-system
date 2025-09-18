import os
from datetime import date

# Root path to your repo
ROOT = "data/dclt/02_EXECUTION/10_Projects"

# Define your projects here
projects = [
    {"id": "001", "title": "Brand System (2026)", "priority": "critical", "status": "in_progress"},
    {"id": "002", "title": "Website Overhaul", "priority": "high", "status": "in_progress"},
    {"id": "003", "title": "2026 Nature Notes Calendar", "priority": "medium", "status": "planning"},
    {"id": "004", "title": "Land-Seller & Realtor Interviews", "priority": "high", "status": "planning"},
    {"id": "005", "title": "2026 Annual Comms Planning", "priority": "medium", "status": "not_started"},
    {"id": "006", "title": "Drip Emails for New Members", "priority": "medium", "status": "planning"},
    {"id": "007", "title": "Letterhead Template for Renewals", "priority": "low", "status": "not_started"},
    {"id": "008", "title": "Pebble Beach Kiosk Panels", "priority": "medium", "status": "planning"},
    {"id": "009", "title": "Donation Tube Vinyl Stickers", "priority": "low", "status": "not_started"},
]

# Helper: safe filename
def to_filename(title: str) -> str:
    return title.replace(" ", "_").replace("(", "").replace(")", "").replace("–", "-") + ".md"

def main():
    os.makedirs(ROOT, exist_ok=True)

    for proj in projects:
        filename = os.path.join(ROOT, to_filename(proj["title"]))
        if os.path.exists(filename):
            print(f"⚠️ Skipping {filename} (already exists)")
            continue

        with open(filename, "w", encoding="utf-8") as f:
            f.write("---\n")
            f.write(f"project_id: {proj['id']}\n")
            f.write(f"title: {proj['title']}\n")
            f.write(f"start_date: TBD\n")
            f.write(f"end_date: TBD\n")
            f.write(f"status: {proj['status']}\n")
            f.write(f"priority: {proj['priority']}\n")
            f.write("notes: \n")
            f.write(f"created_date: {date.today().isoformat()}\n")
            f.write("---\n\n")
            f.write(f"# {proj['title']}\n\n")
            f.write("Project notes and details go here.\n")

        print(f"✅ Created {filename}")

    # Optionally archive old projects.md
    old_file = os.path.join(ROOT, "projects.md")
    if os.path.exists(old_file):
        os.rename(old_file, old_file + ".archived")
        print(f"📦 Archived {old_file}")

if __name__ == "__main__":
    main()