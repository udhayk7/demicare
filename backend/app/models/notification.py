from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    __tablename__ = "notifications"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(50), ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    notification_type: Mapped[str] = mapped_column(String(50), default="medication", index=True)  # medication, safety, ai, system
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), default="info")  # info, warning, alert, success
    read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    timestamp_label: Mapped[str] = mapped_column(String(50), default="Just now")

    user: Mapped[Optional["User"]] = relationship("User", back_populates="notifications")
    patient: Mapped["Patient"] = relationship("Patient", back_populates="notifications")
