from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, TimestampMixin


class AIRecommendation(Base, TimestampMixin):
    __tablename__ = "ai_recommendations"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(100), default="Sensory Habilitation")
    duration_minutes: Mapped[int] = mapped_column(Integer, default=15)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_time: Mapped[str] = mapped_column(String(50), default="In 15 mins")
    status: Mapped[str] = mapped_column(String(30), default="suggested", index=True)  # suggested, started, completed, not_suitable
    icon: Mapped[str] = mapped_column(String(50), default="Sparkles")
    priority: Mapped[str] = mapped_column(String(20), default="normal")
    clinical_disclaimer: Mapped[str] = mapped_column(
        String(255),
        default="Care suggestions are supportive non-pharmacological recommendations and do not replace professional medical advice."
    )
    observed: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_it_matters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    suggested_action: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    why_this_activity: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    safety_care_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expected_outcome: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    caregiver_feedback: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="ai_recommendations")
    feedbacks: Mapped[List["AIFeedback"]] = relationship("AIFeedback", back_populates="recommendation", cascade="all, delete-orphan")



class AIInsight(Base, TimestampMixin):
    __tablename__ = "ai_insights"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # sleep, activity, medication, mood
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp_label: Mapped[str] = mapped_column(String(50), default="Today")
    metric: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="ai_insights")


class AIFeedback(Base, TimestampMixin):
    __tablename__ = "ai_feedbacks"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    recommendation_id: Mapped[str] = mapped_column(String(50), ForeignKey("ai_recommendations.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    feedback_response: Mapped[str] = mapped_column(String(50), default="enjoyed")  # enjoyed, neutral, disliked, tired
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    recommendation: Mapped["AIRecommendation"] = relationship("AIRecommendation", back_populates="feedbacks")


class PatientPreference(Base, TimestampMixin):
    __tablename__ = "patient_preferences"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(50), ForeignKey("patients.id", ondelete="CASCADE"), unique=True, nullable=False)
    likes: Mapped[str] = mapped_column(Text, default="gardening, music, balcony walks, family photographs")
    dislikes: Mapped[str] = mapped_column(Text, default="complex puzzles, loud sudden noises")
