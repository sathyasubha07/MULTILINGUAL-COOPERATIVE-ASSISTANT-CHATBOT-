"""
End-to-End Multilingual RAG Pipeline coordinating Domain Routing, Retrieval, Reasoner, and Citations.
"""
from typing import Dict, Any
from ai_engine.orchestration.domain_router import DomainRouter
from ai_engine.rag.prompt_builder import PromptBuilder
from ai_engine.llm.reasoner import LLMReasoner
from ai_engine.verification.source_validator import SourceValidator
from ai_engine.resolution_navigator.procedure_generator import ProcedureGenerator

class RAGPipeline:
    def __init__(self):
        self.router = DomainRouter()
        self.reasoner = LLMReasoner()
        self.validator = SourceValidator()
        self.procedure_gen = ProcedureGenerator()

    def process_query(self, query: str, language: str = "en") -> Dict[str, Any]:
        # 1. Routing & Retrieval
        routing_result = self.router.route_and_retrieve(query=query, language=language)
        domain = routing_result["domain"]
        docs = routing_result["retrieved_context"]
        citations = routing_result["citations"]

        # 2. Prompt Building
        prompt = PromptBuilder.build_rag_prompt(query, docs, language)

        # 3. LLM Reasoning
        answer = self.reasoner.generate_response(prompt, docs, domain, language)

        # 4. Source Verification
        validation = self.validator.validate(answer, docs, citations)

        # 5. Procedure / Resolution recommendation if Grievance
        procedure = None
        if domain == "grievance" or "delay" in query.lower() or "reject" in query.lower():
            procedure = self.procedure_gen.generate_for_query(query, docs)

        return {
            "query": query,
            "language": language,
            "domain": domain,
            "confidence": routing_result["intent"]["confidence"],
            "answer": answer,
            "citations": validation["citations"],
            "verification_status": validation["is_verified"],
            "procedure": procedure,
            "authorities": routing_result.get("authorities", [])
        }
