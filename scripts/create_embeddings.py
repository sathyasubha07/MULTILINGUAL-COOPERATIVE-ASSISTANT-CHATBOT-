"""
Builds a persistent ChromaDB vector index from the active domain knowledge files.
Run this once, and again any time the JSON content below changes:

    python scripts/create_embeddings.py

Each chunk's TITLE is embedded together with its content (not just the content
alone) — this matters because acronyms/scheme codes like "PM-KISAN" often only
appear in the title field, not in the body text. Without the title included,
a query for the exact scheme code can fail to match its own document.

Each scheme's "designation" field (the officer type responsible for it,
e.g. "AAO") is carried through into Chroma's metadata, so retrieval can
later look up the right contact via authority_lookup.py.
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
            item_id = item.get("id")
            title = item.get("title") or item.get("scheme_name") or item_id
            content = item.get("content") or item.get("summary") or ""
            domain = item.get("domain", "")
            source = item.get("source", "")
            if not source and item.get("citations"):
                source = "; ".join(item["citations"])
            designation = item.get("designation", "")

            # KEY FIX: embed title + content together, not content alone.
            # Also fold in scheme_code if present, so short-code queries
            # ("PM-KISAN", "KCC", "SMAM"...) have literal text to match.
            scheme_code = item.get("scheme_code", "")
            embed_text = f"{title}. {scheme_code}. {content}".strip()

            ids.append(item_id)
            texts.append(embed_text)
            metadatas.append({
                "domain": domain,
                "title": title,
                "source": source,
                "designation": designation,
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
