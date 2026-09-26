from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="caregiver")  # caregiver, secondary_caregiver, doctor, admin
    profile_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    caregiver_relations: Mapped[List["CaregiverPatient"]] = relationship("CaregiverPatient", back_populates="user", cascade="all, delete-orphan")
    notifications: Mapped[List["Notification"]] = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class CaregiverPatient(Base, TimestampMixin):
    __tablename__ = "caregiver_patient"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    caregiver_id: Mapped[str] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_name: Mapped[str] = mapped_column(String(50), nullable=False)  # Daughter, Son, Spouse, Nurse
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    permissions: Mapped[str] = mapped_column(String(200), default="read,write,admin")

    user: Mapped["User"] = relationship("User", back_populates="caregiver_relations")
    patient: Mapped["Patient"] = relationship("Patient", back_populates="caregivers")


class CareTeamMember(Base, TimestampMixin):
    __tablename__ = "care_team_members"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # Neurologist, General Physician, Nurse, Primary Caregiver
    specialty: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    contact: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    permissions: Mapped[str] = mapped_column(String(200), default="read")

    patient: Mapped["Patient"] = relationship("Patient", back_populates="care_team")
