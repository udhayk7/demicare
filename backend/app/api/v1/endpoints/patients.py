from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.schemas.patient import PatientResponse, PatientStatusUpdate
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    dash = DashboardService.get_dashboard(patient_id, db)
    return dash.patient


@router.put("/{patient_id}/status", response_model=PatientResponse)
def update_patient_status(
    patient_id: str,
    update: PatientStatusUpdate,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    patient.status = update.status
    db.commit()
    db.refresh(patient)
    dash = DashboardService.get_dashboard(patient_id, db)
    return dash.patient


@router.get("/{patient_id}/dashboard", response_model=DashboardResponse)
def get_patient_dashboard(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return DashboardService.get_dashboard(patient_id, db)
