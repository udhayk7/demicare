from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Medication(Base, TimestampMixin):
    __tablename__ = "medications"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    dosage: Mapped[str] = mapped_column(String(50), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(String(20), nullable=False)  # "08:00", "21:00"
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)  # taken, pending, missed, snoozed
    instructions: Mapped[str] = mapped_column(String(255), default="")
    icon: Mapped[str] = mapped_column(String(50), default="Pill")
    reminder_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="medications")
    events: Mapped[List["MedicationEvent"]] = relationship("MedicationEvent", back_populates="medication", cascade="all, delete-orphan")


class MedicationEvent(Base, TimestampMixin):
    __tablename__ = "medication_events"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    medication_id: Mapped[str] = mapped_column(String(50), ForeignKey("medications.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    medication_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dosage: Mapped[str] = mapped_column(String(50), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # taken, missed, pending, delayed, skipped
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    acknowledged_by: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="app")  # app, mock_pendant, real_pendant

    medication: Mapped["Medication"] = relationship("Medication", back_populates="events")
