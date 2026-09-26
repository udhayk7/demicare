from typing import Optional
from pydantic import BaseModel, ConfigDict


class CareReportResponse(BaseModel):
    id: str
    title: str
    type: str  # weekly, monthly, doctor, medication, activity, safety
    generatedDate: str
    period: str
    summary: str
    adherenceRate: int
    medicationRate: int
    cognitiveRate: int
    fileSize: str

    model_config = ConfigDict(from_attributes=True)


class ReportGenerateRequest(BaseModel):
    report_type: str = "doctor"  # weekly, monthly, doctor, medication, activity, safety
    period: Optional[str] = "Last 30 Days"
