"""
Chat API Endpoint for Multilingual Cooperative & Legal Inquiries.
"""
from fastapi import APIRouter, HTTPException
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def handle_chat_query(payload: ChatRequest):
    try:
        response = chat_service.process_chat(
            query=payload.query,
            language=payload.language or "en"
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
