from typing import Optional, List
from pydantic import BaseModel
from app.schemas.patient import PatientResponse
from app.schemas.medication import MedicationResponse
from app.schemas.care import RoutineResponse
from app.schemas.monitoring import LocationResponse, MovementResponse, SleepResponse, PendantResponse
from app.schemas.ai import AIRecommendationResponse


class DashboardResponse(BaseModel):
    patient: PatientResponse
    routines: List[RoutineResponse]
    medications: List[MedicationResponse]
    nextMedication: Optional[MedicationResponse] = None
    location: LocationResponse
    movement: MovementResponse
    sleep: SleepResponse
    pendant: PendantResponse
    aiRecommendation: Optional[AIRecommendationResponse] = None
    unreadNotificationsCount: int = 0
    attentionNeeded: bool = False
