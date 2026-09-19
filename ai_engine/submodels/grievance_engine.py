"""
Specialized Grievance Redressal Sub-Model Engine for Cooperative AI Portal.
Handles grievance classification, 4-step statutory remedies, legal escalation ladders,
competent override authorities, evidence checklists, and auto-generated ready-to-print
formal legal complaint/petition drafts across Indian languages.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class GrievanceEngine:
    def __init__(self):
        self.grievances_catalog: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        catalog_path = os.path.join(settings.DATABASE_PATH, "grievances", "grievance_catalog.json")
        if os.path.exists(catalog_path):
            try:
                with open(catalog_path, "r", encoding="utf-8") as f:
                    self.grievances_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading grievances catalog: {e}")

    def find_matching_grievance(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        triggers = {
            "PACS_LOAN_DELAY": ["loan delay", "loan denied", "refused loan", "delaying loan", "loan sanction", "pending loan", "लोन में देरी", "ऋण देने से मना", "கடன் தாமதம்", "రుణం ఆలస్యం", "कर्ज नकार"],
            "PMFBY_PREMIUM_DEFAULT": ["pmfby default", "premium not paid by pacs", "bank default", "insurance rejected", "crop insurance claim not received", "डाटा नॉट फाउंड", "प्रीमियम जमा नहीं किया", "காப்பீடு நிராகரிப்பு", "బీమా క్లెయిమ్ రాలేదు"],
            "FERTILIZER_OVERCHARGING_BUNDLING": ["mrp", "fertilizer overcharging", "bundling", "urea price", "dap price", "black market", "खाद अधिक दाम", "यूरिया अधिक मूल्य", "உரம் கூடுதல் விலை", "ఎరువుల ఎక్కువ ధర", "खतांचा काळाबाजार"],
            "MEMBERSHIP_DENIAL_POLITICAL": ["membership denied", "refused membership", "cancel membership", "member banaya nahi", "सदस्यता देने से इनकार", "உறுப்பினர் சேர்க்கை மறுப்பு", "సభ్యత్వం నిరాకరణ", "सभासदत्व नकार"],
            "BRIBE_CORRUPTION_COMMISSION": ["bribe", "corruption", "cut", "commission", "asking money", "demand money", "रिश्वत", "घूस", "கமிஷன்", "லஞ்சம்", "లంచం", "लाच मागितली"],
            "NO_DUES_CERTIFICATE_DELAY": ["no dues", "noc", "title deed", "land deed", "mortgage release", "एनओसी", "नो ड्यूज", "நோ டியூஸ்", "నో డ్యూస్", "कागदपत्रे परत"],
            "COOP_ELECTION_VOTER_FRAUD": ["election", "voter list", "electoral roll", "voting right", "चुनाव", "मतदाता सूची", "தேர்தல் முறைகேடு", "ఎన్నికల ఓటర్ జాబితా", "निवडणूक गैरव्यवहार"],
            "DIVIDEND_SHARE_WITHHOLDING": ["dividend", "bonus", "share money", "लाभांश", "डिविडेंड", "பங்கு லாபம்", "డివిడెండ్", "लाभांश मिळाला नाही"],
            "UNAUTHORIZED_BANK_DEDUCTIONS": ["unauthorized deduction", "hidden charges", "insurance deducted without permission", "खाते से अवैध कटौती", "அனுமதியின்றி பிடித்தம்", "ఖాతా నుండి అనధికారిక కట్", "विनापरवानगी पैसे कपात"],
            "FINANCIAL_FRAUD_MISAPPROPRIATION": ["embezzlement", "fraud", "scam", "bogus loan", "gaban", "घोटाला", "फर्जी लोन", "முறைகேடு", "మోసం", "पैशांची अफरातफर"]
        }

        for item in self.grievances_catalog:
            code = item.get("grievance_code", "")
            kw_list = triggers.get(code, [])
            score = 0
            for kw in kw_list:
                if kw in q_lower:
                    score += 4 if " " in kw else 2

            if score > 0:
                scored.append((score, item))

        if scored:
            scored.sort(key=lambda x: x[0], reverse=True)
            return [s[1] for s in scored]

        return self.grievances_catalog[:2]

    def generate_grievance_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_grievance(query)
        primary = matched[0]

        guidance_text = self._format_grievance_response(primary, language)

        return {
            "matched_grievances": [g.get("category") for g in matched],
            "primary_grievance": primary,
            "guidance_text": guidance_text,
            "statutory_remedy": primary.get("statutory_remedy"),
            "override_authority": primary.get("override_authority"),
            "legal_sections": primary.get("legal_sections", []),
            "sla_days": primary.get("sla_days", 15),
            "required_evidence": primary.get("required_evidence", []),
            "penalty_on_violator": primary.get("penalty_on_violator"),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_grievance_response(self, g: Dict[str, Any], language: str) -> str:
        cat = g.get("category", "Cooperative Grievance")
        code = g.get("grievance_code", "GRV")
        problem = g.get("problem_statement", "")
        remedy = g.get("statutory_remedy", "")
        override = g.get("override_authority", "")
        sections = ", ".join(g.get("legal_sections", []))
        sla = g.get("sla_days", 15)
        evidence = g.get("required_evidence", [])
        ladder = g.get("escalation_ladder", [])
        penalty = g.get("penalty_on_violator", "")

        evidence_fmt = "\n".join([f"  - {e}" for e in evidence])
        ladder_fmt = "\n".join([f"  • **Level {l['level']} ({l['authority']} - {l['timeline']})**: {l['action']}" for l in ladder])

        if language == "hi":
            return (
                f"### ⚖️ कानूनी शिकायत निवारण एवं समाधान: {cat}\n\n"
                f"**🔍 समस्या विश्लेषण:**\n{problem}\n\n"
                f"**🛡️ वैधानिक समाधान एवं आपके अधिकार:**\n{remedy}\n\n"
                f"**🪜 3-स्तरीय अपीलीय सीढ़ी (SLA समय सीमा: {sla} दिन):**\n{ladder_fmt}\n\n"
                f"**📁 अनिवार्य साक्ष्य चेकलिस्ट:**\n{evidence_fmt}\n\n"
                f"**🏛️ सक्षम अपीलीय अधिकारी:** {override}\n"
                f"**📜 कानूनी धाराएं:** {sections}\n"
                f"**⚠️ दोषी अधिकारी पर कार्रवाई:** {penalty}\n\n"
                f"📝 **औपचारिक शिकायत प्रारूप (Petition Draft):**\n"
                f"```text\n"
                f"सेवा में,\n"
                f"श्रीमान {override}\n"
                f"विषय: {cat} के संबंध में वैधानिक शिकायत - धारा {sections}\n\n"
                f"महोदय,\n"
                f"मैं प्राथमिक कृषि ऋण समिति (PACS) का सदस्य हूँ। {problem}\n"
                f"नागरिक अधिकार पत्र (Citizen Charter) के तहत निर्धारित {sla} दिनों में कोई समाधान नहीं हुआ है।\n"
                f"प्रार्थना: कृपया {sections} के तहत तत्काल राहत प्रदान करें और दोषी अधिकारी के विरुद्ध विभागीय जांच का आदेश दें।\n\n"
                f"भवदीय,\n"
                f"[आवेदक का नाम, हस्ताक्षर एवं मोबाइल]\n"
                f"```"
            )
        elif language == "ta":
            return (
                f"### ⚖️ சட்டப்பூர்வ தீர்வு மற்றும் புகார் நடைமுறை: {cat}\n\n"
                f"**🔍 பிரச்சனை விபரம்:**\n{problem}\n\n"
                f"**🛡️ சட்டப்பூர்வ தீர்வு மற்றும் உங்கள் உரிமைகள்:**\n{remedy}\n\n"
                f"**🪜 மேல்முறையீட்டு படிநிலைகள் (SLA: {sla} நாட்கள்):**\n{ladder_fmt}\n\n"
                f"**📁 தேவையான ஆதாரங்கள்:**\n{evidence_fmt}\n\n"
                f"**🏛️ மேல்முறையீட்டு அதிகாரி:** {override}\n"
                f"**📜 சட்டப் பிரிவுகள்:** {sections}\n"
                f"**⚠️ விதிமீறலுக்கான தண்டனை:** {penalty}"
            )
        else:
            return (
                f"### ⚖️ Statutory Grievance Resolution & Legal Remedy: {cat} ({code})\n\n"
                f"**🔍 Problem Analysis:**\n{problem}\n\n"
                f"**🛡️ Statutory Remedy & Farmer Rights:**\n{remedy}\n\n"
                f"**🪜 3-Tier Escalation Ladder & Time Limits (SLA: {sla} Days):**\n{ladder_fmt}\n\n"
                f"**📁 Mandatory Evidence Checklist:**\n{evidence_fmt}\n\n"
                f"**🏛️ Competent Override Authority:** {override}\n"
                f"**📜 Applicable Statutory Laws:** {sections}\n"
                f"**⚠️ Penalties on Violator:** {penalty}\n\n"
                f"**📝 Ready-to-Print Legal Petition Draft:**\n"
                f"```text\n"
                f"To,\n"
                f"The Competent Authority / {override}\n\n"
                f"Subject: Formal Statutory Petition regarding {cat} under {sections} - Reg.\n\n"
                f"Respected Sir/Madam,\n"
                f"I am a member of the Primary Agricultural Credit Society (PACS). {problem}\n"
                f"Despite representations, the service has been unlawfully withheld beyond the statutory timeline of {sla} days.\n\n"
                f"PRAYER / RELIEF SOUGHT:\n"
                f"1. Direct immediate sanction/redressal under the powers vested under {sections}.\n"
                f"2. Initiate disciplinary action against the responsible officer.\n"
                f"3. Award compensation for harassment and financial loss.\n\n"
                f"Yours sincerely,\n"
                f"[Applicant Name, Signature, Member ID & Mobile]\n"
                f"```"
            )
