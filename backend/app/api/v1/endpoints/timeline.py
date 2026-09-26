from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.schemas.timeline import TimelineEventResponse
from app.services.timeline_service import TimelineService

router = APIRouter()


@router.get("/{patient_id}/timeline", response_model=List[TimelineEventResponse])
def get_patient_timeline(
    patient_id: str,
    category: Optional[str] = Query("all", description="Category filter (all, medication, activities, behaviour, safety, location, camera, care_plan)"),
    limit: Optional[int] = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return TimelineService.get_timeline(patient_id, category=category, limit=limit, db=db)
