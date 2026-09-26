from app.schemas.auth import LoginRequest, TokenResponse, UserResponse, RegisterRequest
from app.schemas.patient import PatientResponse, PatientStatusUpdate
from app.schemas.medication import MedicationResponse, MedicationCreate, MedicationAcknowledgeRequest
from app.schemas.care import (
    RoutineResponse,
    HabilitationResponse,
    CognitiveResponse,
    ObservationCreate,
    ObservationResponse,
    AppointmentResponse
)
from app.schemas.monitoring import (
    Coordinates,
    LocationResponse,
    MovementResponse,
    SleepResponse,
    PendantResponse,
    SafetyEventResponse,
    MonitoringSummaryResponse
)
from app.schemas.camera import FamiliarPersonResponse, RecognitionEventResponse, CameraIngestRequest
from app.schemas.ai import AIRecommendationResponse, AIInsightResponse, AIFeedbackRequest
from app.schemas.timeline import TimelineEventResponse
from app.schemas.report import CareReportResponse, ReportGenerateRequest
from app.schemas.notification import NotificationResponse
from app.schemas.dashboard import DashboardResponse
from app.schemas.simulation import SimPersonDetectedRequest, SimGeofenceExitRequest, SimResponse

__all__ = [
    "LoginRequest",
    "TokenResponse",
    "UserResponse",
    "RegisterRequest",
    "PatientResponse",
    "PatientStatusUpdate",
    "MedicationResponse",
    "MedicationCreate",
    "MedicationAcknowledgeRequest",
    "RoutineResponse",
    "HabilitationResponse",
    "CognitiveResponse",
    "ObservationCreate",
    "ObservationResponse",
    "AppointmentResponse",
    "Coordinates",
    "LocationResponse",
    "MovementResponse",
    "SleepResponse",
    "PendantResponse",
    "SafetyEventResponse",
    "MonitoringSummaryResponse",
    "FamiliarPersonResponse",
    "RecognitionEventResponse",
    "CameraIngestRequest",
    "AIRecommendationResponse",
    "AIInsightResponse",
    "AIFeedbackRequest",
    "TimelineEventResponse",
    "CareReportResponse",
    "ReportGenerateRequest",
    "NotificationResponse",
    "DashboardResponse",
    "SimPersonDetectedRequest",
    "SimGeofenceExitRequest",
    "SimResponse"
]
