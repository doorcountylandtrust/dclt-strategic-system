#!/usr/bin/env python3
"""
scripts/add_reminder.py

Usage:
  python scripts/add_reminder.py --text "Remind me to check signage quotes" --due 2025-10-01 --project "Pebble Beach Kiosk Panels" --created_by "Don" --open-md

This will append a reminder to data/dclt/reminders.json and optionally create
data/dclt/Reminders/<id>.md with frontmatter for Obsidian.
"""
import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path
import argparse

ROOT = Path.cwd()
REMINDERS_JSON = ROOT / "data" / "dclt" / "reminders.json"
REMINDERS_MD_DIR = ROOT / "data" / "dclt" / "Reminders"

def load_reminders():
    if not REMINDERS_JSON.exists():
        return []
    try:
        return json.loads(REMINDERS_JSON.read_text(encoding="utf-8"))
    except Exception as e:
        print("⚠️ Could not load reminders.json:", e)
        return []

def save_reminders(reminders):
    REMINDERS_JSON.parent.mkdir(parents=True, exist_ok=True)
    REMINDERS_JSON.write_text(json.dumps(reminders, indent=2, ensure_ascii=False), encoding="utf-8")

def make_md(rem):
    REMINDERS_MD_DIR.mkdir(parents=True, exist_ok=True)
    md_path = REMINDERS_MD_DIR / f"{rem['id']}.md"
    frontmatter = [
        "---",
        f"id: {rem['id']}",
        f"title: \"{rem['text'].replace('\"','\\\"')}\"",
        f"created_by: {rem.get('created_by','')}",
        f"created_at: {rem['created_at']}",
        f"due: {rem.get('due','')}",
        f"project: \"{rem.get('project','')}\"",
        f"status: {rem.get('status','open')}",
        "---",
        "",
        rem.get("notes",""),
    ]
    md_path.write_text("\n".join(frontmatter), encoding="utf-8")
    return md_path

def main():
    parser = argparse.ArgumentParser(description="Add a reminder to the repo.")
    parser.add_argument("--text", required=True, help="Reminder text (wrap in quotes)")
    parser.add_argument("--due", required=False, help="Due date YYYY-MM-DD (optional)")
    parser.add_argument("--project", required=False, help="Project name (optional)")
    parser.add_argument("--created_by", required=False, default=os.getenv("USER",""), help="Optional author")
    parser.add_argument("--notes", required=False, default="", help="Optional notes")
    parser.add_argument("--open-md", action="store_true", help="Create a companion markdown file in data/dclt/Reminders/")
    args = parser.parse_args()

    reminders = load_reminders()
    now = datetime.utcnow().replace(microsecond=0).isoformat()
    unique_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]

    rem = {
        "id": unique_id,
        "text": args.text,
        "created_by": args.created_by or os.getenv("USER",""),
        "created_at": now,
        "due": args.due or "",
        "project": args.project or "",
        "status": "open",
        "notes": args.notes or ""
    }

    reminders.append(rem)
    save_reminders(reminders)

    md_path = None
    if args.open_md:
        md_path = make_md(rem)

    print("✅ Reminder added:")
    print(json.dumps(rem, indent=2))
    if md_path:
        print(f"📝 Markdown created at: {md_path}")

if __name__ == "__main__":
    main()