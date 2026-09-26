from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access, get_current_user
from app.models.patient import Patient
from app.models.user import User
from app.schemas.care import (
    RoutineResponse,
    HabilitationResponse,
    CognitiveResponse,
    ObservationCreate,
    ObservationResponse,
    AppointmentResponse,
    HydrationLogCreate,
    HydrationLogResponse,
    MealLogCreate,
    MealLogResponse
)
from app.services.care_service import CareService

router = APIRouter()


@router.get("/{patient_id}/care/routines", response_model=List[RoutineResponse])
def get_routines(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.get_routines(patient_id, db)


@router.get("/{patient_id}/care/habilitation", response_model=List[HabilitationResponse])
def get_habilitation(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.get_habilitation(patient_id, db)


@router.post("/{patient_id}/care/habilitation/{activity_id}/toggle", response_model=HabilitationResponse)
def toggle_habilitation(
    patient_id: str,
    activity_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.toggle_habilitation(activity_id, db)


@router.get("/{patient_id}/care/cognitive", response_model=List[CognitiveResponse])
def get_cognitive(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.get_cognitive(patient_id, db)


@router.post("/{patient_id}/care/cognitive/{activity_id}/toggle", response_model=CognitiveResponse)
def toggle_cognitive(
    patient_id: str,
    activity_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.toggle_cognitive(activity_id, db)


@router.get("/{patient_id}/care/observations", response_model=List[ObservationResponse])
def get_observations(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.get_observations(patient_id, db)


@router.post("/{patient_id}/care/observations", response_model=ObservationResponse)
def create_observation(
    patient_id: str,
    data: ObservationCreate,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access),
    current_user: User = Depends(get_current_user)
):
    return CareService.create_observation(patient_id, data, current_user.name, db)


@router.get("/{patient_id}/care/appointments", response_model=List[AppointmentResponse])
def get_appointments(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.get_appointments(patient_id, db)


@router.post("/{patient_id}/care/hydration", response_model=HydrationLogResponse)
def log_hydration(
    patient_id: str,
    data: HydrationLogCreate,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.log_hydration(patient_id, data, db)


@router.post("/{patient_id}/care/nutrition", response_model=MealLogResponse)
def log_nutrition(
    patient_id: str,
    data: MealLogCreate,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return CareService.log_meal(patient_id, data, db)

