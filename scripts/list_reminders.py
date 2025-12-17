import json
from pathlib import Path

REMINDERS_PATH = Path("data/dclt/reminders.json")

def list_reminders():
    if not REMINDERS_PATH.exists():
        print("⚠️ No reminders found.")
        return

    with open(REMINDERS_PATH, "r") as f:
        reminders = json.load(f)

    if not reminders:
        print("⚠️ Reminder file is empty.")
        return

    # Counters for summary
    counts = {"open": 0, "done": 0, "snoozed": 0, "other": 0}

    for r in reminders:
        status = r.get("status", "open")
        counts[status] = counts.get(status, 0) + 1

        print(f"- [{status}] {r.get('id')} :: {r.get('text')}")
        if r.get("due"):
            print(f"   ⏰ Due: {r['due']}")
        if r.get("project"):
            print(f"   📂 Project: {r['project']}")
        print()

    # Print summary
    print("📊 Summary:")
    print(f"   Open: {counts['open']}")
    print(f"   Done: {counts['done']}")
    print(f"   Snoozed: {counts['snoozed']}")
    if counts.get("other", 0) > 0:
        print(f"   Other: {counts['other']}")

if __name__ == "__main__":
    list_reminders()