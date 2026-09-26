from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class CareReport(Base, TimestampMixin):
    __tablename__ = "care_reports"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # weekly, monthly, doctor, medication, activity, safety
    generated_date_label: Mapped[str] = mapped_column(String(50), default="Today")
    period: Mapped[str] = mapped_column(String(100), default="Last 30 Days")
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    adherence_rate: Mapped[int] = mapped_column(Integer, default=87)
    medication_rate: Mapped[int] = mapped_column(Integer, default=91)
    cognitive_rate: Mapped[int] = mapped_column(Integer, default=86)
    file_size: Mapped[str] = mapped_column(String(30), default="1.4 MB")
    file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="reports")


class MedicalDocument(Base, TimestampMixin):
    __tablename__ = "medical_documents"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by: Mapped[str] = mapped_column(String(100), default="Anu Menon")
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), default="application/pdf")
    category: Mapped[str] = mapped_column(String(50), default="Prescription")
    storage_reference: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    patient: Mapped["Patient"] = relationship("Patient", back_populates="medical_documents")
