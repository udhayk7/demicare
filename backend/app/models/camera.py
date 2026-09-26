from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class FamiliarPerson(Base, TimestampMixin):
    __tablename__ = "familiar_people"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    relation: Mapped[str] = mapped_column(String(100), nullable=False)  # Daughter (Primary), Son, Family Nurse
    avatar: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="frequent")  # frequent, recent, visitor
    last_recognized_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="familiar_people")


class RecognitionEvent(Base, TimestampMixin):
    __tablename__ = "recognition_events"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    familiar_person_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("familiar_people.id", ondelete="SET NULL"), nullable=True)
    detected_name: Mapped[str] = mapped_column(String(100), nullable=False)
    relation: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=98.4)
    camera_location: Mapped[str] = mapped_column(String(100), default="Living Room Smart Cam")
    status: Mapped[str] = mapped_column(String(50), default="recognized", index=True)  # recognized, unknown_visitor
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source: Mapped[str] = mapped_column(String(50), default="python_cv_service")
