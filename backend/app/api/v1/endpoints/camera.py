from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.schemas.camera import FamiliarPersonResponse, RecognitionEventResponse, CameraIngestRequest
from app.services.camera_service import CameraService

router = APIRouter()


@router.get("/patients/{patient_id}/camera/familiar-people", response_model=List[FamiliarPersonResponse])
def get_familiar_people(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CameraService.get_familiar_people(patient_id, db)


@router.get("/patients/{patient_id}/camera/recognitions", response_model=List[RecognitionEventResponse])
def get_recognition_events(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CameraService.get_recognition_events(patient_id, db)


@router.post("/camera/recognitions", response_model=RecognitionEventResponse)
def record_camera_recognition(
    req: CameraIngestRequest,
    db: Session = Depends(get_db)
):
    """
    Dedicated endpoint for the external Python computer-vision camera system (Section 28 & 73).
    Receives detection events and records them into recognition_events, updates familiar_people,
    and updates patient timeline & notifications.
    """
    return CameraService.record_recognition(
        patient_id=req.patient_id,
        detected_name=req.detected_name,
        relation=req.relation,
        confidence=req.confidence,
        camera_location=req.camera_location or "Front Door Camera",
        source=req.source or "python_cv_service",
        db=db
    )
