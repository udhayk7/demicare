from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.simulation import SimPersonDetectedRequest, SimGeofenceExitRequest, SimResponse
from app.services.simulation_service import SimulationService

router = APIRouter()


@router.post("/pendant/reminder", response_model=SimResponse)
def simulate_medication_reminder(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_medication_reminder(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/pendant/sos", response_model=SimResponse)
def simulate_sos(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_sos(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/pendant/geofence", response_model=SimResponse)
def simulate_geofence_exit(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_geofence_exit(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/pendant/return-home", response_model=SimResponse)
def simulate_return_home(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_return_home(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/camera/recognition", response_model=SimResponse)
def simulate_camera_recognition(
    req: SimPersonDetectedRequest,
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_person_detected(
        patient_id=patient_id,
        person_name=req.personName,
        relation=req.relation,
        confidence=req.confidence,
        camera_location=req.cameraLocation,
        db=db
    )
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/camera/unknown", response_model=SimResponse)
def simulate_camera_unknown(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_unknown_person(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/ai/recommendation", response_model=SimResponse)
def simulate_ai_recommendation(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    from app.services.ai_service import AIService
    rec = AIService.generate_recommendation(patient_id, db)
    return SimResponse(
        success=True,
        message=f"AI Companion generated new recommendation: '{rec.title}'"
    )


@router.post("/pendant/low-battery", response_model=SimResponse)
def simulate_low_battery(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.simulate_low_battery(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/safety/resolve", response_model=SimResponse)
def resolve_safety_event(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.resolve_safety_event(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])


@router.post("/reset", response_model=SimResponse)
def reset_simulations(
    patient_id: str = Query("pat-101"),
    db: Session = Depends(get_db)
):
    res = SimulationService.reset_simulations(patient_id, db)
    return SimResponse(success=res["success"], message=res["message"])

