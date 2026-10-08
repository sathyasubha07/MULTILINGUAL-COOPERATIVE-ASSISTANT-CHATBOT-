"""
Notifications & User Data Telemetry API Endpoints.
Handles:
- Active Scheme Updates & Broadcast Alerts
- Dynamic User-Tailored Scheme Eligibility Evaluation
- User Data Profile Synchronization (ChatGPT-style personalization context)
- Response Feedback & Interaction Telemetry
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from notifications.notification_service import notification_service

router = APIRouter()

class ProfileRequest(BaseModel):
    id: Optional[str] = None
    name: str
    mobile: Optional[str] = ""
    district: Optional[str] = "Theni"
    state: Optional[str] = "Tamil Nadu"
    societyName: Optional[str] = ""
    memberType: Optional[str] = "Farmer Member"
    land_size_acres: Optional[float] = 2.0
    crop_types: Optional[List[str]] = ["Paddy", "Tomato"]
    has_kcc: Optional[bool] = False
    has_soil_card: Optional[bool] = False
    has_aadhaar_dbt: Optional[bool] = True
    is_pacs_member: Optional[bool] = True
    preferredLang: Optional[str] = "en"

class FeedbackRequest(BaseModel):
    user_id: Optional[str] = "anonymous"
    query: str
    helpful: bool
    score: Optional[int] = 5
    feedback_text: Optional[str] = ""
    category: Optional[str] = "General"

class MarkReadRequest(BaseModel):
    user_id: Optional[str] = "default"
    notification_id: str

@router.get("/")
async def get_notifications(user_id: Optional[str] = None):
    """Fetch all active notifications, broadcast scheme alerts, and user-specific eligibility notices."""
    try:
        notifs = notification_service.get_all_notifications(user_id=user_id)
        return {
            "status": "success",
            "count": len(notifs),
            "unread_count": len([n for n in notifs if not n.get("is_read", False)]),
            "notifications": notifs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/eligibility-check")
async def evaluate_eligibility(profile: ProfileRequest):
    """
    Evaluates farmer profile against 25+ government schemes and determines
    which schemes they are currently eligible for or what actions unlock new benefits.
    """
    try:
        result = notification_service.evaluate_eligibility(profile.dict())
        return {
            "status": "success",
            "evaluation": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/profile")
async def save_profile(profile: ProfileRequest):
    """Save user profile to enable personalized recommendations and scheme alert transitions."""
    try:
        saved = notification_service.save_user_profile(profile.dict())
        # Also run immediate eligibility check
        eligibility = notification_service.evaluate_eligibility(saved)
        return {
            "status": "success",
            "profile": saved,
            "eligibility_summary": eligibility
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile/{user_id}")
async def get_profile(user_id: str):
    """Retrieve user profile and active personalized alerts."""
    try:
        profile = notification_service.get_user_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        eligibility = notification_service.evaluate_eligibility(profile)
        return {
            "status": "success",
            "profile": profile,
            "eligibility_summary": eligibility
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit user feedback on assistant response to continuously improve AI experience."""
    try:
        record = notification_service.log_feedback(feedback.dict())
        return {
            "status": "success",
            "message": "Thank you for your feedback! It helps improve the AI assistance accuracy.",
            "feedback": record
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-read")
async def mark_read(payload: MarkReadRequest):
    """Mark notification alert as read for user."""
    try:
        notification_service.mark_notification_read(payload.user_id, payload.notification_id)
        return {"status": "success", "marked_read": payload.notification_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
