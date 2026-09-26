from app.db.base import Base
from app.models.user import User, CaregiverPatient, CareTeamMember
from app.models.patient import Patient, SafeZone
from app.models.medication import Medication, MedicationEvent
from app.models.care import (
    Routine,
    HabilitationActivity,
    HabilitationEvent,
    CognitiveActivity,
    CognitiveEvent,
    DoctorCarePlan
)
from app.models.lifestyle import MealLog, HydrationLog, BehaviourObservation, Appointment
from app.models.monitoring import LocationEvent, MovementLog, SleepLog, SafetyEvent, PendantDevice
from app.models.camera import FamiliarPerson, RecognitionEvent
from app.models.ai import AIRecommendation, AIInsight, AIFeedback, PatientPreference
from app.models.notification import Notification
from app.models.report import CareReport, MedicalDocument

__all__ = [
    "Base",
    "User",
    "CaregiverPatient",
    "CareTeamMember",
    "Patient",
    "SafeZone",
    "Medication",
    "MedicationEvent",
    "Routine",
    "HabilitationActivity",
    "HabilitationEvent",
    "CognitiveActivity",
    "CognitiveEvent",
    "DoctorCarePlan",
    "MealLog",
    "HydrationLog",
    "BehaviourObservation",
    "Appointment",
    "LocationEvent",
    "MovementLog",
    "SleepLog",
    "SafetyEvent",
    "PendantDevice",
    "FamiliarPerson",
    "RecognitionEvent",
    "AIRecommendation",
    "AIInsight",
    "AIFeedback",
    "PatientPreference",
    "Notification",
    "CareReport",
    "MedicalDocument"
]
