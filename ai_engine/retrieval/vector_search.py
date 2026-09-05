"""
Semantic vector search using ChromaDB + Sentence-Transformers embeddings.
Replaces the earlier keyword/BM25 placeholder with real RAG retrieval.

The index itself is built once (and rebuilt whenever data changes) via
scripts/create_embeddings.py. This class only connects to that persisted
index and runs queries against it.
"""
from typing import List, Dict, Any, Optional

import chromadb
from sentence_transformers import SentenceTransformer
from config.settings import settings

COLLECTION_NAME = "cooperative_kb"


class VectorSearchEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME)
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def load_index(self, docs: List[Dict[str, Any]] = None):
        # No-op kept for backward compatibility with HybridRetriever's old
        # call site. The real index is built by scripts/create_embeddings.py.
        pass

    def search(self, query: str, domain_filter: Optional[str] = None, top_k: int = 4) -> List[Dict[str, Any]]:
        count = self.collection.count()
        if count == 0:
            return []

        query_embedding = self.model.encode([query]).tolist()
        where = None
        if domain_filter and domain_filter != "general_coop":
            where = {"domain": domain_filter}

        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, count),
            where=where,
        )

        ids = result.get("ids", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        documents = result.get("documents", [[]])[0]

        docs = []
        for doc_id, meta, content in zip(ids, metadatas, documents):
            docs.append({
                "id": doc_id,
                "title": meta.get("title", doc_id),
                "domain": meta.get("domain"),
                "summary": content,
                "citations": [meta["source"]] if meta.get("source") else [],
            })
        return docs
