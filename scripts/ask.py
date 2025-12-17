import sys
import os
import json
import numpy as np
from pathlib import Path
from openai import OpenAI

# === CONFIG ===
REPORTS_DIR = Path("reports")
INDEX_PATH = REPORTS_DIR / "index.json"
EMBED_DIR = REPORTS_DIR / "embeddings"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Helpers ---
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def embed_query(query: str) -> np.ndarray:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

def search_index(query: str, k: int = 5):
    """Search index.json + .npy embeddings for best matches"""
    with open(INDEX_PATH, "r") as f:
        index = json.load(f)

    q_emb = embed_query(query)
    scored = []

    for rel_path, meta in index.items():
        emb_file = EMBED_DIR / meta["embedding_file"]
        if not emb_file.exists():
            continue
        emb = np.load(emb_file)
        sim = cosine_similarity(q_emb, emb)
        scored.append((sim, rel_path, meta))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:k]

def answer_question(query: str):
    results = search_index(query, k=5)

    if not results:
        return "No relevant files found."

    context = "\n\n".join(
        f"From {path}:\n{entry['preview']}"
        for _, path, entry in results
    )

    prompt = f"""You are an assistant helping manage LandTrust projects.

Question: {query}

Here are relevant notes:\n{context}

Answer in clear, direct language, citing specific projects if possible.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# --- CLI Entrypoint ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Please provide a question. Example: python scripts/ask.py 'Status of Pebble Beach Kiosk'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print("🤖", answer_question(query))