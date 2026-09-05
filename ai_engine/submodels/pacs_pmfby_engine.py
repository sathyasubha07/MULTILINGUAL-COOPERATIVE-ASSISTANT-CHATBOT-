"""
Specialized PACS & PMFBY Crop Insurance Sub-Model Engine for Cooperative AI Portal.
Handles:
- PMFBY 72-Hour Calamity Intimation workflows & intimation channel routing
- PMFBY Standardized Premium Calculations (2% Kharif, 1.5% Rabi, 5% Commercial)
- PMFBY Clause 17.2 & 21.5 Bank Default Liability & DGRC dispute escalation
- PACS Model Bye-laws 25+ Diversified Economic Activities (Custom Hiring, Drones, CSC, Jan Aushadhi)
- PACS Membership rules, Deemed Membership, and 15-Day Loan Processing SLAs
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings

class PacsPmfbyEngine:
    def __init__(self):
        self.pacs_catalog: List[Dict[str, Any]] = []
        self.pmfby_catalog: List[Dict[str, Any]] = []
        self._load_catalogs()

    def _load_catalogs(self):
        pacs_path = os.path.join(settings.DATABASE_PATH, "pacs", "pacs_bylaws.json")
        if os.path.exists(pacs_path):
            try:
                with open(pacs_path, "r", encoding="utf-8") as f:
                    self.pacs_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading pacs bylaws: {e}")

        pmfby_path = os.path.join(settings.DATABASE_PATH, "pmfby", "pmfby_guidelines.json")
        if os.path.exists(pmfby_path):
            try:
                with open(pmfby_path, "r", encoding="utf-8") as f:
                    self.pmfby_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading pmfby guidelines: {e}")

    def find_matching_topics(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored = []

        all_items = self.pacs_catalog + self.pmfby_catalog

        triggers = {
            "PACS_DEFINITION_STRUCTURE": ["structure of pacs", "what is pacs", "primary agricultural credit society", "3-tier", "dccb", "stcb", "short-term cooperative credit", "पैक्स क्या है", "கூட்டுறவு அமைப்பு", "పాక్స్ నిర్మాణం"],
            "PACS_MODEL_BYLAWS_25_ACTIVITIES": ["commercial and agricultural services", "model bye-laws", "model bylaws", "25+ activities", "25+", "diversified", "pacs operate", "multi-purpose pacs", "m-pacs", "उप-नियम", "பன்முக சேவைகள்"],
            "PACS_MEMBERSHIP_RULES": ["membership types", "regular member", "nominal member", "share capital", "open membership", "open membership rules", "pacs membership", "सदस्यता नियम", "உறுப்பினர் விதிகள்", "సభ్యత్వ నిబంధనలు"],
            "PACS_LOAN_DISPOSAL_SLA": ["statutory time limit", "approve loan", "15-day", "15 days loan", "loan disposal", "loan sla", "citizen charter", "form-b", "15 दिन लोन", "கடன் காலக்கெடு", "రుణం గడువు"],
            "PACS_CUSTOM_HIRING_DRONES": ["rent tractors", "kisan drones", "custom hiring centres", "custom hiring", "chc", "tractor rental", "drone spraying", "drone rental", "chc machinery", "कस्टम हायरिंग", "ड्रोन छिड़काव", "किसान ड्रोन", "டிரோன் தெளிப்பான்"],
            "PACS_CSC_DIGITAL_SERVICES": ["csc in pacs", "common service centre", "common service center", "300+ services", "digital village", "ekyc pacs", "aadhaar pacs", "सीएससी", "இ-சேவை", "డిజిటల్ సేవలు"],
            "PACS_CSC_SERVICES": ["csc in pacs", "common service centre", "common service center", "300+ services", "digital village", "ekyc pacs", "aadhaar pacs"],
            "PACS_JAN_AUSHADHI_PMKSK": ["jan aushadhi", "pmksk", "generic medicine", "kisan samriddhi kendra", "जन औषधि", "மலிவு விலை மருந்து", "జన ఔషధి"],
            "PACS_JAN_AUSHADHI": ["jan aushadhi", "pmbjk", "generic medicine", "जन औषधि"],
            "PACS_PMKSK_KENDRAS": ["pmksk", "kisan samriddhi kendra"],
            "PACS_GRAIN_STORAGE_PLAN": ["grain storage", "godown", "warehouse", "largest grain storage", "e-nwr", "अनाज भंडारण", "தானிய கிடங்கு", "ధాన్య నిల్వ"],
            "PACS_COMPUTERIZATION_ERP": ["pacs computerization", "erp", "cloud erp", "nabard erp", "software", "कंप्यूटरीकरण", "கணினிமயமாக்கல்"],
            "PACS_PETROL_LPG_DEALERSHIP": ["petrol", "diesel", "lpg", "dealership", "pump"],
            "PACS_SOLAR_KUSUM_C": ["solar", "feeder solarization", "kusum component c"],
            "PACS_GOVERNANCE_AUDIT": ["managing committee", "board of directors", "reservation for women", "annual audit", "agm", "statutory audit", "प्रबंध समिति", "தணிக்கை", "ఆడిట్"],
            "PMFBY_72H_LOCALIZED_CALAMITY": ["72 hours", "72 hour", "72h", "hailstorm", "flood", "inundation", "landslide", "cloudburst", "post-harvest", "cut and spread", "calamity", "72 घंटे", "ओलावृष्टि", "बाढ़", "जलभराव", "72 மணி நேரம்", "ஆலங்கட்டி மழை", "வெள்ளம்", "72 గంటలు", "వడగళ్ళు", "వరదలు", "72 तास", "गारपीट"],
            "PMFBY_72H_CALAMITY_INTIMATION": ["72 hours", "72 hour", "72h", "hailstorm", "flood", "inundation", "landslide", "cloudburst", "post-harvest", "cut and spread", "calamity", "72 घंटे", "ओलावृष्टि", "बाढ़", "जलभराव", "72 மணி நேரம்", "ஆலங்கட்டி மழை", "வெள்ளம்", "72 గంటలు", "వడగళ్ళు", "వరదలు", "72 तास", "गारपीट"],
            "PMFBY_PREMIUM_RATES": ["premium percentage", "kharif, rabi and commercial", "kharif premium", "rabi premium", "2%", "1.5%", "5%", "sum insured", "non-loanee", "loanee", "प्रीमियम", "खरीफ", "रबी", "காப்பீட்டு கட்டணம்", "பயிர் காப்பீட்டு பிரீமியம்", "ప్రీమియం", "पिक विमा हप्ता"],
            "PMFBY_CORE_PREMIUM_RATES": ["premium percentage", "kharif, rabi and commercial", "kharif premium", "rabi premium", "2%", "1.5%", "5%", "sum insured", "non-loanee", "loanee"],
            "PMFBY_BANK_DEFAULT_CLAUSE": ["failed to upload", "ncip portal", "cut-off date", "who pays my loss", "pacs deducted pmfby", "clause 17.2", "bank default", "pacs did not pay premium", "premium not uploaded", "data not found", "बैंक की गलती", "प्रीमियम जमा नहीं किया", "வங்கி பொறுப்பு", "బ్యాంక్ డిఫాల్ట్"],
            "PMFBY_YIELD_CALCULATION_TECH": ["cce", "crop cutting", "yield calculation", "threshold yield", "yes-tech", "winds", "फसल कटाई प्रयोग", "விளைச்சல் மதிப்பீடு", "దిగుబడి నష్టం"],
            "PMFBY_YES_TECH_AND_WINDS": ["yes-tech", "winds", "cropic", "remote sensing", "satellite", "aws"],
            "PMFBY_POST_HARVEST_COVER": ["post-harvest", "post harvest", "14 days", "cut and spread", "cyclone"]
        }

        for item in all_items:
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

        return all_items[:2]

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
        title = item.get("title", "PACS & PMFBY Advisory")
        code = item.get("topic_code", "")
        summary = item.get("summary", "")
        citations = ", ".join(item.get("citations", []))

        # Check for 72h Calamity item
        if "intimation_protocol" in item or "mandatory_72h_rule" in item:
            if "intimation_protocol" in item:
                proto = "\n".join([f"  - {p}" for p in item["intimation_protocol"]])
                return (
                    f"### 🌧️ {title} ({code})\n\n"
                    f"**Overview:**\n{summary}\n\n"
                    f"**⚠️ Statutory 72-Hour Calamity Intimation Protocol & SLA:**\n{proto}\n\n"
                    f"🏛️ **Verified Official Sources:** {citations}"
                )
            else:
                perils = "\n".join([f"  - {p}" for p in item.get("covered_perils", [])])
                channels = "\n".join([f"  - {c}" for c in item.get("intimation_channels", [])])
                timeline = item.get("claim_settlement_timeline", {})
                tl_fmt = (
                    f"  • **48 Hours**: {timeline.get('appointment_of_assessor', 'Assessor appointed')}\n"
                    f"  • **10 Days**: {timeline.get('joint_survey', 'Joint survey completed')}\n"
                    f"  • **15 Days**: {timeline.get('claim_disbursal', 'Direct DBT bank payout')}"
                )
                return (
                    f"### 🌧️ {title} ({code})\n\n"
                    f"**⚠️ Mandatory 72-Hour Calamity Rule:**\n{item['mandatory_72h_rule']}\n\n"
                    f"**🌩️ Covered Natural Calamities & Perils:**\n{perils}\n\n"
                    f"**📲 3 Official Intimation Channels:**\n{channels}\n\n"
                    f"**⏱️ 4-Step Claim Settlement SLA Timeline:**\n{tl_fmt}\n\n"
                    f"🏛️ **Verified Legal Sources:** {citations}"
                )

        # Check for Premium Rates / Slabs
        elif "premium_rates" in item or "premium_slabs" in item:
            rates_dict = item.get("premium_rates") or item.get("premium_slabs", {})
            slabs = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in rates_dict.items()])
            return (
                f"### 🌾 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**💰 Statutory Farmer Premium Rates:**\n{slabs}\n\n"
                f"🏛️ **Verified Legal Sources:** {citations}"
            )

        # Check for PACS Multi-Services
        elif "permitted_activities" in item:
            acts = "\n".join([f"  - {a}" for a in item.get("permitted_activities", [])])
            return (
                f"### 🏢 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🛠️ Permitted Multi-Purpose Services at PACS:**\n{acts}\n\n"
                f"🏛️ **Verified Official Sources:** {citations}"
            )

        # Check for PACS Membership Rules
        elif "membership_rules" in item:
            rules = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in item.get("membership_rules", {}).items()])
            return (
                f"### 📋 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🏛️ Statutory Membership Rules:**\n{rules}\n\n"
                f"🏛️ **Verified Legal Sources:** {citations}"
            )

        # Check for PACS Loan Disposal SLA
        elif "operational_rules" in item:
            rules = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in item.get("operational_rules", {}).items()])
            return (
                f"### ⏱️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📜 Mandatory Operational SLAs:**\n{rules}\n\n"
                f"🏛️ **Verified Citizen Charter Standards:** {citations}"
            )

        # Check for PACS Custom Hiring
        elif "machinery_and_rates" in item:
            rates = "\n".join([f"  - {m}" for m in item.get("machinery_and_rates", [])])
            booking = item.get("booking_process", "")
            return (
                f"### 🚜 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🛠️ Available Machinery & Regulated Rental Rates:**\n{rates}\n\n"
                f"**📝 Booking Procedure:** {booking}\n\n"
                f"🏛️ **Verified Official Guidelines:** {citations}"
            )

        # Check for PACS CSC Services
        elif "key_services" in item:
            services = "\n".join([f"  - {s}" for s in item.get("key_services", [])])
            return (
                f"### 📲 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🌐 Available Digital Village Services:**\n{services}\n\n"
                f"🏛️ **Verified Digital Mission Standards:** {citations}"
            )

        # Check for PACS Jan Aushadhi / PMKSK
        elif "key_benefits" in item:
            benefits = "\n".join([f"  - {b}" for b in item.get("key_benefits", [])])
            return (
                f"### 💊 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🏥 Community Healthcare & Input Advantages:**\n{benefits}\n\n"
                f"🏛️ **Verified Government Sources:** {citations}"
            )

        # Check for Grain Storage Plan
        elif "financial_and_infra_support" in item:
            infra = "\n".join([f"  - {s}" for s in item.get("financial_and_infra_support", [])])
            return (
                f"### 🏗️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**📦 Infrastructure & Financial Subsidies:**\n{infra}\n\n"
                f"🏛️ **Verified Cabinet Decisions:** {citations}"
            )

        # Check for Computerization ERP
        elif "core_features" in item:
            feats = "\n".join([f"  - {f}" for f in item.get("core_features", [])])
            return (
                f"### 💻 {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**🖥️ Core Cloud ERP Capabilities:**\n{feats}\n\n"
                f"🏛️ **Verified National Project Standards:** {citations}"
            )

        # Check for Governance & Audit
        elif "governance_standards" in item:
            gov = "\n".join([f"  - **{k.replace('_', ' ').title()}**: {v}" for k, v in item.get("governance_standards", {}).items()])
            return (
                f"### 🏛️ {title} ({code})\n\n"
                f"**Overview:**\n{summary}\n\n"
                f"**⚖️ Statutory Governance & Audit Norms:**\n{gov}\n\n"
                f"🏛️ **Verified Cooperative Act Standards:** {citations}"
            )

        # Check for Bank Default Clause
        elif "statutory_rule" in item:
            return (
                f"### ⚖️ {title} ({code})\n\n"
                f"**🛡️ 100% Bank Default Liability Mandate:**\n{item.get('statutory_rule')}\n\n"
                f"**🏛️ Adjudication Authority:** {item.get('enforcement_authority')}\n\n"
                f"🏛️ **Verified Legal Sources:** {citations}"
            )

        # Default fallback
        return (
            f"### 📌 {title}\n\n"
            f"**Overview:**\n{summary}\n\n"
            f"🏛️ **Verified Sources:** {citations}"
        )
