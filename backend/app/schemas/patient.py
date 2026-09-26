from typing import Optional
from pydantic import BaseModel, ConfigDict


class PatientResponse(BaseModel):
    id: str
    name: str
    age: int
    condition: str
    stage: str
    status: str
    primaryCaregiver: str
    primaryCaregiverRelation: str
    secondaryCaregiver: str
    secondaryCaregiverRelation: str
    doctorName: str
    doctorSpecialty: str
    avatarUrl: str
    emergencyContact: str

    model_config = ConfigDict(from_attributes=True)


class PatientStatusUpdate(BaseModel):
    status: str
