import os
import json
import hashlib
import datetime
import numpy as np
from pathlib import Path
from openai import OpenAI

# === CONFIG ===
ROOT_DIR = Path("data/dclt/02_EXECUTION/10_Projects")
REPORTS_DIR = Path("reports")
EMBED_DIR = REPORTS_DIR / "embeddings"
INDEX_PATH = REPORTS_DIR / "index.json"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === HELPERS ===
def file_hash(path: Path) -> str:
    """SHA256 hash of file contents"""
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_index() -> dict:
    if INDEX_PATH.exists():
        with open(INDEX_PATH, "r") as f:
            return json.load(f)
    return {}

def save_index(index: dict):
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

def embed_text(text: str) -> np.ndarray:
    """Call OpenAI embeddings API and return numpy array"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text[:5000]  # truncate for safety
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

# === MAIN INDEXER ===
def main():
    REPORTS_DIR.mkdir(exist_ok=True)
    EMBED_DIR.mkdir(exist_ok=True)

    index = load_index()
    updated_index = {}
    new_files, unchanged_files, removed_files = 0, 0, 0

    for path in ROOT_DIR.rglob("*.md"):
        rel_path = str(path.relative_to(ROOT_DIR))
        hash_val = file_hash(path)

        # skip unchanged
        if rel_path in index and index[rel_path]["hash"] == hash_val:
            updated_index[rel_path] = index[rel_path]
            unchanged_files += 1
            continue

        # read file and make preview
        text = path.read_text(errors="ignore")
        preview = text[:200].replace("\n", " ")

        # embed and save vector to .npy file
        emb = embed_text(text)
        emb_file = f"{hash_val}.npy"
        np.save(EMBED_DIR / emb_file, emb)

        # record metadata
        updated_index[rel_path] = {
            "hash": hash_val,
            "modified": datetime.datetime.now().isoformat(),
            "embedding_file": emb_file,
            "preview": preview
        }

        new_files += 1

    # detect removed files
    for rel_path in index.keys():
        if rel_path not in updated_index:
            removed_files += 1

    # save index
    save_index(updated_index)

    print(f"✅ Index updated at {INDEX_PATH}")
    print(f"   {new_files} new/updated, {unchanged_files} unchanged, {removed_files} removed.")

if __name__ == "__main__":
    main()