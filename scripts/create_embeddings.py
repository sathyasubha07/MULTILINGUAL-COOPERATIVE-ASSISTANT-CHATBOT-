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
    os.path.join(settings.DATABASE_PATH, "grievances", "grievance_catalog.json"),
    os.path.join(settings.DATABASE_PATH, "pacs", "pacs_bylaws.json"),
    os.path.join(settings.DATABASE_PATH, "pmfby", "pmfby_guidelines.json"),
    os.path.join(settings.DATABASE_PATH, "laws", "cooperative_laws.json"),
]


def extract_doc_text(item):
    if "content" in item and item["content"]:
        return str(item["content"])
    parts = []
    for k in ["title", "scheme_name", "act_name", "grievance_type", "summary", "description", "resolution_procedure"]:
        if k in item and item[k]:
            parts.append(str(item[k]))
    for list_k in ["key_provisions", "key_benefits", "eligibility", "citations", "applicable_laws"]:
        if list_k in item and isinstance(item[list_k], list):
            parts.extend([str(x) for x in item[list_k]])
    return " \n".join(parts) if parts else str(item)


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
        for idx, item in enumerate(items):
            doc_id = item.get("id") or f"{os.path.basename(path).split('.')[0]}_{idx}"
            doc_text = extract_doc_text(item)
            doc_domain = item.get("domain") or os.path.basename(path).split("_")[0]
            doc_title = item.get("title") or item.get("scheme_name") or item.get("act_name") or item.get("grievance_type") or doc_id
            doc_source = item.get("source") or (item.get("citations")[0] if item.get("citations") else "")

            ids.append(str(doc_id))
            texts.append(doc_text)
            metadatas.append({
                "domain": str(doc_domain),
                "title": str(doc_title),
                "source": str(doc_source)
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
