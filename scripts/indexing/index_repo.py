#!/usr/bin/env python3
import os
import json
import hashlib
from pathlib import Path
from openai import OpenAI

# 🔧 Config
ROOT_DIR = "data/dclt/02_EXECUTION/10_Projects"
INDEX_PATH = "reports/index.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def file_hash(path: Path):
    """Return SHA1 hash of a file."""
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def embed_text(text: str):
    """Generate an embedding for the given text."""
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:5000]  # truncate to 5000 chars
    ).data[0].embedding

def load_index():
    if Path(INDEX_PATH).exists():
        with open(INDEX_PATH, "r") as f:
            return json.load(f)
    return {}

def save_index(index):
    os.makedirs(Path(INDEX_PATH).parent, exist_ok=True)
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

def main():
    index = load_index()
    updated = {}
    new_files = 0
    skipped = 0
    removed = 0

    # Walk through all .md files
    for path in Path(ROOT_DIR).rglob("*.md"):
        rel_path = str(path.relative_to(ROOT_DIR))
        hash_val = file_hash(path)

        # Skip if unchanged
        if rel_path in index and index[rel_path]["hash"] == hash_val:
            updated[rel_path] = index[rel_path]
            skipped += 1
            continue

        # Read content
        text = path.read_text(errors="ignore")

        # Generate embedding + preview
        emb = embed_text(text)
        preview = text.strip().replace("\n", " ")[:200] + "..."

        updated[rel_path] = {
            "hash": hash_val,
            "embedding": emb,       # stored as JSON array (not string!)
            "preview": preview
        }
        new_files += 1

    # Detect removed files
    for old_path in index.keys():
        if old_path not in updated:
            removed += 1

    save_index(updated)

    print(f"✅ Index updated at {INDEX_PATH}")
    print(f"   {new_files} new/updated, {skipped} unchanged, {removed} removed.")

if __name__ == "__main__":
    main()