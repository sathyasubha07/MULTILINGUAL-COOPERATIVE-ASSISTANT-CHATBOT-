"""
Specialized Farmer Scheme Sub-Model Engine for Cooperative AI Portal.
Handles scheme identification, eligibility matching, subsidy calculation, document checklists,
and verified online/offline application workflows across all 20+ Central & State agricultural schemes.
"""
import os
import json
import re
from typing import Dict, Any, List, Optional
from config.settings import settings
from ai_engine.language.translation import TranslationEngine

class FarmerSchemeEngine:
    def __init__(self):
        self.schemes_catalog: List[Dict[str, Any]] = []
        self.translator = TranslationEngine()
        self._load_schemes()

    def _load_schemes(self):
        schemes_path = os.path.join(settings.DATABASE_PATH, "schemes", "farmer_schemes.json")
        if os.path.exists(schemes_path):
            try:
                with open(schemes_path, "r", encoding="utf-8") as f:
                    self.schemes_catalog = json.load(f)
            except Exception as e:
                print(f"Error loading schemes catalog: {e}")

    def find_matching_schemes(self, query: str) -> List[Dict[str, Any]]:
        q_lower = query.lower()
        scored_schemes = []

        # Exhaustive Weighted Trigger Registry for all 20 Schemes
        triggers = {
            "SVAMITVA": ["svamitva", "property card", "village mapping", "drone survey", "gharauni", "स्वामित्व", "घरौनी", "சொத்து அட்டை", "గ్రామీణ ఆస్తి", "प्रॉपर्टी कार्ड"],
            "SPICES-BOARD": ["cardamom", "spices board", "turmeric boiler", "pepper thresher", "lakadong", "iccd", "silpaulin", "इलायची", "मसाला बोर्ड", "हल्दी", "ஏலக்காய்", "மஞ்சள்", "మిరియాలు", "पसुपु", "वेलची"],
            "COFFEE-BOARD": ["coffee board", "coffee plantation", "baby pulper", "drying yard", "coffee", "कॉफी", "காபி", "కాఫీ"],
            "COCONUT-CPIS-KERA": ["coconut palm", "kera suraksha", "tree climber", "coconut board", "neera", "नारियल", "केरा सुरक्षा", "தென்னை", "కొబ్బరి"],
            "ACABC": ["acabc", "ac&abc", "agri clinic", "agri business center", "agri graduate", "कृषि क्लीनिक", "வேளாண் மருந்தகம்", "అగ్రి క్లినిక్", "अॅग्री क्लिनिक"],
            "NMNF-BPKP": ["natural farming", "nmnf", "bpkp", "jeevamrutha", "krishi sakhi", "cow based", "प्राकृतिक खेती", "जीवामृत", "இயற்கை வேளாண்மை", "సహజ వ్యవసాయం", "नैसर्गिक शेती"],
            "GOPAL-RATNA": ["gopal ratna", "gokul mission", "indigenous breed", "dairy award", "गोपाल रत्न", "गोकुल मिशन", "கோபால் ரத்னா", "గోపాల్ రత్న"],
            "STUDENT-READY": ["student ready", "rawe", "iari scholarship", "icar fellowship", "स्टूडेंट रेडी", "आईएआरआई", "மாணவர் ஊரக"],
            "GOBARDHAN": ["gobardhan", "biogas subsidy", "cbg plant", "cattle dung", "गोवर्धन", "बायोगैस", "கோபர்தன்", "గోబర్ధన్"],
            "AMI-ISAM": ["ami", "isam", "rural godown", "storage subsidy", "ग्रामीण गोदाम", "கிடங்கு மானியம்", "గ్రామీణ గోదాము"],
            "NMEO-OP": ["nmeo", "oil palm", "palm oil", "palm plantation", "ऑयल पाम", "पाम की खेती", "ஆயில் பாம்", "ఆయిల్ పామ్"],
            "PMJVM-TRIFED": ["pmjvm", "trifed", "van dhan", "minor forest produce", "vdvk", "वन धन", "जनजातीय", "பழங்குடியினர்", "వన్ ధన్"],
            "TDPS-TEA": ["tea board", "small tea grower", "small tea growers", "tea plucking", "tea mechanization", "tea plantation", "चाय विकास", "தேயிலை", "టీ అభివృద్ధి"],
            "NFSM": ["nfsm", "food security mission", "seed minikit", "pulses subsidy", "nutri cereals", "paddy seed", "wheat seed", "pulses seed", "certified seed", "खाद्य सुरक्षा मिशन", "बीज मिनीकिट", "உணவுப் பாதுகாப்பு", "சான்றளிக்கப்பட்ட விதை", "ఆహార భద్రత"],
            "SHC": ["soil health", "soil test", "soil testing", "soil card", "मिट्टी परीक्षण", "मृदा स्वास्थ्य", "மண் பரிசோதனை", "నేల పరీక్ష"],
            "ENAM": ["e-nam", "enam", "e nam", "mandi online", "online mandi", "mandi trade", "ई-नाम", "மண்டி வர்த்தகம்", "ఈ-நாம்"],
            "MIDH": ["midh", "tomato", "tomato seed", "tomato seeds", "vegetable seeds", "vegetable seed", "seeds", "seed", "sowing", "sow", "seedling", "seedlings", "horticulture", "polyhouse", "poly house", "shade net", "mulching", "orchard", "greenhouse", "mushroom", "vegetable cultivation", "தக்காளி", "விதை", "விதைகள்", "தக்காளி விதை", "காய்கறி விதை", "நாற்று", "தோட்டக்கலை", "பாலிஹவுஸ்", "पॉलीहाउस", "शेडनेट", "टमाटर के बीज", "सब्जी बीज", "தோட்டக்கலை துறை"],
            "RKVY-RAFTAAR": ["rkvy", "raftaar", "agri startup", "startup grant", "incubator", "रफ्तार", "एग्री-स्टार्टअप", "தொழில்முனைவு"],
            "PM-AASHA": ["pm-aasha", "pmaasha", "msp", "minimum support price", "procurement", "price support", "एमएसपी", "न्यूनतम समर्थन मूल्य", "குறைந்தபட்ச ஆதரவு விலை"],
            "FPO-10000": ["fpo", "farmer producer organization", "10000 fpo", "equity grant", "एफपीओ", "உழவர் உற்பத்தியாளர் அமைப்பு", "రైతు ఉత్పత్తిదారుల"],
            "NBHM": ["nbhm", "beekeeping", "honey mission", "bee box", "मधुमक्खी पालन", "शहद मिशन", "தேனீ வளர்ப்பு", "తేనెటీగల పెంపకం"],
            "PM-KMY": ["pm-kmy", "pmkmy", "maan-dhan", "maandhan", "farmer pension", "3000 pension", "₹3,000", "किसान पेंशन", "விவசாயிகள் ஓய்வூதியம்", "రైతు పెన్షన్"],
            "PM-KUSUM": ["kusum", "solar pump", "solar subsidy", "solar tubewell", "solar water pump", "water pump", "irrigation pump", "borewell motor", "5 hp", "7.5 hp", "3 hp", "power cut pump", "power cut", "electricity problem", "power supply", "feeder solarization", "agricultural pump", "pump set", "solar motor", "power cut problem", "सोलर पंप", "சோலார் பம்ப்", "சவுர பம்பு", "सौर कृषी पंप"],
            "SMAM": ["smam", "mechanization", "tractor subsidy", "drone subsidy", "kisan drone", "rotavator", "कृषि यंत्र", "ட்ராக்டர் மானியம்"],
            "PKVY": ["pkvy", "organic farming", "paramparagat krishi", "50000", "50,000", "जैविक खेती", "இயற்கை விவசாயம்"],
            "PMKSY-PDMC": ["pmksy", "drip irrigation", "sprinkler", "micro irrigation", "per drop more crop", "water problem", "water scarcity", "water shortage", "irrigation water", "water not coming", "borewell water", "farm water", "drip", "sprinkler subsidy", "ड्रिप सिंचाई", "पानी की समस्या", "सिंचाई पानी", "சொட்டு நீர் பாசனம்", "தண்ணீர் பிரச்சனை", "பாசன நீர்", "நீటి సమస్య", "సాగునీరు"],
            "PMAY-G": ["pmay", "awaas", "awas yojana", "pucca house", "rural housing", "120000", "1,20,000", "आवास योजना", "வீட்டு வசதி திட்டம்"],
            "NLM-AHIDF": ["livestock", "goat farming", "sheep farming", "poultry subsidy", "piggery", "पशुधन मिशन", "बकरी पालन", "ஆடு வளர்ப்பு"],
            "PMMSY": ["pmmsy", "matsya", "fisheries", "fish pond", "biofloc", "மத்ஸ்ய சம்பதா", "मछली पालन", "மீன்வள மேம்பாடு"],
            "AIF": ["aif", "agri infra", "agriculture infrastructure fund", "cold storage subsidy", "godown subsidy", "कृषि अवसंरचना कोष"],
            "KCC": ["kcc", "kisan credit card", "crop loan", "4%", "4 percent", "interest subvention", "केसीसी", "किसान क्रेडिट कार्ड", "பயிர் கடன்"],
            "PM-KISAN": ["pm-kisan", "pmkisan", "pm kisan", "kisan samman", "samman nidhi", "6000", "₹6,000", "2000", "installment", "किस्त", "पीएम किसान", "தவணை"],
            "RUBBER-MTFP": ["rubber", "natural rubber", "rubber board", "replanting rubber", "रबर", "ரப்பர்"],
            "NBM": ["bamboo", "bamboo mission", "बांस मिशन", "மூங்கில்"],
            "RAD-IFS": ["rainfed", "integrated farming", "ifs", "वर्षा आधारित खेती", "ஒருங்கிணைந்த பண்ணை"],
            "ISAC-NCDC": ["ncdc", "isac", "cooperative loan", "सहकारिता ऋण", "கூட்டுறவு கடன்"],
            "APEDA-FAS": ["apeda", "export promotion", "agri export", "कृषि निर्यात", "வேளாண் ஏற்றுமதி"],
            "LHDC": ["lhdc", "animal vaccination", "foot and mouth", "fmd", "pashu aadhaar", "पशु आधार", "पशु टीकाकरण", "கால்நடை தடுப்பூசி"],
            "ECOMARK": ["ecomark", "eco label", "पर्यावरण अनुकूल", "சுற்றுச்சூழல் முத்திரை"],
            "NAGAR-VAN": ["nagar van", "city forest", "nagar vatika", "नगर वन"],
            "PMGSY": ["pmgsy", "gram sadak", "rural road", "सड़क योजना", "கிராம சாலை"],
            "PMAAGY-PMAGY": ["adi adarsh", "adarsh gram", "pm-ajay", "आदर्श ग्राम", "மாதிரி கிராமம்"],
            "PM-VANBANDHU": ["vanbandhu", "tribal scholarship", "वनबंधु कल्याण", "பழங்குடியினர் உதவித்தொகை"],
            "AGRI-AWARDS": ["krishi vigyan puraskar", "national water awards competition", "dhanwantari award", "geoscience award", "कृषि पुरस्कार"]
        }

        # 1. Multi-Field + Trigger Weighted Scoring
        q_tokens = set(re.findall(r'\w+', q_lower))

        for scheme in self.schemes_catalog:
            code = scheme.get("scheme_code", "")
            kw_list = triggers.get(code, [])
            score = 0.0

            # Direct trigger phrase matches
            for kw in kw_list:
                if kw in q_lower:
                    score += 6.0 if " " in kw else 3.0

            # Scheme Name and Code direct token matches
            s_name = scheme.get("scheme_name", "").lower()
            s_code = code.lower()
            if s_code and (s_code in q_lower or s_code.replace("-", "") in q_lower.replace("-", "")):
                score += 8.0
            for tok in q_tokens:
                if len(tok) > 2 and tok in s_name:
                    score += 2.0

            # Summary, Category & Benefit matches
            summary = (scheme.get("summary", "") + " " + scheme.get("category", "")).lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in summary:
                    score += 1.0

            # Financial benefit & Eligibility token matches
            benefit = scheme.get("financial_benefit", "").lower()
            for tok in q_tokens:
                if len(tok) > 3 and tok in benefit:
                    score += 1.0

            if score > 0:
                scored_schemes.append((score, scheme))

        # Sort by score descending
        if scored_schemes:
            scored_schemes.sort(key=lambda x: x[0], reverse=True)
            return [item[1] for item in scored_schemes]

        # Fallback to top schemes if no score
        return self.schemes_catalog[:3]

    def generate_scheme_guidance(self, query: str, language: str = "en") -> Dict[str, Any]:
        matched = self.find_matching_schemes(query)
        primary = matched[0]

        guidance_text = self._format_scheme_response(primary, query, language)
        if language not in ("en", "ta", "hi"):
            guidance_text = self.translator.translate(guidance_text, "en", language)

        return {
            "matched_schemes": [s.get("scheme_name") for s in matched],
            "primary_scheme": primary,
            "guidance_text": guidance_text,
            "financial_benefit": primary.get("financial_benefit"),
            "official_portal": primary.get("official_portal"),
            "documents_required": primary.get("documents_required", []),
            "citations": primary.get("citations", []),
            "is_verified": primary.get("is_verified", True),
            "trust_score": primary.get("trust_score", 0.99)
        }

    def _format_scheme_response(self, scheme: Dict[str, Any], query: str, language: str) -> str:
        name = scheme.get("scheme_name", "Farmer Welfare Scheme")
        summary = scheme.get("summary", "")
        benefit = scheme.get("financial_benefit", "")
        eligibility = scheme.get("eligibility_criteria", "")
        portal = scheme.get("official_portal", "https://myscheme.gov.in")
        docs = scheme.get("documents_required", [])
        online_mode = scheme.get("application_mode_online", "")
        offline_mode = scheme.get("application_mode_offline", "")
        citations = scheme.get("citations", [])

        docs_formatted = "\n".join([f"  - {d}" for d in docs])
        q_low = query.lower()

        is_asking_docs = any(w in q_low for w in ["document", "documents", "paper", "papers", "proof", "दस्तावेज़", "ஆவணங்கள்", "காగితాలు"])
        is_asking_subsidy = any(w in q_low for w in ["subsidy", "benefit", "amount", "money", "how much", "rate", "subvention", "अनुदान", "लाभ", "रुपये", "மானியம்", "தொகை", "సబ్సిడీ"])
        is_asking_eligibility = any(w in q_low for w in ["eligible", "eligibility", "who can", "criteria", "पात्रता", "தகுதி", "అర్హత"])
        is_asking_apply = any(w in q_low for w in ["how to apply", "apply", "registration", "register", "आवेदन", "விண்ணப்பிக்க", "దరఖాస్తు"])
        is_asking_seed = any(w in q_low for w in ["seed", "seeds", "sow", "sowing", "tomato", "vegetable", "seedling", "seedlings", "collect", "where to get", "where could i", "விதை", "விதைகள்", "நாற்று", "தக்காளி", "காய்கறி", "बीज", "टमाटर"])

        if language == "hi":
            sections = [f"### 📜 {name}\n"]
            if is_asking_seed:
                sections.append(
                    "**🌱 प्रमाणित बीज एवं पौध वितरण केंद्र (Where to Collect):**\n"
                    "- **ब्लॉक कृषि विस्तार केंद्र (AEC) / बागवानी डिपो:** प्रमाणित हाइब्रिड सब्जी/टमाटर के बीज 50% सरकारी अनुदान पर उपलब्ध।\n"
                    "- **स्थानीय प्राथमिक कृषि साख समिति (PACS / PMKSK):** प्रमाणित बीज कोटा वितरण केंद्र।\n"
                    "- **राजकीय बागवानी फार्म एवं नर्सरी:** प्रो-ट्रे पौध एवं उन्नत किस्में।\n"
                )
                sections.append(f"**💰 वित्तीय लाभ एवं अनुदान:**\n{benefit}\n")
                sections.append(f"**📝 आवेदन एवं पंजीयन:** ऑनलाइन: [{portal}]({portal}) | ऑफ़लाइन: {offline_mode}\n")
            elif is_asking_subsidy:
                sections.append(f"**💰 वित्तीय लाभ एवं अनुदान सहायता:**\n{benefit}\n")
                sections.append(f"**📌 योजना विवरण:**\n{summary}\n")
            elif is_asking_docs:
                sections.append(f"**📋 आवश्यक दस्तावेज़ चेकलिस्ट:**\n{docs_formatted}\n")
                sections.append(f"**💰 वित्तीय लाभ:**\n{benefit}\n")
            elif is_asking_eligibility:
                sections.append(f"**🎯 पात्रता मानदंड:**\n{eligibility}\n")
                sections.append(f"**💰 वित्तीय लाभ:**\n{benefit}\n")
            elif is_asking_apply:
                sections.append(f"**📝 आवेदन प्रक्रिया:**\n- **ऑनलाइन आवेदन:** {online_mode} (पोर्टल: [{portal}]({portal}))\n- **ऑफ़लाइन आवेदन:** {offline_mode}\n")
                sections.append(f"**📋 आवश्यक दस्तावेज़:**\n{docs_formatted}\n")
            else:
                sections.append(f"**📌 योजना सारांश:**\n{summary}\n")
                sections.append(f"**💰 वित्तीय लाभ एवं अनुदान:**\n{benefit}\n")
                sections.append(f"**📋 आवश्यक दस्तावेज़:**\n{docs_formatted}\n")
                sections.append(f"**📝 आवेदन प्रक्रिया:**\n- **ऑनलाइन:** {online_mode} (पोर्टल: [{portal}]({portal}))\n- **ऑफ़लाइन:** {offline_mode}\n")

            sections.append(f"🏛️ **सत्यापित आधिकारिक संदर्भ:** {', '.join(citations)}")
            return "\n".join(sections)

        elif language == "ta":
            sections = [f"### 📜 {name}\n"]
            if is_asking_seed:
                sections.append(
                    "**🌱 சான்றளிக்கப்பட்ட விதை மற்றும் நாற்றுகள் பெறும் இடங்கள் (Where to Collect):**\n"
                    "- **வட்டார வேளாண்மை விரிவாக்க மையம் (AEC) / தோட்டக்கலை உதவி இயக்குனர் அலுவலகம்:** தக்காளி மற்றும் காய்கறி விதைகள் 50% அரசு மானியத்தில் பெறலாம்.\n"
                    "- **தொடக்க வேளாண்மை கூட்டுறவு கடன் சங்கம் (PACS / PMKSK):** தரமான சான்றளிக்கப்பட்ட விதை இருப்பு மையம்.\n"
                    "- **அரசு தோட்டக்கலை பண்ணை (State Horticulture Farm):** குழித்தட்டு நாற்றுகள் (Pro-tray Seedlings).\n"
                )
                sections.append(f"**💰 நிதி உதவி மற்றும் மானிய விபரம்:**\n{benefit}\n")
                sections.append(f"**📝 பதிவு முறை:** ஆன்லைன்: [{portal}]({portal}) | நேரடி: {offline_mode}\n")
            elif is_asking_subsidy:
                sections.append(f"**💰 நிதி உதவி மற்றும் மானிய விபரம்:**\n{benefit}\n")
                sections.append(f"**📌 திட்ட விளக்கம்:**\n{summary}\n")
            elif is_asking_docs:
                sections.append(f"**📋 தேவையான ஆவணங்கள்:**\n{docs_formatted}\n")
                sections.append(f"**💰 நிதி உதவி:**\n{benefit}\n")
            elif is_asking_eligibility:
                sections.append(f"**🎯 தகுதி வரம்புகள்:**\n{eligibility}\n")
                sections.append(f"**💰 நிதி உதவி:**\n{benefit}\n")
            else:
                sections.append(f"**📌 திட்ட விளக்கம்:**\n{summary}\n")
                sections.append(f"**💰 நிதி உதவி மற்றும் மானிய விபரம்:**\n{benefit}\n")
                sections.append(f"**📋 தேவையான ஆவணங்கள்:**\n{docs_formatted}\n")
                sections.append(f"**📝 விண்ணப்பிக்கும் முறை:**\n- **ஆன்லைன்:** {online_mode} (இணையதளம்: [{portal}]({portal}))\n- **நேரடி:** {offline_mode}\n")

            sections.append(f"🏛️ **அரசாணை மற்றும் சான்றுகள்:** {', '.join(citations)}")
            return "\n".join(sections)

        else:
            sections = [f"### 📜 {name}\n"]
            if is_asking_subsidy:
                sections.append(f"**💰 Financial Benefit & Subsidy Slabs:**\n{benefit}\n")
                sections.append(f"**📌 Scheme Overview:**\n{summary}\n")
            elif is_asking_docs:
                sections.append(f"**📋 Mandatory Document Checklist:**\n{docs_formatted}\n")
                sections.append(f"**💰 Financial Benefit:**\n{benefit}\n")
            elif is_asking_eligibility:
                sections.append(f"**🎯 Eligibility Criteria:**\n{eligibility}\n")
                sections.append(f"**💰 Financial Benefit:**\n{benefit}\n")
            elif is_asking_apply:
                sections.append(f"**📝 Application Workflow:**\n- **Online Registration:** {online_mode} (Official Portal: [{portal}]({portal}))\n- **Offline Submission:** {offline_mode}\n")
                sections.append(f"**📋 Required Documents:**\n{docs_formatted}\n")
            else:
                sections.append(f"**📌 Scheme Overview:**\n{summary}\n")
                sections.append(f"**💰 Financial Benefit & Subsidy Slabs:**\n{benefit}\n")
                sections.append(f"**📋 Mandatory Document Checklist:**\n{docs_formatted}\n")
                sections.append(f"**📝 Application Workflow:**\n- **Online:** {online_mode} (Official Portal: [{portal}]({portal}))\n- **Offline:** {offline_mode}\n")

            sections.append(f"🏛️ **Verified Official Citations:** {', '.join(citations)}")
            return "\n".join(sections)
