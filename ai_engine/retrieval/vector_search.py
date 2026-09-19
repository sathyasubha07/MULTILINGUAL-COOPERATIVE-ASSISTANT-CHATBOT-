import re
import math
from typing import List, Dict, Any, Optional
from config.settings import settings

COLLECTION_NAME = "cooperative_kb"


class VectorSearchEngine:
    def __init__(self):
        self.chroma_available = False
        self.indexed_docs: List[Dict[str, Any]] = []
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer
            self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
            self.collection = self.client.get_or_create_collection(COLLECTION_NAME)
            self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
            self.chroma_available = True
        except Exception:
            self.chroma_available = False

    def load_index(self, docs: List[Dict[str, Any]] = None):
        if docs:
            self.indexed_docs = docs

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def search(self, query: str, domain_filter: Optional[str] = None, top_k: int = 4) -> List[Dict[str, Any]]:
        # 1. ChromaDB Dense Search if available
        if self.chroma_available:
            try:
                count = self.collection.count()
                if count > 0:
                    query_embedding = self.model.encode([query]).tolist()
                    where = {"domain": domain_filter} if (domain_filter and domain_filter != "general_coop") else None
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
                    if docs:
                        return docs
            except Exception:
                pass

        # 2. Resilient BM25 / Keyword Token Fallback
        if not self.indexed_docs:
            return []

        query_tokens = set(self._tokenize(query))
        scored_docs = []

        for doc in self.indexed_docs:
            if domain_filter and domain_filter != "general_coop" and doc.get("domain") != domain_filter:
                continue

            doc_text = " ".join([
                str(v) for k, v in doc.items() if isinstance(v, (str, list, dict))
            ])
            doc_tokens = self._tokenize(doc_text)
            if not doc_tokens:
                continue

            matches = [token for token in doc_tokens if token in query_tokens]
            score = len(matches) / (math.sqrt(len(doc_tokens)) + 1.0)

            title = str(doc.get("title") or doc.get("scheme_name") or doc.get("act_name") or "").lower()
            for q_tok in query_tokens:
                if q_tok in title:
                    score += 1.5

            if score > 0:
                scored_docs.append({"doc": doc, "score": score})

        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return [item["doc"] for item in scored_docs[:top_k]]

