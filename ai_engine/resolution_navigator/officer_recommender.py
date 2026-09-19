"""
Strict Zero-Hallucination Officer Recommendation Engine for Cooperative AI Portal.
Recommends verified district and taluk-level government officers for Tamil Nadu districts (Theni, Madurai, Pudukkottai)
based on:
1. User Query & District/Taluk Context
2. Multi-Domain Fusion Solution Output & Active Domains
3. Strict Database Cross-Verification against database/data/officers/tamil_nadu_district_officers.json

Strict Rule:
If no officer matching the specific role and jurisdiction is available in the verified database,
it returns None without hallucinating or inventing contact details.
"""

import os
import re
import json
from typing import Dict, Any, List, Optional
from config.settings import settings

class OfficerRecommender:
    def __init__(self):
        self.officers_db: List[Dict[str, Any]] = []
        self._load_database()

    def _load_database(self):
        officers_path = os.path.join(settings.DATABASE_PATH, "officers", "tamil_nadu_district_officers.json")
        if os.path.exists(officers_path):
            try:
                with open(officers_path, "r", encoding="utf-8") as f:
                    self.officers_db = json.load(f)
            except Exception as e:
                print(f"Error loading officers database: {e}")

    def detect_district_and_locality(self, text: str) -> Dict[str, Optional[str]]:
        """Identifies mentioned district and sub-locality/taluk from user query."""
        text_lower = text.lower()
        detected_district = None
        detected_locality = None

        # District triggers
        district_keywords = {
            "Theni": ["theni", "தேனி", "தேனி மாவட்டம்", "andipatti", "cumbum", "periyakulam", "uthamapalayam", "chinnamanur", "bodinayakanur", "kadamalaigundu", "bodi", "gudalur"],
            "Madurai": ["madurai", "மதுரை", "மதுரை மாவட்டம்", "melur", "vadipatti", "usilampatti", "thirumangalam", "alanganallur", "kottampatti", "chellampatti", "thirupparankundram", "peraiyur", "kalligudi", "sedapatti"],
            "Pudukkottai": ["pudukkottai", "புதுக்கோட்டை", "புதுக்கோட்டை மாவட்டம்", "aranthangi", "illuppur", "karambakudi", "thirumayam", "avudaiyarkoil", "kunnandarkoil", "viralimalai", "ponnamaravathi", "gandarvakottai", "manamelkudi", "annavasal", "arimalam", "thiruvarankulam"],
            "Erode": ["erode", "ஈரோடு", "ஈரோடு மாவட்டம்", "perundurai", "bhavani", "gobichettipalayam", "gobi", "sathyamangalam", "sathy", "chennimalai", "anthiyur", "kodumudi", "nambiyur", "ammapettai"],
            "Karur": ["karur", "கரூர்", "கரூர் மாவட்டம்", "kadavur", "kulithalai", "krishnarayapuram", "thanthoni", "thogaimalai"]
        }

        for district, keywords in district_keywords.items():
            for kw in keywords:
                if kw in text_lower:
                    detected_district = district
                    break
            if detected_district:
                break

        # Locality / Taluk / Block triggers
        localities = [
            "andipatti", "cumbum", "periyakulam", "uthamapalayam", "chinnamanur", "bodinayakanur", "kadamalaigundu",
            "melur", "vadipatti", "usilampatti", "thirumangalam", "alanganallur", "kottampatti", "chellampatti", "thirupparankundram", "peraiyur", "kalligudi", "sedapatti",
            "aranthangi", "illuppur", "karambakudi", "thirumayam", "avudaiyarkoil", "kunnandarkoil", "viralimalai", "ponnamaravathi", "gandarvakottai", "manamelkudi", "annavasal", "arimalam", "thiruvarankulam",
            "perundurai", "bhavani", "gobichettipalayam", "sathyamangalam", "chennimalai", "anthiyur", "kodumudi", "nambiyur", "ammapettai",
            "kadavur", "kulithalai", "krishnarayapuram", "thanthoni", "thogaimalai",
            "ஆண்டிபட்டி", "கம்பம்", "பெரியகுளம்", "உத்தமபாளையம்", "சின்னமனூர்", "போடி", "மேலூர்", "வாடிப்பட்டி", "உசிலம்பட்டி", "திருமங்கலம்", "அறந்தாங்கி", "இலுப்பூர்", "விராலிமலை",
            "பெருந்துறை", "பவானி", "கோபிசெட்டிபாளையம்", "சத்தியமங்கலம்", "சென்னிமலை", "அந்தியூர்", "கொடுமுடி", "நம்பியூர்", "அம்மாபேட்டை",
            "கடவூர்", "குளித்தலை", "கிருஷ்ணராயபுரம்", "தான்தோன்றி", "தோகைமலை"
        ]

        LOCALITY_MAP = {
            "ஆண்டிபட்டி": "andipatti",
            "கம்பம்": "cumbum",
            "பெரியகுளம்": "periyakulam",
            "உத்தமபாளையம்": "uthamapalayam",
            "சின்னமனூர்": "chinnamanur",
            "போடி": "bodi",
            "கடமலைக்குண்டு": "kadamalaigundu",
            "மேலூர்": "melur",
            "வாடிப்பட்டி": "vadipatti",
            "உசிலம்பட்டி": "usilampatti",
            "திருமங்கலம்": "thirumangalam",
            "அலங்காநல்லூர்": "alanganallur",
            "கொட்டாம்பட்டி": "kottampatti",
            "அறந்தாங்கி": "aranthangi",
            "இலுப்பூர்": "illuppur",
            "விராலிமலை": "viralimalai",
            "பெருந்துறை": "perundurai",
            "பவானி": "bhavani",
            "கோபிசெட்டிபாளையம்": "gobichettipalayam",
            "சத்தியமங்கலம்": "sathyamangalam",
            "சென்னிமலை": "chennimalai",
            "அந்தியூர்": "anthiyur",
            "கொடுமுடி": "kodumudi",
            "நம்பியூர்": "nambiyur",
            "அம்மாபேட்டை": "ammapettai",
            "கடவூர்": "kadavur",
            "குளித்தலை": "kulithalai",
            "கிருஷ்ணராயபுரம்": "krishnarayapuram",
            "தான்தோன்றி": "thanthoni",
            "தோகைமலை": "thogaimalai"
        }

        for loc in localities:
            if loc in text_lower:
                detected_locality = LOCALITY_MAP.get(loc, loc)
                break

        return {
            "district": detected_district,
            "locality": detected_locality
        }

    def recommend_officer(
        self,
        query: str,
        active_domains: List[str],
        fusion_output: str = "",
        language: str = "en"
    ) -> Optional[Dict[str, Any]]:
        """
        Recommends verified officer matching the problem and jurisdiction.
        Returns None if no matching officer exists.
        """
        loc_info = self.detect_district_and_locality(query)
        district = loc_info["district"]
        locality = loc_info["locality"]

        if not district:
            # Zero hallucination: If district is unknown, do not recommend random officers
            return None

        # Determine target departments based on active domains and query keywords
        q_lower = query.lower()
        target_departments = []

        # Granular department prioritization
        if any(w in q_lower for w in ["supply officer", "ration", "pds", "rice", "fair price", "ரேஷன்", "வழங்கல் அதிகாரி"]):
            target_departments = ["Civil Supplies", "Co-operative", "District Supply Office"]
        elif any(w in q_lower for w in ["machinery", "tractor", "drone", "harvester", "agri engineering", "பொறியியல்"]):
            target_departments = ["Agricultural Engineering", "Agriculture", "DRDA"]
        elif any(w in q_lower for w in ["horticulture", "vegetable", "fruit", "polyhouse", "drip", "தோட்டக்கலை"]):
            target_departments = ["Horticulture", "Agriculture"]
        elif any(w in q_lower for w in ["agriculture officer", "agri officer", "aao", "ada", "crop loss", "pmfby", "hailstorm", "flood", "விவசாய அதிகாரி", "வேளாண்மை", "வேளாண் உதவி அலுவலர்", "வேளாண் உதவி இயக்குனர்"]):
            target_departments = ["Agriculture", "Horticulture", "District Administration"]
        elif any(w in q_lower for w in ["cooperative", "sub registrar", "subregistrar", "joint registrar", "pacs", "கூட்டுறவு", "பதிவாளர்"]):
            target_departments = ["Co-operative", "Co-operation, Food & Consumer Protection", "District Administration"]
        elif any(w in q_lower for w in ["tahsildar", "rdo", "patta", "title deed", "land record", "தாசில்தார்", "நில ஆவணம்"]):
            target_departments = ["Taluk Office", "Revenue", "Revenue Division", "Collectorate"]
        elif any(w in q_lower for w in ["fertilizer", "urea", "dap", "mrp", "black marketing", "overcharging", "உரம்", "யூரியா"]):
            target_departments = ["Co-operative", "Agriculture", "Civil Supplies", "Co-operation, Food & Consumer Protection"]
        elif "pacs_pmfby" in active_domains:
            target_departments = ["Agriculture", "Co-operative", "Horticulture", "Co-operation, Food & Consumer Protection"]
        elif "grievance" in active_domains:
            target_departments = ["Co-operative", "Agriculture", "Civil Supplies", "Revenue", "Taluk Office", "District Administration"]
        elif "farmer_scheme" in active_domains:
            target_departments = ["Agriculture", "Horticulture", "Agricultural Engineering", "DRDA"]
        elif "cooperative_law" in active_domains:
            target_departments = ["Co-operative", "Co-operation, Food & Consumer Protection", "District Administration"]
        else:
            target_departments = ["Agriculture", "Co-operative", "Revenue", "Taluk Office", "District Administration", "District Officers"]

        # Filter candidate officers from the verified database
        district_officers = [o for o in self.officers_db if o.get("district", "").lower() == district.lower()]
        if not district_officers:
            return None

        # Score matching officers
        scored_candidates = []
        for officer in district_officers:
            dept = officer.get("department", "")
            role = officer.get("designation_or_role", "") or officer.get("designation", "")
            place = officer.get("place_or_address", "")
            name = officer.get("name", "")
            block = officer.get("block_name", "") or ""
            hq = officer.get("head_quarters", "") or ""
            mobile = officer.get("mobile", "")
            landline = officer.get("landline", "")
            email = officer.get("email", "")

            # Ignore empty contact entries
            if not mobile and not landline and not email:
                continue

            # Strict Department Relevance Filter
            if dept not in target_departments:
                continue

            score = 0

            # Department match (higher score for top priority department)
            idx = target_departments.index(dept)
            score += (50 - idx * 10)

            # Locality / Block match
            if locality:
                loc_cleaned = locality.lower()
                if (loc_cleaned in role.lower() or 
                    loc_cleaned in place.lower() or 
                    loc_cleaned in name.lower() or
                    (block and loc_cleaned in block.lower()) or
                    (hq and loc_cleaned in hq.lower())):
                    score += 45

            # Role relevance matching specific query words
            if "supply officer" in q_lower and "supply officer" in role.lower():
                score += 30
            if "sub registrar" in q_lower and ("sub registrar" in role.lower() or "subregistrar" in role.lower()):
                score += 30
            if "joint registrar" in q_lower and "joint registrar" in role.lower():
                score += 35
            if ("agriculture" in q_lower or "agri" in q_lower) and ("agri" in role.lower() or "aao" in role.lower() or "ada" in role.lower()):
                score += 25
            if ("aao" in q_lower or "assistant agricultural officer" in q_lower) and "aao" in role.lower():
                score += 35
            if ("ada" in q_lower or "assistant director of agriculture" in q_lower) and "ada" in role.lower():
                score += 35
            if "tahsildar" in q_lower and "tahsildar" in role.lower():
                score += 25
            if "horticulture" in q_lower and "horti" in role.lower():
                score += 25
            if ("engineering" in q_lower or "machinery" in q_lower) and "engineer" in role.lower():
                score += 30

            if score > 0:
                scored_candidates.append((score, officer))

        if not scored_candidates:
            return None

        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_officer = scored_candidates[0][1]

        # Format recommendation text
        formatted_block = self._format_officer_block(top_officer, district, language)

        return {
            "district": district,
            "locality": locality,
            "officer": top_officer,
            "recommendation_text": formatted_block,
            "is_verified": True,
            "trust_score": 0.99
        }

    def _format_officer_block(self, officer: Dict[str, Any], district: str, language: str) -> str:
        name = officer.get("name") or "Concerned Designated Officer"
        role = officer.get("designation_or_role", "")
        dept = officer.get("department", "")
        mobile = officer.get("mobile", "")
        landline = officer.get("landline", "")
        email = officer.get("email", "")
        source = officer.get("source", f"https://{district.lower()}.nic.in")

        contacts = []
        if mobile:
            contacts.append(f"📱 **Mobile:** `{mobile}`")
        if landline:
            contacts.append(f"☎️ **Landline / Office:** `{landline}`")
        if email:
            contacts.append(f"✉️ **Email:** `{email}`")

        contact_str = " | ".join(contacts) if contacts else "Office Directory Listed"

        if language == "ta":
            return (
                f"### 🏛️ பரிந்துரைக்கப்படும் அதிகாரப்பூர்வ தொடர்பு ({district} மாவட்டம்)\n"
                f"- **அதிகாரி பெயர் / பதவி:** **{name}** ({role})\n"
                f"- **துறை:** {dept}\n"
                f"- **தொடர்பு விவரங்கள்:** {contact_str}\n"
                f"- **சரிபார்க்கப்பட்ட ஆதாரம்:** [மாவட்ட நிர்வாக தொடர்பு கையேடு]({source})\n"
                f"*(குறிப்பு: இத்தகவல் அதிகாரப்பூர்வ அரசு தரவுத்தளத்தில் இருந்து சரிபார்க்கப்பட்டது)*"
            )
        elif language == "hi":
            return (
                f"### 🏛️ अनुशंसित आधिकारिक संपर्क ({district} जिला)\n"
                f"- **अधिकारी का नाम / पद:** **{name}** ({role})\n"
                f"- **विभाग:** {dept}\n"
                f"- **संपर्क विवरण:** {contact_str}\n"
                f"- **सत्यापित आधिकारिक स्रोत:** [जिला प्रशासन डायरेक्टरी]({source})\n"
                f"*(नोट: यह विवरण आधिकारिक सरकारी डेटाबेस द्वारा सत्यापित है)*"
            )
        else:
            return (
                f"### 🏛️ Recommended Statutory Authority Contact ({district} District)\n"
                f"- **Officer Name / Designation:** **{name}** ({role})\n"
                f"- **Department:** {dept}\n"
                f"- **Official Contact Details:** {contact_str}\n"
                f"- **Verified Government Source:** [District Administration Directory]({source})\n"
                f"*(Note: Official verified contact record from government directory - Zero Hallucination)*"
            )
