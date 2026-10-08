"""
Main FastAPI Application Entrypoint.
Team BRAVITS - Smart India Hackathon (SIH 2026)
Multilingual Cooperative Governance & Legal Assistance Portal (SIH26088)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings

from backend.app.api.chat import router as chat_router
from backend.app.api.schemes import router as schemes_router
from backend.app.api.grievance import router as grievance_router
from backend.app.api.pacs import pacs_router
from backend.app.api.law import router as law_router
from backend.app.api.financial import router as financial_router
from backend.app.api.notifications import router as notifications_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multilingual AI Assistant for Cooperative Societies, PACS, Farmers, PMFBY, and Grievance Resolution"
)

# Enable CORS for frontend and kiosk clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(chat_router, prefix=f"{settings.API_V1_STR}/chat", tags=["AI Chat & Legal RAG"])
app.include_router(schemes_router, prefix=f"{settings.API_V1_STR}/schemes", tags=["Schemes & PMFBY"])
app.include_router(grievance_router, prefix=f"{settings.API_V1_STR}/grievance", tags=["Resolution Navigator"])
app.include_router(pacs_router, prefix=f"{settings.API_V1_STR}/pacs", tags=["PACS Services & Bylaws"])
app.include_router(law_router, prefix=f"{settings.API_V1_STR}/law", tags=["Cooperative Laws & MSCS"])
app.include_router(financial_router, prefix=f"{settings.API_V1_STR}/financial", tags=["Financial Literacy & KCC"])
app.include_router(notifications_router, prefix=f"{settings.API_V1_STR}/notifications", tags=["Scheme Alerts & Notifications"])

import asyncio
from ai_engine.language.text_to_speech import text_to_speech

@app.on_event("startup")
async def warm_up_tts_cache():
    def _warmup():
        common_phrases = [
            ("Welcome to the Cooperative AI Assistant.", "en"),
            ("Hello! How can I assist you with cooperative services and legal schemes today?", "en"),
            ("സഹകരണ ബാങ്ക് സേവനങ്ങളിലേക്ക് സ്വാഗതം.", "ml"),
            ("നമസ്കാരം! സഹകരണ സൊസൈറ്റി സേവനങ്ങളിൽ ഞാൻ നിങ്ങളെ എങ്ങനെ സഹായിക്കണം?", "ml"),
            ("வணக்கம்! கூட்டுறவு சேவை மற்றும் சட்ட உதவி மையத்திற்கு வரவேற்கிறோம்.", "ta"),
            ("விவசாயம், தொடக்க வேளாண்மைக் கூட்டுறவு கடன் சங்கம் மற்றும் அரசு திட்டங்கள் பற்றிய வழிகாட்டுதல் பெறலாம்.", "ta"),
            ("सहकारी एआई सहायक में आपका स्वागत है।", "hi"),
        ]
        for phrase, lang in common_phrases:
            try:
                text_to_speech(phrase, lang, play_audio=False)
            except Exception:
                pass

    # Run warmup in background thread to avoid blocking server boot
    asyncio.get_event_loop().run_in_executor(None, _warmup)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "offline_edge_mode": settings.OFFLINE_MODE,
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
