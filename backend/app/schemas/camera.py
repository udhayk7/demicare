from typing import Optional
from pydantic import BaseModel, ConfigDict


class FamiliarPersonResponse(BaseModel):
    id: str
    name: str
    relation: str
    avatar: str
    lastRecognized: Optional[str] = None
    status: str  # frequent, recent, visitor

    model_config = ConfigDict(from_attributes=True)


class RecognitionEventResponse(BaseModel):
    id: str
    timestamp: str
    personName: str
    relation: str
    confidenceScore: float
    cameraLocation: str
    status: str  # recognized, unknown_visitor

    model_config = ConfigDict(from_attributes=True)


class CameraIngestRequest(BaseModel):
    patient_id: str = "pat-101"
    familiar_person_id: Optional[str] = None
    detected_name: str
    relation: str
    confidence: float = 98.5
    camera_location: Optional[str] = "Front Door Camera"
    source: Optional[str] = "python_cv_service"
