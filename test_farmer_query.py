import sys
import io
import json
from ai_engine.rag.rag_pipeline import RAGPipeline

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

rag = RAGPipeline()
query = "I am a farmer in theni what are schemes I am eligible for and other farmer related questions which is frequently asked by farmer"
res = rag.process_query(query, "en")

print("=== RAW ANSWER ===")
print(res.get("answer"))
print("\n=== DOMAIN ===", res.get("domain"))
print("\n=== RECOMMENDED OFFICER ===", json.dumps(res.get("recommended_officer"), indent=2))
