from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.schemas.report import CareReportResponse, ReportGenerateRequest
from app.services.report_service import ReportService

router = APIRouter()


@router.get("/{patient_id}/reports", response_model=List[CareReportResponse])
def get_reports(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return ReportService.get_reports(patient_id, db)


@router.post("/{patient_id}/reports/generate", response_model=CareReportResponse)
def generate_report(
    patient_id: str,
    req: ReportGenerateRequest,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    return ReportService.generate_report(patient_id, req, db)


@router.get("/{patient_id}/reports/{report_id}/download")
def download_report_pdf(
    patient_id: str,
    report_id: str,
    token: Optional[str] = None,
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    pdf_buffer = ReportService.build_pdf_stream(report_id, db)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=CareReport_{report_id}.pdf"}
    )

