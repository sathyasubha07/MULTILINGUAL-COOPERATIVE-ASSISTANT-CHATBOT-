"""
Intent Classifier & Query Categorizer for Multilingual Cooperative AI System.
Categorizes queries into:
- cooperative_law
- farmer_scheme
- pmfby
- pacs
- financial_literacy
- grievance
- general_faq
"""
import re
from typing import Dict, Any, List

class IntentClassifier:
    def __init__(self):
        self.domain_keywords = {
            "pmfby": [
                "crop insurance", "fasal bima", "pmfby", "crop loss", "claim",
                "hailstorm", "flood damage", "72 hours", "insurance premium",
                "फसल बीमा", "नुकसान", "முப்பயிர்க் காப்பீடு", "పంట భీమా", "पिक विमा"
            ],
            "cooperative_law": [
                "act", "section", "mscs", "bylaw", "bye-law", "election", "arbitration",
                "board meeting", "voting right", "dispute", "tribunal", "धारा", "कानून",
                "सहमती कायदा", "சட்டம்", "చట్టం"
            ],
            "farmer_scheme": [
                "scheme", "pm-kisan", "subsidy", "kisan samman", "aif", "machinery",
                "grant", "yojana", "योजना", "पीएम किसान", "अनुदान", "திட்டம்", "పథకం"
            ],
            "pacs": [
                "pacs", "society", "secretary", "membership", "fertilizer", "seed",
                "godown", "cooperative society", "पैक्स", "समिति", "సొసైటీ", "சங்கம்"
            ],
            "financial_literacy": [
                "kcc", "loan", "interest", "subvention", "credit card", "scale of finance",
                "banking", "aeps", "micro atm", "dbt", "ऋण", "ब्याज", "केसीसी", "வட்டி", "రుణం"
            ],
            "grievance": [
                "complaint", "rejected", "delay", "bribe", "harassment", "escalate",
                "officer", "redressal", "fraud", "शिकायत", "अपील", "புகார்", "ఫిర్యాదు"
            ]
        }

    def classify(self, query: str) -> Dict[str, Any]:
        cleaned_query = query.lower()
        scores: Dict[str, int] = {domain: 0 for domain in self.domain_keywords}
        
        for domain, keywords in self.domain_keywords.items():
            for kw in keywords:
                if kw in cleaned_query:
                    scores[domain] += 2
                else:
                    # check word boundaries
                    pattern = r'\b' + re.escape(kw) + r'\b'
                    if re.search(pattern, cleaned_query):
                        scores[domain] += 3

        # Default fallback
        best_domain = max(scores, key=scores.get)
        confidence = scores[best_domain] / 10.0 if scores[best_domain] > 0 else 0.4
        if scores[best_domain] == 0:
            best_domain = "general_coop"
            confidence = 0.5

        return {
            "domain": best_domain,
            "confidence": min(confidence, 0.98),
            "all_scores": scores,
            "raw_query": query
        }
