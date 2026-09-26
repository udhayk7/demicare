from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class MealLog(Base, TimestampMixin):
    __tablename__ = "meal_logs"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    meal_type: Mapped[str] = mapped_column(String(50), nullable=False)  # breakfast, lunch, dinner, snack
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    intake_level: Mapped[str] = mapped_column(String(30), default="good")  # good, moderate, poor
    appetite: Mapped[str] = mapped_column(String(50), default="normal")
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


class HydrationLog(Base, TimestampMixin):
    __tablename__ = "hydration_logs"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    amount: Mapped[int] = mapped_column(Integer, default=1)  # glasses
    unit: Mapped[str] = mapped_column(String(20), default="glass")
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), default="caregiver")


class BehaviourObservation(Base, TimestampMixin):
    __tablename__ = "behaviour_observations"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    observation_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # confusion, agitation, repetitive_questioning, wandering, calm
    note: Mapped[str] = mapped_column(Text, nullable=False)
    intensity: Mapped[str] = mapped_column(String(30), default="mild")  # mild, moderate, severe
    caregiver_action_taken: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    possible_trigger: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_by: Mapped[str] = mapped_column(String(100), default="Anu Menon")

    patient: Mapped["Patient"] = relationship("Patient", back_populates="behaviour_observations")


class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    doctor: Mapped[str] = mapped_column(String(100), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), default="Neurology")
    date_str: Mapped[str] = mapped_column(String(50), nullable=False)  # "28 Sep 2026"
    time_str: Mapped[str] = mapped_column(String(30), nullable=False)  # "10:30 AM"
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="upcoming")  # upcoming, completed, cancelled
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reminder_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="appointments")
