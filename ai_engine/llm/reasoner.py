"""
LLM Reasoner with multi-backend support: Google Gemini, Groq, Local Ollama, and Edge Rule-Grounded Synthesis.
Guarantees 100% offline & edge availability for Smart Kiosks / Raspberry Pi devices while leveraging
Google Gemini Multi-Agent personas for deep statutory reasoning when online.
"""
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from config.settings import settings

# Specialized Domain Agent Personas
AGENT_PERSONAS = {
    "farmer_scheme": (
        "You are the Senior Agricultural Schemes & Farmer Welfare Agent for India's Cooperative System. "
        "You provide comprehensive statutory guidance on Central & State agricultural schemes (PM-KISAN, MIDH, NFSM, "
        "PM-KUSUM solar pumps, SMAM farm mechanization, PKVY organic farming, AIF infrastructure fund, NLM livestock, etc.), "
        "certified seed & fertilizer procurement, subsidy calculation, document checklists, and application workflows."
    ),
    "grievance": (
        "You are the Senior Cooperative Grievance & Statutory Dispute Redressal Agent. "
        "You provide legal resolution pathways, 3-Tier Escalation Ladders, statutory SLA timelines under the Citizen Charter, "
        "remedies against officer corruption, loan delays, membership denial, Aadhaar/CSC demographic updates, and "
        "generate structured legal petition drafts with competent override authorities."
    ),
    "pacs_pmfby": (
        "You are the Senior PACS & PMFBY Crop Insurance Agent. "
        "You specialize in Primary Agricultural Credit Society Model Bye-Laws 2023 (25+ diversified activities, CSC, custom hiring, Jan Aushadhi), "
        "PMFBY 72-Hour Calamity Intimation protocols (14447 toll-free / Crop Insurance App), 2% Kharif / 1.5% Rabi / 5% Commercial premium rates, "
        "Clause 17.2 bank default liabilities, and District Grievance Redressal Committee (DGRC) dispute escalation."
    ),
    "cooperative_law": (
        "You are the Senior Cooperative Law & Statutory Governance Legal Agent. "
        "You specialize in the Multi-State Co-operative Societies (MSCS) Act 2002 & 2023 Amendment, State Co-operative Societies Acts, "
        "Section 45 Cooperative Election Authority (CEA), Section 84 Statutory Arbitration (bar of civil courts, 3-year limitation period), "
        "Section 85 Cooperative Ombudsman, Board disqualifications, and 97th Constitutional Amendment democratic principles."
    ),
    "financial_literacy": (
        "You are the Senior Rural Banking, KCC & Financial Literacy Agent. "
        "You specialize in KCC Scale of Finance calculation, Modified Interest Subvention Scheme (MISS) 4% net interest rate, "
        "RBI Fair Lending mandates (15-day mandatory title deed release under ₹5,000/day penalty), AePS 2FA biometric safety, "
        "and NPCI Aadhaar Mapper DBT Seeding."
    )
}

LANGUAGE_NAMES = {
    "en": "English",
    "ta": "Tamil (தமிழ்)",
    "hi": "Hindi (हिंदी)",
    "ml": "Malayalam (മലയാളം)",
    "te": "Telugu (తెలుగు)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "mr": "Marathi (मराठी)",
    "gu": "Gujarati (ગુજરાતી)",
    "bn": "Bengali (বাংলা)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "or": "Odia (ଓଡ଼ିଆ)"
}

