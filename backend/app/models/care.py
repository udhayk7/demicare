from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Routine(Base, TimestampMixin):
    __tablename__ = "routines"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # medication, activities, cognitive, hydration, nutrition, behaviour
    completed_count: Mapped[int] = mapped_column(Integer, default=0)
    total_count: Mapped[int] = mapped_column(Integer, default=1)
    scheduled_time: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    recurrence: Mapped[str] = mapped_column(String(50), default="daily")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="routines")


class HabilitationActivity(Base, TimestampMixin):
    __tablename__ = "habilitation_activities"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="Physical")  # Physical, Sensory, Auditory, Social, Daily Living
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=15)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    scheduled_time: Mapped[str] = mapped_column(String(20), default="10:00")
    recommended_by: Mapped[Optional[str]] = mapped_column(String(100), default="Dr. Arun Nair")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="habilitation_activities")
    events: Mapped[List["HabilitationEvent"]] = relationship("HabilitationEvent", back_populates="activity", cascade="all, delete-orphan")


class HabilitationEvent(Base, TimestampMixin):
    __tablename__ = "habilitation_events"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    activity_id: Mapped[str] = mapped_column(String(50), ForeignKey("habilitation_activities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="completed")  # pending, completed, assisted, skipped
    assistance_level: Mapped[str] = mapped_column(String(50), default="independent")  # independent, gentle_guidance, full_assistance
    patient_response: Mapped[str] = mapped_column(String(50), default="enjoyed")  # enjoyed, neutral, disliked, tired
    caregiver_note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    activity: Mapped["HabilitationActivity"] = relationship("HabilitationActivity", back_populates="events")


class CognitiveActivity(Base, TimestampMixin):
    __tablename__ = "cognitive_activities"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(50), default="Reminiscence")  # Reminiscence, Executive Function, Memory Retrieval
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=15)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(30), default="easy")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="cognitive_activities")
    events: Mapped[List["CognitiveEvent"]] = relationship("CognitiveEvent", back_populates="activity", cascade="all, delete-orphan")


class CognitiveEvent(Base, TimestampMixin):
    __tablename__ = "cognitive_events"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    activity_id: Mapped[str] = mapped_column(String(50), ForeignKey("cognitive_activities.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    performance: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    patient_response: Mapped[str] = mapped_column(String(50), default="enjoyed")
    caregiver_note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    activity: Mapped["CognitiveActivity"] = relationship("CognitiveActivity", back_populates="events")


class DoctorCarePlan(Base, TimestampMixin):
    __tablename__ = "doctor_care_plans"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by: Mapped[str] = mapped_column(String(100), default="Dr. Arun Nair")
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="Cognitive & Mobility")
    frequency: Mapped[str] = mapped_column(String(50), default="Daily")
    target: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    start_date: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    end_date: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="doctor_care_plans")
