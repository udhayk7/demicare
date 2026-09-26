from typing import Optional
from pydantic import BaseModel, ConfigDict


class MedicationResponse(BaseModel):
    id: str
    name: str
    dosage: str
    scheduledTime: str
    status: str
    instructions: str
    icon: Optional[str] = "Pill"

    model_config = ConfigDict(from_attributes=True)


class MedicationCreate(BaseModel):
    name: str
    dosage: str
    scheduled_time: str
    instructions: Optional[str] = ""
    icon: Optional[str] = "Pill"
    reminder_enabled: Optional[bool] = True


class MedicationAcknowledgeRequest(BaseModel):
    status: str = "taken"  # taken, missed, snoozed
    acknowledged_by: Optional[str] = "Anu Menon"
