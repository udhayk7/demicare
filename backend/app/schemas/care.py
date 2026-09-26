from typing import Optional
from pydantic import BaseModel, ConfigDict


class RoutineResponse(BaseModel):
    id: str
    title: str
    category: str
    completed: int
    total: int

    model_config = ConfigDict(from_attributes=True)


class HabilitationResponse(BaseModel):
    id: str
    title: str
    category: str
    durationMinutes: int
    completed: bool
    scheduledTime: str

    model_config = ConfigDict(from_attributes=True)


class CognitiveResponse(BaseModel):
    id: str
    title: str
    type: str
    durationMinutes: int
    completed: bool
    score: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ObservationCreate(BaseModel):
    type: str  # confusion, agitation, repetitive_questioning, wandering, calm
    note: str
    intensity: Optional[str] = "mild"  # mild, moderate, severe
    caregiverActionTaken: Optional[str] = "Logged & observed by caregiver."


class ObservationResponse(BaseModel):
    id: str
    timestamp: str
    type: str
    note: str
    intensity: str
    caregiverActionTaken: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AppointmentResponse(BaseModel):
    id: str
    title: str
    doctor: str
    specialty: str
    date: str
    time: str
    location: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class HydrationLogCreate(BaseModel):
    amount: int = 1
    unit: str = "glass"


class HydrationLogResponse(BaseModel):
    id: str
    amount: int
    unit: str
    recordedAt: str
    todayTotal: int

    model_config = ConfigDict(from_attributes=True)


class MealLogCreate(BaseModel):
    mealType: str = "snack"  # breakfast, lunch, dinner, snack
    intakeLevel: str = "good"  # good, moderate, poor
    notes: Optional[str] = None


class MealLogResponse(BaseModel):
    id: str
    mealType: str
    intakeLevel: str
    recordedAt: str
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
