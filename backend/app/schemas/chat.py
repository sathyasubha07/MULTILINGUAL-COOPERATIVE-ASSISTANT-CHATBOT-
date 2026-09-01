"""
Pydantic API Schemas for Chat and Grievance workflows.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    language: Optional[str] = "en"
    domain: Optional[str] = None
    district: Optional[str] = None

class CitationModel(BaseModel):
    citation_text: str
    badge: Optional[str] = "Official"

class ProcedureStep(BaseModel):
    step_no: int
    title: str
    instruction: str
    timeline: str

class ChatResponse(BaseModel):
    query: str
    domain: str
    language: str
    confidence: float
    answer: str
    citations: List[str]
    verification_status: bool
    procedure: Optional[Dict[str, Any]] = None
    authorities: Optional[List[Dict[str, Any]]] = None

class GrievanceSubmission(BaseModel):
    applicant_name: str
    mobile: str
    aadhaar_last4: Optional[str] = None
    district: str
    society_name: Optional[str] = None
    category: str
    complaint_details: str
    language: Optional[str] = "en"
