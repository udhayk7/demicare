from typing import Optional
from pydantic import BaseModel, ConfigDict


class TimelineEventResponse(BaseModel):
    id: str
    timestamp: str
    timeDisplay: str
    title: str
    description: str
    category: str
    severity: Optional[str] = "info"
    iconName: str = "Bell"

    model_config = ConfigDict(from_attributes=True)
