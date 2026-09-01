"""
Domain Router for dispatching queries to specialized RAG handlers and knowledge retrievers.
"""
from typing import Dict, Any
from ai_engine.orchestration.intent_classifier import IntentClassifier
from ai_engine.retrieval.hybrid_retrieval import HybridRetriever

class DomainRouter:
    def __init__(self):
        self.classifier = IntentClassifier()
        self.retriever = HybridRetriever()

    def route_and_retrieve(self, query: str, language: str = "en") -> Dict[str, Any]:
        classification = self.classifier.classify(query)
        domain = classification["domain"]
        
        # Hybrid retrieval with domain filtering
        retrieval_results = self.retriever.retrieve(query=query, domain_filter=domain)
        
        return {
            "intent": classification,
            "domain": domain,
            "language": language,
            "retrieved_context": retrieval_results["documents"],
            "citations": retrieval_results["citations"],
            "authorities": retrieval_results.get("authorities", [])
        }
