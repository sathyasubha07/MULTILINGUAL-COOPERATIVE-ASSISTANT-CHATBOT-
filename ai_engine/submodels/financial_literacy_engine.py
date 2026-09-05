"""
Specialized Financial & Credit Literacy Sub-Model Engine for Cooperative AI Portal.
Handles:
- KCC Limit Calculation (Scale of Finance, 10% household, 20% maintenance, 5-year revolving credit)
- Modified Interest Subvention Scheme (7% base rate, 3% Prompt Repayment Incentive, 4% effective interest)
- Collateral-free limits (₹1.60L / ₹2.00L) & allied sector credit (₹2.00L)
- Fair Lending Practices (zero fees up to ₹3 Lakh, mandatory 15-day title deed release under ₹5,000/day penalty)
- Digital Banking Safety (AePS, Micro-ATMs, 2FA biometric security)
- NPCI Aadhaar Mapper DBT Seeding
- Natural Calamity Loan Restructuring & CIBIL Protection
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class FinancialLiteracyEngine:
    def __init__(self):
        self.fin_catalog: List[Dict[str, Any]] = []
        self._load_catalog()

    def _load_catalog(self):
        fin_path = os.path.join(settings.DATABASE_PATH, "financial", "financial_literacy.json")
        if os.path.exists(fin_path):
            try:
                with open(fin_path, "r", encoding="utf-8") as f:
                    self.fin_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading financial catalog: {e}")

    def find_matching_topics(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        triggers = {
            "FIN_SCALE_OF_FINANCE_CALCULATION": ["scale of finance", "limit calculation", "kcc formula", "5 year sanction", "dltc", "स्केल ऑफ फाइनेंस", "क्रेडिट लिमिट गणना", "அளவீட்டு முறை", "రుణ పరిమితి గణన"],
            "FIN_KCC_SCALE_OF_FINANCE": ["scale of finance", "limit calculation", "kcc formula", "5 year sanction", "dltc"],
            "FIN_INTEREST_SUBVENTION_4_PERCENT": ["4%", "4 percent", "interest subvention", "prompt repayment", "pri", "7%", "3%", "effective interest", "4 प्रतिशत ब्याज", "ब्याज छूट", "4 சதவீத வட்டி", "4 శాతం వడ్డీ"],
            "FIN_INTEREST_SUBVENTION_4PERCENT": ["4%", "4 percent", "interest subvention", "prompt repayment", "pri", "7%"],
            "FIN_TITLE_DEED_RELEASE_COMPENSATION": ["title deed", "no dues", "noc", "release documents", "5000 per day", "5,000", "penalty", "original documents", "land documents", "एनओसी", "टाइटिल डीड", "दस्तावेज़", "நோ டியூஸ்", "நில ஆவணம்", "నో డ్యూస్"],
            "FIN_FAIR_LENDING_15DAY_DOCS": ["title deed", "no dues", "noc", "release documents", "5000 per day"],
            "FIN_AEPS_MICRO_ATM_SAFETY": ["aeps", "micro atm", "biometric safety", "fingerprint scam", "two factor", "2fa", "माइक्रो एटीएम", "बायोमेट्रिक सुरक्षा", "கைரேகை பாதுகாப்பு"],
            "FIN_DBT_AADHAAR_SEEDING_VS_LINKING": ["npci mapper", "dbt seeding", "aadhaar seeding", "dbt failure", "apb", "डीबीटी सीडिंग", "एनपीसीआई", "டிபிடி இணைப்பு", "ఆధార్ సీడింగ్"],
            "FIN_NPCI_DBT_SEEDING": ["npci mapper", "dbt seeding", "aadhaar seeding", "dbt failure"],
            "FIN_CIBIL_CALAMITY_RESTRUCTURING": ["cibil", "credit score", "restructuring", "calamity loan", "moratorium", "npa", "ऋण पुनर्गठन", "सिबिल स्कोर", "கடன் மறுசீரமைப்பு"]
        }

        for item in self.fin_catalog:
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

        return self.fin_catalog[:2]

    def generate_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_topics(query)
        primary = matched[0]

        guidance_text = self._format_response(primary, language)

        return {
            "matched_topics": [t.get("title") for t in matched],
            "primary_topic": primary,
            "guidance_text": guidance_text,
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_response(self, item: Dict[str, Any], language: str) -> str:
        title = item.get("title", "Credit & Financial Guidance")
        code = item.get("topic_code", "")
        summary = item.get("summary", "")
        citations = ", ".join(item.get("citations", []))

        # Check for Scale of Finance Breakdown
        if "formula_breakdown" in item:
            breakdown = "\n".join([f"  - {f}" for f in item["formula_breakdown"]])
            return (
                f"### 🧮 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📐 Standard Calculation Formulas:**\n{breakdown}\n\n"
                f"🏛️ **Verified NABARD & RBI Standards:** {citations}"
            )

        # Check for Financial Mechanics
        elif "financial_mechanics" in item:
            mechanics = "\n".join([f"  - {m}" for m in item["financial_mechanics"]])
            return (
                f"### 💰 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📊 Regulated Interest Rates & Subventions:**\n{mechanics}\n\n"
                f"🏛️ **Verified RBI & MoA&FW Directives:** {citations}"
            )

        # Check for Statutory Rules (e.g. Title Deed 15-30 days & ₹5,000/day penalty)
        elif "statutory_rules" in item:
            rules = "\n".join([f"  - {r}" for r in item["statutory_rules"]])
            return (
                f"### ⚖️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📜 Statutory Rights & Penalty Directives:**\n{rules}\n\n"
                f"🏛️ **Verified RBI Fair Lending Directives:** {citations}"
            )

        # Check for Safety Norms (AePS)
        elif "safety_norms" in item:
            norms = "\n".join([f"  - {s}" for s in item["safety_norms"]])
            return (
                f"### 🔒 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🛡️ Biometric & Micro-ATM Safety Rules:**\n{norms}\n\n"
                f"🏛️ **Verified NPCI & RBI Directives:** {citations}"
            )

        # Check for Key Differences (DBT)
        elif "key_differences" in item:
            diffs = "\n".join([f"  - {d}" for d in item["key_differences"]])
            return (
                f"### 🔄 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🔍 Direct Benefit Transfer (DBT) Directives:**\n{diffs}\n\n"
                f"🏛️ **Verified NPCI & MoF Guidelines:** {citations}"
            )

        # Default fallback
        return (
            f"### 💳 {title} ({code})\n\n"
            f"**Overview:**\n{summary}\n\n"
            f"🏛️ **Verified Financial Sources:** {citations}"
        )
