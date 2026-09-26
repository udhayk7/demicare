import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.patient import Patient, SafeZone
from app.models.medication import Medication, MedicationEvent
from app.models.monitoring import LocationEvent, SafetyEvent, PendantDevice
from app.models.camera import FamiliarPerson, RecognitionEvent
from app.models.ai import AIRecommendation
from app.models.notification import Notification
from app.models.care import Routine


class SimulationService:
    @staticmethod
    def simulate_medication_reminder(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.status = "attention"

        # Find or use evening Donepezil
        med = db.query(Medication).filter(
            Medication.patient_id == patient_id,
            Medication.name.ilike("%Donepezil%"),
            Medication.scheduled_time == "21:00"
        ).first()

        med_name = med.name if med else "Donepezil"
        med_dosage = med.dosage if med else "5 mg"

        # Create alert notification
        notif = Notification(
            id=f"notif-med-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="medication",
            title="Medication Alert",
            message=f"{med_name} {med_dosage} scheduled for 9:00 PM needs confirmation.",
            severity="warning",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)
        db.commit()

        return {
            "success": True,
            "message": f"Evening medication reminder triggered for {med_name} {med_dosage}."
        }

    @staticmethod
    def simulate_sos(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.status = "critical"

        pend = db.query(PendantDevice).filter(PendantDevice.patient_id == patient_id).first()
        if pend:
            pend.battery_percentage = max(10, pend.battery_percentage - 5)

        safe_evt = SafetyEvent(
            id=f"safe-sos-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            event_type="sos_button",
            severity="critical",
            resolved=False,
            description="Patient pressed emergency panic button on wearable pendant.",
            occurred_at=now,
            source="mock_pendant"
        )
        db.add(safe_evt)

        notif = Notification(
            id=f"notif-sos-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="safety",
            title="🚨 CRITICAL SOS ALERT",
            message=f"{patient.name if patient else 'Raghavan'} pressed the Pendant SOS button at home.",
            severity="alert",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)
        db.commit()

        return {
            "success": True,
            "message": "Emergency SOS triggered on wearable pendant."
        }

    @staticmethod
    def simulate_geofence_exit(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.status = "attention"

        # Update location to beyond 150m
        loc = LocationEvent(
            id=f"loc-exit-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            latitude=12.9268,
            longitude=77.6872,
            address="Near East Gate Alleyway (180m from home)",
            status="safe_zone_exit",
            recorded_at=now,
            source="mock_pendant"
        )
        db.add(loc)

        safe_evt = SafetyEvent(
            id=f"safe-geo-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            event_type="geofence_exit",
            severity="high",
            resolved=False,
            description="Patient left 150m safe perimeter around 42 Jasmine Gardens.",
            occurred_at=now,
            source="mock_pendant"
        )
        db.add(safe_evt)

        notif = Notification(
            id=f"notif-geo-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="safety",
            title="📍 Safe Zone Boundary Exit",
            message="Patient crossed 150m perimeter near East Gate Alleyway.",
            severity="alert",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)
        db.commit()

        return {
            "success": True,
            "message": "Patient exited 150m safe boundary."
        }

    @staticmethod
    def simulate_return_home(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.status = "stable"

        loc = LocationEvent(
            id=f"loc-home-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            latitude=12.9250,
            longitude=77.6850,
            address="42 Jasmine Gardens, Green Glen Layout, Bengaluru",
            status="at_home",
            recorded_at=now,
            source="mock_pendant"
        )
        db.add(loc)

        # Resolve active geofence alerts
        active_safes = db.query(SafetyEvent).filter(
            SafetyEvent.patient_id == patient_id,
            SafetyEvent.event_type == "geofence_exit",
            SafetyEvent.resolved == False
        ).all()
        for s in active_safes:
            s.resolved = True
            s.resolved_at = now

        db.commit()

        return {
            "success": True,
            "message": "Patient safely returned inside home perimeter."
        }

    @staticmethod
    def simulate_person_detected(
        patient_id: str,
        person_name: str,
        relation: str,
        confidence: float,
        camera_location: str,
        db: Session
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        fam = db.query(FamiliarPerson).filter(
            FamiliarPerson.patient_id == patient_id,
            FamiliarPerson.name.ilike(f"%{person_name}%")
        ).first()

        if fam:
            fam.last_recognized_at = now

        rec = RecognitionEvent(
            id=f"rec-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            familiar_person_id=fam.id if fam else None,
            detected_name=person_name,
            relation=relation,
            confidence_score=confidence,
            camera_location=camera_location,
            status="recognized",
            detected_at=now,
            source="camera_simulation"
        )
        db.add(rec)

        notif = Notification(
            id=f"notif-cam-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="camera",
            title="📹 Familiar Person Detected",
            message=f"{person_name} ({relation}) recognized at {camera_location}.",
            severity="info",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)
        db.commit()

        return {
            "success": True,
            "message": f"Camera recognized {person_name} ({relation})."
        }

    @staticmethod
    def simulate_unknown_person(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        rec = RecognitionEvent(
            id=f"rec-unk-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            familiar_person_id=None,
            detected_name="Unidentified Person",
            relation="Unknown Visitor",
            confidence_score=42.0,
            camera_location="Front Door Camera",
            status="unknown_visitor",
            detected_at=now,
            source="camera_simulation"
        )
        db.add(rec)

        notif = Notification(
            id=f"notif-unk-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="camera",
            title="⚠️ Unrecognized Visitor at Doorstep",
            message="Camera detected an unknown visitor at the front entrance.",
            severity="warning",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)
        db.commit()

        return {
            "success": True,
            "message": "Camera detected unrecognized visitor at doorstep."
        }

    @staticmethod
    def simulate_low_battery(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        pend = db.query(PendantDevice).filter(PendantDevice.patient_id == patient_id).first()
        if pend:
            pend.battery_percentage = 14
            pend.status = "low_battery"

        notif = Notification(
            id=f"notif-bat-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="safety",
            title="⚠️ Low Pendant Battery (14%)",
            message="Raghavan's pendant dropped below 15%. Please place it on the charging dock.",
            severity="warning",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)
        db.commit()

        return {
            "success": True,
            "message": "Pendant battery dropped to 14%. Warning notification sent."
        }

    @staticmethod
    def resolve_safety_event(patient_id: str, db: Session) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient and patient.status in ["critical", "attention"]:
            patient.status = "stable"

        active_safes = db.query(SafetyEvent).filter(
            SafetyEvent.patient_id == patient_id,
            SafetyEvent.resolved == False
        ).all()
        for s in active_safes:
            s.resolved = True
            s.resolved_at = now

        db.commit()
        return {
            "success": True,
            "message": "Active safety events marked resolved and patient status restored to stable."
        }

    @staticmethod
    def reset_simulations(patient_id: str, db: Session) -> Dict[str, Any]:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.status = "stable"

        pend = db.query(PendantDevice).filter(PendantDevice.patient_id == patient_id).first()
        if pend:
            pend.status = "online"
            pend.battery_percentage = 78

        # Clear unresolved safety events
        active_safes = db.query(SafetyEvent).filter(
            SafetyEvent.patient_id == patient_id,
            SafetyEvent.resolved == False
        ).all()
        for s in active_safes:
            s.resolved = True

        db.commit()

        return {
            "success": True,
            "message": "Simulation states successfully reset to baseline."
        }

