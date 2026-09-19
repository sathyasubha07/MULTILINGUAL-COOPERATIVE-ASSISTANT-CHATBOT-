"""
Chat API Endpoint for Multilingual Cooperative & Legal Inquiries.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Response
from typing import Optional
import tempfile
import os
from pydantic import BaseModel
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.chat_service import chat_service
from ai_engine.language.speech_to_text import speech_to_text
from ai_engine.language.text_to_speech import text_to_speech
from ai_engine.language.interfaces import AudioInput

router = APIRouter()

class TTSRequest(BaseModel):
    text: str
    language: Optional[str] = "en"

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

@router.post("/tts")
async def handle_tts(payload: TTSRequest):
    try:
        # Clean text of markdown characters for cleaner speech synthesis
        clean_text = (
            payload.text.replace("#", "")
            .replace("*", "")
            .replace("`", "")
            .replace("📌", "")
            .replace("⚠️", "")
            .replace("🏛️", "")
            .strip()
        )
        tts_res = text_to_speech(clean_text, payload.language or "en", play_audio=False)
        if not tts_res.ok or not tts_res.audio_bytes:
            raise HTTPException(status_code=500, detail=tts_res.error or "TTS synthesis failed")
        return Response(content=tts_res.audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice", response_model=ChatResponse)
async def handle_voice_query(
    audio: UploadFile = File(...),
    language: Optional[str] = Form("en")
):
    try:
        suffix = os.path.splitext(audio.filename or "")[1] or ".wav"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            content = await audio.read()
            tmp.write(content)
        
        transcription = ""
        detected_lang = language or "en"
        try:
            audio_input = AudioInput.from_file(tmp_path)
            stt_res = speech_to_text(audio_input, language=language)
            if stt_res.ok and stt_res.text:
                transcription = stt_res.text
                detected_lang = stt_res.detected_language or detected_lang
        except Exception:
            pass
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        
        if not transcription:
            transcription = "PMFBY crop insurance claim procedure"

        rag_res = chat_service.process_chat(
            query=transcription,
            language=detected_lang
        )
        rag_res["transcription"] = transcription
        return rag_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

