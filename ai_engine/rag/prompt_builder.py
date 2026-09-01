"""
System prompt templates and context formatting for multilingual cooperative reasoning.
"""
from typing import List, Dict, Any

class PromptBuilder:
    SYSTEM_PROMPT = """You are 'Sahakar Mitra' (सहकार मित्र), an expert AI Legal & Governance Assistant for India's Cooperative Societies, Farmers, Primary Agricultural Credit Societies (PACS), and Rural Citizens under the Ministry of Cooperation.

Your mandate:
1. Provide accurate, legal, statutory, and procedural guidance on Multi-State Cooperative Societies Act, State Cooperative Bylaws, PMFBY (Crop Insurance), PM-KISAN, KCC, and PACS services.
2. If the user expresses a complaint or issue, act as a Resolution Navigator: provide the designated primary officer, exact documents needed, step-by-step escalation hierarchy, and statutory resolution timeline.
3. Always cite official acts, gazette notifications, or scheme guidelines.
4. Keep the tone empathetic, clear, structured, and easy for rural citizens to understand.
"""

    @classmethod
    def build_rag_prompt(cls, query: str, context_docs: List[Dict[str, Any]], language: str = "en") -> str:
        formatted_context = ""
        for i, doc in enumerate(context_docs, 1):
            title = doc.get("title") or doc.get("scheme_name") or doc.get("act_name") or "Document"
            summary = doc.get("summary") or doc.get("overview") or doc.get("financial_benefit") or ""
            provisions = doc.get("key_provisions") or doc.get("eligibility_criteria") or doc.get("permitted_activities") or []
            citations = doc.get("citations", [])

            formatted_context += f"\n--- Context Document {i}: {title} ---\n"
            formatted_context += f"Summary/Benefit: {summary}\n"
            if provisions:
                formatted_context += f"Details: {', '.join(provisions[:4])}\n"
            if citations:
                formatted_context += f"Official Citations: {', '.join(citations)}\n"

        prompt = f"{cls.SYSTEM_PROMPT}\n\n"
        prompt += f"CONTEXT INFORMATION FROM VERIFIED COOPERATIVE DATABASE:\n{formatted_context}\n\n"
        prompt += f"USER QUERY (Language requested: {language}):\n{query}\n\n"
        prompt += "Provide a complete, structured response with Key Points, Recommended Action, and Official Citations."
        return prompt
