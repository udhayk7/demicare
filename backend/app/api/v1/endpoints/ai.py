from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.schemas.ai import AIRecommendationResponse, AIInsightResponse, AIFeedbackRequest, AICompleteRequest
from app.services.ai_service import AIService

router = APIRouter()


@router.get("/{patient_id}/ai/recommendations", response_model=List[AIRecommendationResponse])
def get_ai_recommendations(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return AIService.get_recommendations(patient_id, db)


@router.get("/{patient_id}/ai/insights", response_model=List[AIInsightResponse])
def get_ai_insights(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return AIService.get_insights(patient_id, db)


@router.post("/{patient_id}/ai/recommendations/{rec_id}/complete", response_model=AIRecommendationResponse)
def complete_ai_recommendation(
    patient_id: str,
    rec_id: str,
    req: Optional[AICompleteRequest] = None,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    feedback_val = req.feedback if req and req.feedback else "enjoyed"
    return AIService.complete_recommendation(rec_id, feedback_val=feedback_val, db=db)



@router.post("/{patient_id}/ai/recommendations/{rec_id}/feedback", response_model=AIRecommendationResponse)
def record_ai_feedback(
    patient_id: str,
    rec_id: str,
    req: AIFeedbackRequest,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return AIService.record_feedback(rec_id, req, db)


@router.post("/{patient_id}/ai/generate-summary", response_model=AIRecommendationResponse)
def generate_ai_summary_suggestion(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return AIService.generate_recommendation(patient_id, db)
