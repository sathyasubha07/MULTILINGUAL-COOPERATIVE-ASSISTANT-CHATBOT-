"""
Hybrid Retrieval engine: real ChromaDB semantic search + domain metadata filtering.
"""
import os
import json
from typing import List, Dict, Any, Optional
from config.settings import settings
from ai_engine.retrieval.vector_search import VectorSearchEngine


class HybridRetriever:
    def __init__(self):
        self.vector_engine = VectorSearchEngine()
        self.authorities: List[Dict[str, Any]] = []
        self._load_authorities()

    def _load_authorities(self):
        auth_path = settings.AUTHORITIES_PATH
        if os.path.exists(auth_path):
            try:
                with open(auth_path, "r", encoding="utf-8") as f:
                    self.authorities = json.load(f)
            except Exception as e:
                print(f"Error loading authorities: {e}")

    def retrieve(self, query: str, domain_filter: Optional[str] = None, top_k: int = 3) -> Dict[str, Any]:
        results = self.vector_engine.search(query=query, domain_filter=domain_filter, top_k=top_k)

        citations = []
        for doc in results:
            citations.extend(doc.get("citations", []))

        return {
            "documents": results,
            "citations": list(set(citations)),
            "authorities": self.authorities[:2] if domain_filter == "grievance" else []
        }
