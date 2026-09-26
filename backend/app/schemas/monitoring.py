from typing import Optional
from pydantic import BaseModel, ConfigDict


class Coordinates(BaseModel):
    lat: float
    lng: float


class LocationResponse(BaseModel):
    status: str  # at_home, safe_zone_exit, wandering
    address: str
    coordinates: Coordinates
    safeZoneCenter: Coordinates
    safeZoneRadiusMeters: int
    lastUpdated: str
    batteryLevel: int

    model_config = ConfigDict(from_attributes=True)


class MovementResponse(BaseModel):
    dailyKm: float
    steps: int
    activityLevel: str  # low, normal, active
    lastMovementTime: str

    model_config = ConfigDict(from_attributes=True)


class SleepResponse(BaseModel):
    durationHours: float
    quality: str  # restful, restless, interrupted
    sleepStart: str
    sleepEnd: str
    nightWakeups: int

    model_config = ConfigDict(from_attributes=True)


class PendantResponse(BaseModel):
    connected: bool
    batteryLevel: int
    gpsStatus: str  # available, low_accuracy, unavailable
    speakerStatus: str  # working, muted
    lastSync: str
    remindersActive: bool

    model_config = ConfigDict(from_attributes=True)


class SafetyEventResponse(BaseModel):
    id: str
    timestamp: str
    type: str  # sos_button, fall_detected, geofence_exit, pendant_disconnected
    severity: str  # low, medium, high, critical
    resolved: bool
    description: str

    model_config = ConfigDict(from_attributes=True)


class MonitoringSummaryResponse(BaseModel):
    location: LocationResponse
    movement: MovementResponse
    sleep: SleepResponse
    pendant: PendantResponse
    safetyEvents: list[SafetyEventResponse]
