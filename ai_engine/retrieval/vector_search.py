"""
Vector search simulation & indexer with lightweight cosine/BM25 scoring for offline edge capability.
"""
import math
import re
from typing import List, Dict, Any

class VectorSearchEngine:
    def __init__(self):
        self.indexed_docs = []

    def load_index(self, docs: List[Dict[str, Any]]):
        self.indexed_docs = docs

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        query_tokens = set(self._tokenize(query))
        scored_docs = []

        for doc in self.indexed_docs:
            doc_text = " ".join([
                str(v) for k, v in doc.items() if isinstance(v, (str, list, dict))
            ])
            doc_tokens = self._tokenize(doc_text)
            if not doc_tokens:
                continue

            # Term overlap + length normalization (BM25 style lightweight similarity)
            matches = [token for token in doc_tokens if token in query_tokens]
            score = len(matches) / (math.sqrt(len(doc_tokens)) + 1.0)
            
            # Boost matches in title or section
            title = str(doc.get("title") or doc.get("scheme_name") or doc.get("act_name") or "").lower()
            for q_tok in query_tokens:
                if q_tok in title:
                    score += 1.5

            if score > 0:
                scored_docs.append({"doc": doc, "score": score})

        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return [item["doc"] for item in scored_docs[:top_k]]
