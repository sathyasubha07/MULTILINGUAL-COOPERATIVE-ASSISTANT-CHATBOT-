"""
Builds a persistent ChromaDB vector index from the active domain knowledge files.
Run this once, and again any time the JSON content below changes:

    python scripts/create_embeddings.py

Prototype scope: only farmer_scheme + financial_literacy are embedded for now.
Add more paths to SOURCE_FILES as you bring more domains online (e.g. grievance).
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from sentence_transformers import SentenceTransformer
from config.settings import settings

COLLECTION_NAME = "cooperative_kb"

SOURCE_FILES = [
    os.path.join(settings.DATABASE_PATH, "schemes", "farmer_schemes.json"),
    os.path.join(settings.DATABASE_PATH, "financial", "financial_literacy.json"),
]


def build_index():
    print(f"[*] Loading embedding model: {settings.EMBEDDING_MODEL}")
    model = SentenceTransformer(settings.EMBEDDING_MODEL)

    os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
    client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(COLLECTION_NAME)

    ids, texts, metadatas = [], [], []
    for path in SOURCE_FILES:
        if not os.path.exists(path):
            print(f"[!] Skipping missing file: {path}")
            continue
        with open(path, "r", encoding="utf-8") as f:
            items = json.load(f)
        for item in items:
            ids.append(item["id"])
            texts.append(item["content"])
            metadatas.append({
                "domain": item["domain"],
                "title": item["title"],
                "source": item.get("source", "")
            })
        print(f"[+] Loaded {len(items)} chunks from {os.path.relpath(path, settings.BASE_DIR)}")

    if not ids:
        print("[!] No documents found to embed. Check SOURCE_FILES paths.")
        return

    print(f"[*] Embedding {len(ids)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)

    print(f"[OK] Indexed {len(ids)} documents into ChromaDB at {settings.VECTOR_DB_PATH}")


if __name__ == "__main__":
    build_index()
