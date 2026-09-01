"""
Hybrid Retrieval engine combining Vector/BM25 search with metadata filtering and static database loading.
"""
import os
import json
from typing import List, Dict, Any, Optional
from config.settings import settings
from ai_engine.retrieval.vector_search import VectorSearchEngine
from ai_engine.retrieval.metadata_filter import MetadataFilter

class HybridRetriever:
    def __init__(self):
        self.vector_engine = VectorSearchEngine()
        self.all_documents: List[Dict[str, Any]] = []
        self.authorities: List[Dict[str, Any]] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        self.all_documents = []
        data_dir = settings.DATABASE_PATH
        
        if os.path.exists(data_dir):
            for root, _, files in os.walk(data_dir):
                for file in files:
                    if file.endswith(".json"):
                        path = os.path.join(root, file)
                        try:
                            with open(path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                if isinstance(data, list):
                                    self.all_documents.extend(data)
                                elif isinstance(data, dict):
                                    self.all_documents.append(data)
                        except Exception as e:
                            print(f"Error loading {path}: {e}")

        # Load authorities
        auth_path = settings.AUTHORITIES_PATH
        if os.path.exists(auth_path):
            try:
                with open(auth_path, "r", encoding="utf-8") as f:
                    self.authorities = json.load(f)
            except Exception as e:
                print(f"Error loading authorities: {e}")

        self.vector_engine.load_index(self.all_documents)

    def retrieve(self, query: str, domain_filter: Optional[str] = None, top_k: int = 3) -> Dict[str, Any]:
        # Filter documents if domain is specific
        target_docs = self.all_documents
        if domain_filter and domain_filter != "general_coop":
            filtered = MetadataFilter.filter_by_domain(self.all_documents, domain_filter)
            if filtered:
                target_docs = filtered

        # Temporary search on filtered pool
        searcher = VectorSearchEngine()
        searcher.load_index(target_docs)
        results = searcher.search(query=query, top_k=top_k)

        # Extract verified citations
        citations = []
        for doc in results:
            if "citations" in doc and isinstance(doc["citations"], list):
                citations.extend(doc["citations"])
            elif "section" in doc:
                citations.append(f"{doc.get('act_name', 'Act')} - {doc.get('section')}")

        return {
            "documents": results if results else target_docs[:2],
            "citations": list(set(citations)),
            "authorities": self.authorities[:2] if domain_filter == "grievance" else []
        }
