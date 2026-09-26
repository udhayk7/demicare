import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.camera import FamiliarPerson, RecognitionEvent
from app.models.notification import Notification
from app.schemas.camera import FamiliarPersonResponse, RecognitionEventResponse, CameraIngestRequest


class CameraService:
    @staticmethod
    def get_familiar_people(patient_id: str, db: Session) -> List[FamiliarPersonResponse]:
        people = db.query(FamiliarPerson).filter(
            FamiliarPerson.patient_id == patient_id,
            FamiliarPerson.active == True
        ).all()

        return [
            FamiliarPersonResponse(
                id=p.id,
                name=p.name,
                relation=p.relation,
                avatar=p.avatar,
                lastRecognized="5 min ago" if p.last_recognized_at else "Recently",
                status=p.status
            )
            for p in people
        ]

    @staticmethod
    def get_recognition_events(patient_id: str, db: Session) -> List[RecognitionEventResponse]:
        events = db.query(RecognitionEvent).filter(
            RecognitionEvent.patient_id == patient_id
        ).order_by(desc(RecognitionEvent.detected_at)).all()

        return [
            RecognitionEventResponse(
                id=e.id,
                timestamp=e.detected_at.strftime("%I:%M %p"),
                personName=e.detected_name,
                relation=e.relation,
                confidenceScore=e.confidence_score,
                cameraLocation=e.camera_location,
                status=e.status
            )
            for e in events
        ]

    @staticmethod
    def record_recognition(
        patient_id: str,
        detected_name: str,
        relation: str,
        confidence: float,
        camera_location: str,
        source: str,
        db: Session
    ) -> RecognitionEventResponse:
        now = datetime.now(timezone.utc)
        status = "recognized" if confidence >= 60.0 and detected_name != "Unidentified Person" else "unknown_visitor"

        familiar_person = db.query(FamiliarPerson).filter(
            FamiliarPerson.patient_id == patient_id,
            FamiliarPerson.name.ilike(f"%{detected_name}%")
        ).first()

        if familiar_person:
            familiar_person.last_recognized_at = now

        new_rec = RecognitionEvent(
            id=f"rec-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            familiar_person_id=familiar_person.id if familiar_person else None,
            detected_name=detected_name,
            relation=relation,
            confidence_score=confidence,
            camera_location=camera_location,
            status=status,
            detected_at=now,
            source=source
        )
        db.add(new_rec)

        # Create notification if unknown visitor or recognized
        notif_sev = "warning" if status == "unknown_visitor" else "info"
        notif_title = "⚠️ Unrecognized Visitor" if status == "unknown_visitor" else "📹 Familiar Person Detected"
        notif_msg = f"{detected_name} ({relation}) detected at {camera_location} ({confidence:.1f}% confidence)."

        notif = Notification(
            id=f"notif-cam-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="camera",
            title=notif_title,
            message=notif_msg,
            severity=notif_sev,
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)

        db.commit()
        db.refresh(new_rec)

        return RecognitionEventResponse(
            id=new_rec.id,
            timestamp=now.strftime("%I:%M %p"),
            personName=new_rec.detected_name,
            relation=new_rec.relation,
            confidenceScore=new_rec.confidence_score,
            cameraLocation=new_rec.camera_location,
            status=new_rec.status
        )
