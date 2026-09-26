import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.medication import Medication, MedicationEvent
from app.models.care import Routine
from app.models.notification import Notification
from app.schemas.medication import MedicationResponse, MedicationCreate


class MedicationService:
    @staticmethod
    def get_medications(patient_id: str, db: Session) -> List[MedicationResponse]:
        meds = db.query(Medication).filter(Medication.patient_id == patient_id).order_by(Medication.scheduled_time).all()
        return [
            MedicationResponse(
                id=m.id,
                name=m.name,
                dosage=m.dosage,
                scheduledTime=m.scheduled_time,
                status=m.status,
                instructions=m.instructions,
                icon=m.icon
            )
            for m in meds
        ]

    @staticmethod
    def acknowledge_medication(
        medication_id: str,
        status: str,
        acknowledged_by: str,
        db: Session
    ) -> MedicationResponse:
        med = db.query(Medication).filter(Medication.id == medication_id).first()
        if not med:
            raise ValueError(f"Medication {medication_id} not found")

        med.status = status
        now = datetime.now(timezone.utc)

        # Create or update event
        event = MedicationEvent(
            id=f"me-evt-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            medication_id=med.id,
            patient_id=med.patient_id,
            medication_name=med.name,
            dosage=med.dosage,
            scheduled_at=now,
            status=status,
            acknowledged_at=now if status == "taken" else None,
            acknowledged_by=acknowledged_by if status == "taken" else None,
            source="app"
        )
        db.add(event)

        # Update medication routine count if taken
        if status == "taken":
            routine = db.query(Routine).filter(
                Routine.patient_id == med.patient_id,
                Routine.category == "medication"
            ).first()
            if routine:
                routine.completed_count = min(routine.total_count, routine.completed_count + 1)

        db.commit()
        db.refresh(med)

        return MedicationResponse(
            id=med.id,
            name=med.name,
            dosage=med.dosage,
            scheduledTime=med.scheduled_time,
            status=med.status,
            instructions=med.instructions,
            icon=med.icon
        )

    @staticmethod
    def create_medication(
        patient_id: str,
        data: MedicationCreate,
        db: Session
    ) -> MedicationResponse:
        new_id = f"med-{int(datetime.now(timezone.utc).timestamp())}-{uuid.uuid4().hex[:6]}"
        med = Medication(
            id=new_id,
            patient_id=patient_id,
            name=data.name,
            dosage=data.dosage,
            scheduled_time=data.scheduled_time,
            status="pending",
            instructions=data.instructions or "",
            icon=data.icon or "Pill",
            reminder_enabled=data.reminder_enabled if data.reminder_enabled is not None else True
        )
        db.add(med)

        # Increment routine total count
        routine = db.query(Routine).filter(
            Routine.patient_id == patient_id,
            Routine.category == "medication"
        ).first()
        if routine:
            routine.total_count += 1

        db.commit()
        db.refresh(med)

        return MedicationResponse(
            id=med.id,
            name=med.name,
            dosage=med.dosage,
            scheduledTime=med.scheduled_time,
            status=med.status,
            instructions=med.instructions,
            icon=med.icon
        )

    @staticmethod
    def calculate_adherence(patient_id: str, db: Session, days: int = 30) -> int:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        events = db.query(MedicationEvent).filter(
            MedicationEvent.patient_id == patient_id,
            MedicationEvent.scheduled_at >= since
        ).all()
        if not events:
            return 91  # Default benchmark for demonstration
        taken = sum(1 for e in events if e.status == "taken")
        return int(round((taken / len(events)) * 100))
