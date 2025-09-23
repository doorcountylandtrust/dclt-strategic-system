#!/usr/bin/env python3
import os
import json
import time
import hashlib
from pathlib import Path
from openai import OpenAI
import subprocess

# === CONFIG ===
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # repo root
DATA_DIR = PROJECT_ROOT / "data/dclt/02_EXECUTION/10_Projects"
INDEX_PATH = Path("reports/index.json")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === HELPERS ===
def file_hash(path):
    """Return md5 hash of file contents."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def git_commit(message, add_all=False):
    """Run a git commit with a message. Add changes if requested."""
    try:
        if add_all:
            subprocess.run(["git", "add", "-A"], cwd=PROJECT_ROOT)
        else:
            subprocess.run(["git", "add", str(INDEX_PATH)], cwd=PROJECT_ROOT)
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=PROJECT_ROOT,
            check=False
        )
    except Exception as e:
        print(f"[WARN] Git commit skipped: {e}")

# === LOAD PREVIOUS INDEX ===
if INDEX_PATH.exists():
    with open(INDEX_PATH, "r") as f:
        index = json.load(f)
else:
    index = {}

# Track stats
indexed, skipped, removed = 0, 0, 0
seen_files = set()

# === PRE-INDEX SNAPSHOT COMMIT ===
git_commit(f"Pre-index snapshot {time.strftime('%Y-%m-%d %H:%M')}", add_all=True)

# === WALK FILES ===
for path in DATA_DIR.rglob("*.md"):
    rel_path = str(path.relative_to(PROJECT_ROOT))
    seen_files.add(rel_path)
    mtime = os.path.getmtime(path)
    hash_val = file_hash(path)

    # Skip unchanged
    if rel_path in index and index[rel_path]["hash"] == hash_val:
        skipped += 1
        continue

    # Read text
    with open(path, "r") as f:
        text = f.read()

    # Generate embedding (truncate if too long)
    try:
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=text[:5000]
        ).data[0].embedding
    except Exception as e:
        print(f"[ERROR] embedding failed for {rel_path}: {e}")
        continue

    index[rel_path] = {
        "mtime": mtime,
        "hash": hash_val,
        "embedding": emb
    }
    indexed += 1

# Remove stale entries
for old_file in list(index.keys()):
    if old_file not in seen_files:
        del index[old_file]
        removed += 1

# Save index
INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(INDEX_PATH, "w") as f:
    json.dump(index, f, indent=2)

# === AUTO COMMIT INDEX UPDATE ===
git_commit(f"Auto: updated index.json {time.strftime('%Y-%m-%d %H:%M')}")

# === OPTIONAL PUSH ===
# subprocess.run(["git", "push"], cwd=PROJECT_ROOT)

# === SUMMARY ===
print(f"[DONE] {indexed} files indexed, {skipped} skipped, {removed} removed.")