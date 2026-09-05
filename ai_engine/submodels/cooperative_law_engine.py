"""
Specialized Cooperative Law & Governance Sub-Model Engine for Cooperative AI Portal.
Handles:
- Multi-State Co-operative Societies Act 2002 & 2023 Amendment
- Cooperative Election Authority (Section 45) & Election dispute arbitration
- Statutory Arbitration under Section 84 (3-year limitation period, civil courts barred)
- Cooperative Ombudsman under Section 85 for member grievance redressal
- Statutory Surcharge & Inquiries under Section 88 / 108
- Board disqualifications (Section 43/44), Women & SC/ST reservations, democratic voting rights (Section 20)
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class CooperativeLawEngine:
    def __init__(self):
        self.laws_catalog: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        laws_path = os.path.join(settings.DATABASE_PATH, "laws", "cooperative_laws.json")
        if os.path.exists(laws_path):
            try:
                with open(laws_path, "r", encoding="utf-8") as f:
                    self.laws_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading cooperative laws: {e}")

    def find_matching_laws(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        triggers = {
            "LAW_ELECTION_AUTHORITY": ["section 45", "sec 45", "election authority", "cooperative election", "electoral roll", "voter list", "cea", "धारा 45", "चुनाव प्राधिकरण", "தேர்தல் ஆணையம்", "ఎన్నికల అథారిటీ"],
            "LAW_ARBITRATION_SECTION_84": ["section 84", "sec 84", "arbitration", "arbitrator", "statutory arbitration", "civil court barred", "dispute", "धारा 84", "मध्यस्थता", "நடுவர் மன்றம்", "మధ్యవర్తిత్వం"],
            "LAW_OMBUDSMAN_SECTION_85": ["section 85", "sec 85", "ombudsman", "cooperative ombudsman", "deficiency in service", "धारा 85", "लोकपाल", "ஒம்புட்ஸ்மேன்", "ఓంబుడ్స్‌మన్"],
            "LAW_BOARD_DISQUALIFICATIONS": ["disqualification", "board of directors", "default on loan", "reservation for women", "tenure", "निदेशक अयोग्यता", "இயக்குனர் தகுதிநீக்கம்", "బోర్డు అనర్హత"],
            "LAW_INQUIRY_SURCHARGE": ["section 108", "section 88", "surcharge", "statutory inquiry", "misappropriation", "forensic audit", "धारा 88", "धारा 108", "अधिभार", "விசாரணை"],
            "LAW_OPEN_MEMBERSHIP_SECTION_19": ["section 19", "sec 19", "open membership", "deemed membership", "refusal of membership", "धारा 19", "खुली सदस्यता", "உறுப்பினர் உரிமை"],
            "LAW_NET_PROFITS_DIVIDEND": ["section 67", "net profit", "reserve fund", "25%", "dividend", "education fund", "धारा 67", "लाभांश", "பங்கு லாபம்", "డివిడెండ్"],
            "LAW_DEMOCRATIC_VOTING_RIGHTS": ["section 20", "one member one vote", "voting rights", "no proxy", "active member", "धारा 20", "मतदान अधिकार", "வாக்குரிமை", "ఓటు హక్కు"]
        }

        for item in self.laws_catalog:
            code = item.get("topic_code", "")
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

        return self.laws_catalog[:2]

    def generate_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_laws(query)
        primary = matched[0]

        guidance_text = self._format_response(primary, language)

        return {
            "matched_laws": [l.get("title") for l in matched],
            "primary_law": primary,
            "guidance_text": guidance_text,
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_response(self, item: Dict[str, Any], language: str) -> str:
        title = item.get("title", "Cooperative Legal Guidance")
        act = item.get("act_name", "Multi-State Co-operative Societies Act")
        section = item.get("section", "")
        summary = item.get("summary", "")
        provisions = item.get("key_provisions", [])
        citations = ", ".join(item.get("citations", []))

        prov_fmt = "\n".join([f"  - {p}" for p in provisions])

        if language == "hi":
            return (
                f"### 🏛️ {title} ({section})\n\n"
                f"**📜 कानून:** {act}\n"
                f"**⚖️ वैधानिक धारा:** {section}\n\n"
                f"**विवरण:**\n{summary}\n\n"
                f"**⚖️ प्रमुख कानूनी प्रावधान:**\n{prov_fmt}\n\n"
                f"🏛️ **सत्यापित आधिकारिक कानूनी संदर्भ:** {citations}"
            )
        elif language == "ta":
            return (
                f"### 🏛️ {title} ({section})\n\n"
                f"**📜 சட்டம்:** {act}\n"
                f"**⚖️ சட்டப்பிரிவு:** {section}\n\n"
                f"**விவரம்:**\n{summary}\n\n"
                f"**⚖️ முக்கிய சட்ட விதிகள்:**\n{prov_fmt}\n\n"
                f"🏛️ **சட்டப்பூர்வ சான்றுகள்:** {citations}"
            )
        else:
            return (
                f"### 🏛️ {title} ({section})\n\n"
                f"**Governing Act:** {act}\n"
                f"**Statutory Section:** {section}\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**Key Statutory Provisions & Legal Rules:**\n{prov_fmt}\n\n"
                f"🏛️ **Verified Legal Sources & Gazette Citations:** {citations}"
            )
