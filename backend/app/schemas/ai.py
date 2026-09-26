from typing import Optional
from pydantic import BaseModel, ConfigDict


class AIRecommendationResponse(BaseModel):
    id: str
    title: str
    activityType: str
    durationMinutes: int
    reason: str
    recommendedTime: str
    status: str  # suggested, started, completed, not_suitable
    icon: str
    observed: Optional[str] = None
    whyItMatters: Optional[str] = None
    suggestedAction: Optional[str] = None
    whyThisActivity: Optional[str] = None
    safetyCarePlan: Optional[str] = None
    expectedOutcome: Optional[str] = None
    caregiverFeedback: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AIInsightResponse(BaseModel):
    id: str
    category: str  # sleep, activity, medication, mood
    title: str
    description: str
    timestamp: str
    metric: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AIFeedbackRequest(BaseModel):
    feedback: str = "enjoyed"  # enjoyed, neutral, disliked, tired, assistance_needed, refused
    notes: Optional[str] = None


class AICompleteRequest(BaseModel):
    feedback: Optional[str] = "enjoyed"
    notes: Optional[str] = None

