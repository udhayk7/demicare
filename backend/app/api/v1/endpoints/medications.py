from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access, get_current_user
from app.models.patient import Patient
from app.models.user import User
from app.schemas.medication import MedicationResponse, MedicationCreate, MedicationAcknowledgeRequest
from app.services.medication_service import MedicationService

router = APIRouter()


@router.get("/{patient_id}/medications", response_model=List[MedicationResponse])
def get_medications(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MedicationService.get_medications(patient_id, db)


@router.post("/{patient_id}/medications", response_model=MedicationResponse)
def create_medication(
    patient_id: str,
    med_in: MedicationCreate,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MedicationService.create_medication(patient_id, med_in, db)


@router.post("/{patient_id}/medications/{med_id}/acknowledge", response_model=MedicationResponse)
def acknowledge_medication(
    patient_id: str,
    med_id: str,
    req: MedicationAcknowledgeRequest,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access),
    current_user: User = Depends(get_current_user)
):
    return MedicationService.acknowledge_medication(
        medication_id=med_id,
        status="taken",
        acknowledged_by=current_user.name,
        db=db
    )


@router.post("/{patient_id}/medications/{med_id}/miss", response_model=MedicationResponse)
def mark_medication_missed(
    patient_id: str,
    med_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access),
    current_user: User = Depends(get_current_user)
):
    return MedicationService.acknowledge_medication(
        medication_id=med_id,
        status="missed",
        acknowledged_by=current_user.name,
        db=db
    )
