import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.care import Routine, HabilitationActivity, HabilitationEvent, CognitiveActivity, CognitiveEvent
from app.models.lifestyle import BehaviourObservation, Appointment, MealLog, HydrationLog
from app.schemas.care import (
    RoutineResponse,
    HabilitationResponse,
    CognitiveResponse,
    ObservationCreate,
    ObservationResponse,
    AppointmentResponse,
    HydrationLogCreate,
    HydrationLogResponse,
    MealLogCreate,
    MealLogResponse
)


class CareService:
    @staticmethod
    def get_routines(patient_id: str, db: Session) -> List[RoutineResponse]:
        routines = db.query(Routine).filter(Routine.patient_id == patient_id).order_by(Routine.id).all()
        return [
            RoutineResponse(
                id=r.id,
                title=r.title,
                category=r.category,
                completed=r.completed_count,
                total=r.total_count
            )
            for r in routines
        ]

    @staticmethod
    def get_habilitation(patient_id: str, db: Session) -> List[HabilitationResponse]:
        habs = db.query(HabilitationActivity).filter(HabilitationActivity.patient_id == patient_id).order_by(HabilitationActivity.id).all()
        return [
            HabilitationResponse(
                id=h.id,
                title=h.title,
                category=h.category,
                durationMinutes=h.duration_minutes,
                completed=h.completed,
                scheduledTime=h.scheduled_time
            )
            for h in habs
        ]

    @staticmethod
    def toggle_habilitation(activity_id: str, db: Session) -> HabilitationResponse:
        hab = db.query(HabilitationActivity).filter(HabilitationActivity.id == activity_id).first()
        if not hab:
            raise ValueError(f"Habilitation activity {activity_id} not found")

        hab.completed = not hab.completed
        now = datetime.now(timezone.utc)

        if hab.completed:
            evt = HabilitationEvent(
                id=f"he-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
                activity_id=hab.id,
                patient_id=hab.patient_id,
                scheduled_at=now,
                completed_at=now,
                status="completed",
                assistance_level="independent",
                patient_response="enjoyed",
                caregiver_note="Activity completed by caregiver toggle."
            )
            db.add(evt)

        # Update routines counter
        rout = db.query(Routine).filter(
            Routine.patient_id == hab.patient_id,
            Routine.category == "activities"
        ).first()
        if rout:
            if hab.completed:
                rout.completed_count = min(rout.total_count, rout.completed_count + 1)
            else:
                rout.completed_count = max(0, rout.completed_count - 1)

        db.commit()
        db.refresh(hab)

        return HabilitationResponse(
            id=hab.id,
            title=hab.title,
            category=hab.category,
            durationMinutes=hab.duration_minutes,
            completed=hab.completed,
            scheduledTime=hab.scheduled_time
        )

    @staticmethod
    def get_cognitive(patient_id: str, db: Session) -> List[CognitiveResponse]:
        cogs = db.query(CognitiveActivity).filter(CognitiveActivity.patient_id == patient_id).order_by(CognitiveActivity.id).all()
        return [
            CognitiveResponse(
                id=c.id,
                title=c.title,
                type=c.activity_type,
                durationMinutes=c.duration_minutes,
                completed=c.completed,
                score=c.score
            )
            for c in cogs
        ]

    @staticmethod
    def toggle_cognitive(activity_id: str, db: Session) -> CognitiveResponse:
        cog = db.query(CognitiveActivity).filter(CognitiveActivity.id == activity_id).first()
        if not cog:
            raise ValueError(f"Cognitive activity {activity_id} not found")

        cog.completed = not cog.completed
        now = datetime.now(timezone.utc)

        if cog.completed:
            evt = CognitiveEvent(
                id=f"ce-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
                activity_id=cog.id,
                patient_id=cog.patient_id,
                completed_at=now,
                performance="Completed",
                patient_response="enjoyed",
                caregiver_note="Cognitive exercise session completed."
            )
            db.add(evt)

        # Update routines counter
        rout = db.query(Routine).filter(
            Routine.patient_id == cog.patient_id,
            Routine.category == "cognitive"
        ).first()
        if rout:
            if cog.completed:
                rout.completed_count = min(rout.total_count, rout.completed_count + 1)
            else:
                rout.completed_count = max(0, rout.completed_count - 1)

        db.commit()
        db.refresh(cog)

        return CognitiveResponse(
            id=cog.id,
            title=cog.title,
            type=cog.activity_type,
            durationMinutes=cog.duration_minutes,
            completed=cog.completed,
            score=cog.score
        )

    @staticmethod
    def get_observations(patient_id: str, db: Session) -> List[ObservationResponse]:
        obs = db.query(BehaviourObservation).filter(
            BehaviourObservation.patient_id == patient_id
        ).order_by(desc(BehaviourObservation.observed_at)).all()

        return [
            ObservationResponse(
                id=o.id,
                timestamp=o.observed_at.strftime("%I:%M %p"),
                type=o.observation_type,
                note=o.note,
                intensity=o.intensity,
                caregiverActionTaken=o.caregiver_action_taken
            )
            for o in obs
        ]

    @staticmethod
    def create_observation(
        patient_id: str,
        data: ObservationCreate,
        user_name: str,
        db: Session
    ) -> ObservationResponse:
        now = datetime.now(timezone.utc)
        new_obs = BehaviourObservation(
            id=f"obs-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            observation_type=data.type,
            note=data.note,
            intensity=data.intensity or "mild",
            caregiver_action_taken=data.caregiverActionTaken or "Logged & observed by caregiver.",
            observed_at=now,
            created_by=user_name
        )
        db.add(new_obs)
        db.commit()
        db.refresh(new_obs)

        return ObservationResponse(
            id=new_obs.id,
            timestamp=now.strftime("%I:%M %p"),
            type=new_obs.observation_type,
            note=new_obs.note,
            intensity=new_obs.intensity,
            caregiverActionTaken=new_obs.caregiver_action_taken
        )

    @staticmethod
    def get_appointments(patient_id: str, db: Session) -> List[AppointmentResponse]:
        apps = db.query(Appointment).filter(Appointment.patient_id == patient_id).order_by(Appointment.id).all()
        return [
            AppointmentResponse(
                id=a.id,
                title=a.title,
                doctor=a.doctor,
                specialty=a.specialty,
                date=a.date_str,
                time=a.time_str,
                location=a.location,
                status=a.status
            )
            for a in apps
        ]

    @staticmethod
    def log_hydration(
        patient_id: str,
        data: HydrationLogCreate,
        db: Session
    ) -> HydrationLogResponse:
        now = datetime.now(timezone.utc)
        log = HydrationLog(
            id=f"hyd-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            amount=data.amount,
            unit=data.unit,
            recorded_at=now,
            source="caregiver"
        )
        db.add(log)

        # Update routine hydration count
        rout = db.query(Routine).filter(
            Routine.patient_id == patient_id,
            Routine.category == "hydration"
        ).first()
        if rout:
            rout.completed_count = min(rout.total_count, rout.completed_count + data.amount)

        db.commit()

        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_total = db.query(HydrationLog).filter(
            HydrationLog.patient_id == patient_id,
            HydrationLog.recorded_at >= today_start
        ).count()

        return HydrationLogResponse(
            id=log.id,
            amount=log.amount,
            unit=log.unit,
            recordedAt=now.strftime("%I:%M %p"),
            todayTotal=rout.completed_count if rout else today_total
        )

    @staticmethod
    def log_meal(
        patient_id: str,
        data: MealLogCreate,
        db: Session
    ) -> MealLogResponse:
        now = datetime.now(timezone.utc)
        log = MealLog(
            id=f"meal-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            meal_type=data.mealType,
            recorded_at=now,
            intake_level=data.intakeLevel,
            appetite="normal",
            notes=data.notes
        )
        db.add(log)

        # Update routine meals count if present
        rout = db.query(Routine).filter(
            Routine.patient_id == patient_id,
            Routine.category == "meals"
        ).first()
        if rout:
            rout.completed_count = min(rout.total_count, rout.completed_count + 1)

        db.commit()

        return MealLogResponse(
            id=log.id,
            mealType=log.meal_type,
            intakeLevel=log.intake_level,
            recordedAt=now.strftime("%I:%M %p"),
            notes=log.notes
        )

