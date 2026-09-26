from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    condition: Mapped[str] = mapped_column(String(100), default="Mild-to-Moderate Dementia")
    stage: Mapped[str] = mapped_column(String(50), default="Stage 2 · Moderate")
    status: Mapped[str] = mapped_column(String(20), default="stable", index=True)  # stable, attention, critical
    
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    medical_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mobility_level: Mapped[Optional[str]] = mapped_column(String(50), default="independent")
    communication_preferences: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    known_triggers: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Relationships
    caregivers: Mapped[List["CaregiverPatient"]] = relationship("CaregiverPatient", back_populates="patient", cascade="all, delete-orphan")
    care_team: Mapped[List["CareTeamMember"]] = relationship("CareTeamMember", back_populates="patient", cascade="all, delete-orphan")
    safe_zones: Mapped[List["SafeZone"]] = relationship("SafeZone", back_populates="patient", cascade="all, delete-orphan")
    medications: Mapped[List["Medication"]] = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    routines: Mapped[List["Routine"]] = relationship("Routine", back_populates="patient", cascade="all, delete-orphan")
    habilitation_activities: Mapped[List["HabilitationActivity"]] = relationship("HabilitationActivity", back_populates="patient", cascade="all, delete-orphan")
    cognitive_activities: Mapped[List["CognitiveActivity"]] = relationship("CognitiveActivity", back_populates="patient", cascade="all, delete-orphan")
    doctor_care_plans: Mapped[List["DoctorCarePlan"]] = relationship("DoctorCarePlan", back_populates="patient", cascade="all, delete-orphan")
    behaviour_observations: Mapped[List["BehaviourObservation"]] = relationship("BehaviourObservation", back_populates="patient", cascade="all, delete-orphan")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    pendant: Mapped[Optional["PendantDevice"]] = relationship("PendantDevice", back_populates="patient", uselist=False, cascade="all, delete-orphan")
    familiar_people: Mapped[List["FamiliarPerson"]] = relationship("FamiliarPerson", back_populates="patient", cascade="all, delete-orphan")
    ai_recommendations: Mapped[List["AIRecommendation"]] = relationship("AIRecommendation", back_populates="patient", cascade="all, delete-orphan")
    ai_insights: Mapped[List["AIInsight"]] = relationship("AIInsight", back_populates="patient", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="patient", cascade="all, delete-orphan")
    reports: Mapped[List["CareReport"]] = relationship("CareReport", back_populates="patient", cascade="all, delete-orphan")
    medical_documents: Mapped[List["MedicalDocument"]] = relationship("MedicalDocument", back_populates="patient", cascade="all, delete-orphan")


class SafeZone(Base, TimestampMixin):
    __tablename__ = "safe_zones"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), default="Home Safe Zone")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    radius_meters: Mapped[int] = mapped_column(Integer, default=150)
    address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="safe_zones")
