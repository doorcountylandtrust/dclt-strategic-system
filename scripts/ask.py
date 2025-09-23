# scripts/query/ask.py

import sys
import json
import os
import numpy as np
from openai import OpenAI

INDEX_PATH = "reports/index.json"   # same place your indexer writes to
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_index(query, k=5):
    # load the index
    with open(INDEX_PATH, "r") as f:
        index = json.load(f)

    # embed the query
    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    # score each doc
    scored = []
    for entry in index:
        sim = cosine_similarity(q_emb, entry["embedding"])
        scored.append((sim, entry))

    # sort by similarity
    scored.sort(key=lambda x: x[0], reverse=True)
    return [e for _, e in scored[:k]]

def answer_question(query):
    # retrieve top matches
    results = search_index(query, k=5)

    # stitch context
    context = "\n\n".join([r["text"] for r in results])

    # ask GPT with context
    prompt = f"""
You are an assistant for my project repo. Use the following context to answer the question:

Context:
{context}

Question: {query}

Answer:
    """

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ask.py 'your question here'")
        sys.exit(1)

    query = sys.argv[1]
    answer = answer_question(query)
    print("\nQ:", query)
    print("A:", answer)