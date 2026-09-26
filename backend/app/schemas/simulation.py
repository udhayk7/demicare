from typing import Optional
from pydantic import BaseModel


class SimPersonDetectedRequest(BaseModel):
    personName: str = "Anu Menon"
    relation: str = "Daughter"
    confidence: float = 99.1
    cameraLocation: str = "Front Entrance Cam"


class SimGeofenceExitRequest(BaseModel):
    address: Optional[str] = "Near East Gate Alleyway (180m from home)"
    lat: Optional[float] = 12.9268
    lng: Optional[float] = 77.6872


class SimResponse(BaseModel):
    success: bool = True
    message: str
    detail: Optional[str] = None
