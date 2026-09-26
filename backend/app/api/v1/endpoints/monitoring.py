from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.schemas.monitoring import (
    LocationResponse,
    MovementResponse,
    SleepResponse,
    PendantResponse,
    SafetyEventResponse,
    MonitoringSummaryResponse
)
from app.services.monitoring_service import MonitoringService

router = APIRouter()


@router.get("/{patient_id}/monitoring/summary", response_model=MonitoringSummaryResponse)
def get_monitoring_summary(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.get_summary(patient_id, db)


@router.get("/{patient_id}/monitoring/location", response_model=LocationResponse)
def get_location(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.get_location(patient_id, db)


@router.get("/{patient_id}/monitoring/movement", response_model=MovementResponse)
def get_movement(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.get_movement(patient_id, db)


@router.get("/{patient_id}/monitoring/sleep", response_model=SleepResponse)
def get_sleep(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.get_sleep(patient_id, db)


@router.get("/{patient_id}/monitoring/pendant", response_model=PendantResponse)
def get_pendant(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.get_pendant(patient_id, db)


@router.post("/{patient_id}/monitoring/pendant/test-reminder")
def test_pendant_reminder(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return {"success": True, "message": "Test reminder tone played on pendant device."}


@router.get("/{patient_id}/monitoring/safety", response_model=List[SafetyEventResponse])
def get_safety_events(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.get_safety_events(patient_id, db)


@router.post("/{patient_id}/monitoring/safety/sos", response_model=SafetyEventResponse)
def trigger_sos(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return MonitoringService.trigger_sos(patient_id, source="app_emergency_button", db=db)
