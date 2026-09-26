from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class LocationEvent(Base, TimestampMixin):
    __tablename__ = "location_events"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(String(255), default="42 Jasmine Gardens, Green Glen Layout, Bengaluru")
    status: Mapped[str] = mapped_column(String(30), default="at_home", index=True)  # at_home, safe_zone_exit, wandering
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    source: Mapped[str] = mapped_column(String(50), default="mock_pendant")  # mock_pendant, real_pendant, manual


class MovementLog(Base, TimestampMixin):
    __tablename__ = "movement_logs"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    log_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    daily_km: Mapped[float] = mapped_column(Float, default=3.1)
    steps: Mapped[int] = mapped_column(Integer, default=4250)
    active_minutes: Mapped[int] = mapped_column(Integer, default=45)
    activity_level: Mapped[str] = mapped_column(String(30), default="normal")  # low, normal, active
    last_movement_time: Mapped[str] = mapped_column(String(50), default="15 min ago")
    source: Mapped[str] = mapped_column(String(50), default="mock_pendant")


class SleepLog(Base, TimestampMixin):
    __tablename__ = "sleep_logs"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    sleep_start: Mapped[str] = mapped_column(String(50), default="10:15 PM")
    sleep_end: Mapped[str] = mapped_column(String(50), default="05:35 AM")
    duration_hours: Mapped[float] = mapped_column(Float, default=7.33)
    quality: Mapped[str] = mapped_column(String(30), default="restful")  # restful, restless, interrupted
    night_wakeups: Mapped[int] = mapped_column(Integer, default=1)
    movement_level: Mapped[str] = mapped_column(String(30), default="low")
    recorded_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), default="mock_pendant")


class SafetyEvent(Base, TimestampMixin):
    __tablename__ = "safety_events"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # sos_button, fall_detected, geofence_exit, pendant_disconnected
    severity: Mapped[str] = mapped_column(String(30), default="critical")  # low, medium, high, critical
    resolved: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    source: Mapped[str] = mapped_column(String(50), default="mock_pendant")  # mock_pendant, real_pendant, app


class PendantDevice(Base, TimestampMixin):
    __tablename__ = "pendant_devices"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), unique=True, nullable=False)
    device_identifier: Mapped[str] = mapped_column(String(100), default="PENDANT-CARE-7789")
    status: Mapped[str] = mapped_column(String(30), default="online")  # online, offline, low_battery
    battery_percentage: Mapped[int] = mapped_column(Integer, default=78)
    gps_status: Mapped[str] = mapped_column(String(30), default="available")  # available, low_accuracy, unavailable
    speaker_status: Mapped[str] = mapped_column(String(30), default="working")  # working, muted
    reminders_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_sync_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    firmware_version: Mapped[str] = mapped_column(String(50), default="v2.1.4-build26")

    patient: Mapped["Patient"] = relationship("Patient", back_populates="pendant")
