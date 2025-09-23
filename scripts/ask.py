import sys
import json
import os
from openai import OpenAI
import numpy as np

INDEX_PATH = "reports/index.json"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def embed_text(text):
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

def search_index(query, k=5):
    with open(INDEX_PATH, "r") as f:
        index = json.load(f)

    q_emb = embed_text(query)
    scored = []
    for path, entry in index.items():
        sim = cosine_similarity(q_emb, entry["embedding"])
        scored.append((sim, path, entry))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:k]

def answer_question(query):
    results = search_index(query, k=5)
    context = "\n\n".join(
        f"From {path}:\n{entry.get('preview', '')}" for _, path, entry in results
    )

    prompt = f"""You are an assistant helping manage LandTrust projects.

Question: {query}

Here are relevant notes:
{context}

Answer in clear, direct language, citing specific projects if possible.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # ✅ use this for now
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ Please provide a question. Example: python ask.py 'Status of Pebble Beach Kiosk'")
    else:
        query = " ".join(sys.argv[1:])
        print("🤖", answer_question(query))