class LLMReasoner:
    def __init__(self):
        self.provider = settings.DEFAULT_LLM_PROVIDER
        self.groq_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY")
        self.gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        self.gemini_models = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite-preview", "gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.7-flash"]

    def generate_response(self, prompt: str, context_docs: List[Dict[str, Any]], domain: str, language: str = "en") -> str:
        """
        Generate a legally-grounded statutory response using Gemini (or Groq) if available,
        with instant fallback to local edge reasoning for offline kiosk reliability.
        """
        # 1. Try Gemini Provider if configured
        if self.gemini_key and (self.provider == "gemini" or self.provider == "local_rule_rag" or not self.groq_key):
            gemini_res = self._call_gemini(prompt, context_docs, domain, language)
            if gemini_res and len(gemini_res.strip()) > 20:
                return gemini_res

        # 2. Try Groq Provider if configured
        if self.groq_key and self.provider == "groq":
            groq_res = self._call_groq(prompt)
            if groq_res and len(groq_res.strip()) > 20:
                return groq_res

        # 3. Local Edge Synthesizer (Zero-latency, 100% offline compliant)
        return self._local_edge_reasoning(context_docs, domain, language)

    def _call_gemini(self, prompt: str, context_docs: List[Dict[str, Any]], domain: str, language: str) -> Optional[str]:
        if not self.gemini_key:
            return None

        persona = AGENT_PERSONAS.get(domain, AGENT_PERSONAS["farmer_scheme"])
        lang_name = LANGUAGE_NAMES.get(language, "English")

        # Format context into clean facts
        context_str = ""
        citations_list = []
        if context_docs:
            facts = []
            for d in context_docs[:6]:
                title = d.get("title") or d.get("scheme_name") or d.get("act_name") or d.get("category", "")
                summary = d.get("summary") or d.get("overview") or d.get("description") or d.get("financial_benefit", "")
                facts.append(f"- **{title}**: {summary}")
                if "citations" in d:
                    citations_list.extend(d["citations"])
                if "legal_sections" in d:
                    citations_list.extend(d["legal_sections"])
            context_str = "\n".join(facts)

        system_instruction = (
            f"{persona}\n"
            f"Target Output Language: {lang_name}.\n"
            "STRICT OPERATIONAL DIRECTIVES:\n"
            "1. Answer authoritatively, directly, and comprehensively with rich formatting (bold headings, structured scheme breakdown, key eligibility, document checklists, and application steps).\n"
            "2. Ensure all guidance aligns with official Indian cooperative laws, Ministry of Agriculture & Farmers Welfare, PMFBY, RBI/NABARD guidelines, and State Agriculture departments.\n"
            "3. If the farmer asks for eligible schemes or general assistance, present all relevant flagship central and state schemes clearly.\n"
            f"4. Respond naturally and fully in {lang_name}.\n"
            "5. CRITICAL: Do NOT output internal thought processes, planning notes, or meta-comments. Output ONLY the complete, direct, final advisory for the user."
        )

        user_content = (
            f"Verified Official Statutory Context:\n{context_str}\n\n"
            f"Farmer / Citizen Query:\n{prompt}\n\n"
            f"Generate a comprehensive, complete, structured, and legally accurate advisory in {lang_name}:"
        )

        payload = {
            "system_instruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": [{
                "role": "user",
                "parts": [{"text": user_content}]
            }],
            "generationConfig": {
                "temperature": 0.25,
                "topP": 0.95,
                "maxOutputTokens": 3500
            }
        }

        data_bytes = json.dumps(payload).encode("utf-8")

        for model_name in self.gemini_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.gemini_key}"
            req = urllib.request.Request(
                url,
                data=data_bytes,
                headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(req, timeout=12.0) as resp:
                    if resp.status == 200:
                        res_json = json.loads(resp.read().decode("utf-8"))
                        candidates = res_json.get("candidates", [])
                        if candidates and "content" in candidates[0]:
                            parts = candidates[0]["content"].get("parts", [])
                            if parts and "text" in parts[0]:
                                text_output = parts[0]["text"].strip()
                                # Append verified citations if not already present
                                if citations_list and "🏛️" not in text_output and "Verified" not in text_output and "சான்றாதாரங்கள்" not in text_output:
                                    unique_cites = list(dict.fromkeys(citations_list))[:4]
                                    text_output += f"\n\n🏛️ **Verified Sources / Citations:** {', '.join(unique_cites)}"
                                return text_output
            except Exception as e:
                # Silently try next model or fallback
                continue

        return None

    def _call_groq(self, prompt: str) -> Optional[str]:
        if not self.groq_key:
            return None
        try:
            import httpx
            resp = httpx.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {self.groq_key}"},
                json={
                    "model": "openai/gpt-oss-120b",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2
                },
                timeout=8.0
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            pass
        return None

    def _local_edge_reasoning(self, docs: List[Dict[str, Any]], domain: str, language: str) -> str:
        if not docs:
            if language == "ta":
                return "உங்கள் வினவலுக்குரிய அதிகாரப்பூர்வ கூட்டுறவு ஆவணம் கண்டறியப்படவில்லை. தயவுசெய்து உங்கள் உள்ளூர் தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS) அல்லது கூட்டுறவு சங்கங்களின் துணைப் பதிவாளரை அணுகவும்."
            elif language == "hi":
                return "आपके प्रश्न से संबंधित कोई आधिकारिक सहकारी रिकॉर्ड नहीं मिला। कृपया अपने स्थानीय प्राथमिक कृषि ऋण समिति (PACS) सचिव या सहायक रजिस्ट्रार से संपर्क करें।"
            return "No matching official cooperative record found for your exact query. Please consult your local Assistant Registrar of Cooperative Societies (ARCS) or PACS Secretary."

        primary_doc = docs[0]
        title = primary_doc.get("title") or primary_doc.get("scheme_name") or primary_doc.get("act_name") or primary_doc.get("category", "Cooperative Advisory")
        summary = primary_doc.get("summary") or primary_doc.get("overview") or primary_doc.get("financial_benefit") or primary_doc.get("description", "")
        provisions = primary_doc.get("key_provisions") or primary_doc.get("eligibility_criteria") or primary_doc.get("permitted_activities") or primary_doc.get("risk_coverage") or []
        
        response_lines = [
            f"### 📌 {title}",
            f"\n**Overview & Guidance:**\n{summary}\n"
        ]

        if provisions:
            response_lines.append("**Key Provisions / Guidelines:**")
            for item in provisions[:4]:
                response_lines.append(f"- {item}")

        if "critical_deadlines" in primary_doc:
            deadlines = primary_doc["critical_deadlines"]
            response_lines.append(f"\n⚠️ **Mandatory Time Limits:** {deadlines.get('intimation_period', 'Immediate')}")

        if "statutory_timeline" in primary_doc:
            response_lines.append(f"\n⏱️ **Statutory Resolution Timeline:** {primary_doc['statutory_timeline']}")

        citations = primary_doc.get("citations", [])
        if citations:
            response_lines.append(f"\n🏛️ **Verified Legal Sources:** {', '.join(citations)}")

        return "\n".join(response_lines)
