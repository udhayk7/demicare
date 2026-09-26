from pydantic import BaseModel, ConfigDict


class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    timestamp: str
    read: bool
    type: str  # medication, safety, ai, system

    model_config = ConfigDict(from_attributes=True)
