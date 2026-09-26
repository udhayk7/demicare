import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.patient import Patient, SafeZone
from app.models.monitoring import LocationEvent, MovementLog, SleepLog, SafetyEvent, PendantDevice
from app.models.notification import Notification
from app.schemas.monitoring import (
    LocationResponse,
    MovementResponse,
    SleepResponse,
    PendantResponse,
    SafetyEventResponse,
    Coordinates,
    MonitoringSummaryResponse
)


class MonitoringService:
    @staticmethod
    def get_location(patient_id: str, db: Session) -> LocationResponse:
        loc = db.query(LocationEvent).filter(
            LocationEvent.patient_id == patient_id
        ).order_by(desc(LocationEvent.recorded_at)).first()

        safe_zone = db.query(SafeZone).filter(
            SafeZone.patient_id == patient_id,
            SafeZone.active == True
        ).first()

        cur_lat = loc.latitude if loc else 12.9250
        cur_lng = loc.longitude if loc else 77.6850
        sz_lat = safe_zone.latitude if safe_zone else 12.9250
        sz_lng = safe_zone.longitude if safe_zone else 77.6850
        radius = safe_zone.radius_meters if safe_zone else 150

        return LocationResponse(
            status=loc.status if loc else "at_home",
            address=loc.address if loc else "42 Jasmine Gardens, Green Glen Layout, Bengaluru",
            coordinates=Coordinates(lat=cur_lat, lng=cur_lng),
            safeZoneCenter=Coordinates(lat=sz_lat, lng=sz_lng),
            safeZoneRadiusMeters=radius,
            lastUpdated="2 min ago",
            batteryLevel=78
        )

    @staticmethod
    def get_movement(patient_id: str, db: Session) -> MovementResponse:
        mov = db.query(MovementLog).filter(
            MovementLog.patient_id == patient_id
        ).order_by(desc(MovementLog.log_date)).first()

        return MovementResponse(
            dailyKm=mov.daily_km if mov else 3.1,
            steps=mov.steps if mov else 4250,
            activityLevel=mov.activity_level if mov else "normal",
            lastMovementTime=mov.last_movement_time if mov else "15 min ago"
        )

    @staticmethod
    def get_sleep(patient_id: str, db: Session) -> SleepResponse:
        slp = db.query(SleepLog).filter(
            SleepLog.patient_id == patient_id
        ).order_by(desc(SleepLog.recorded_date)).first()

        return SleepResponse(
            durationHours=slp.duration_hours if slp else 7.33,
            quality=slp.quality if slp else "restful",
            sleepStart=slp.sleep_start if slp else "10:15 PM",
            sleepEnd=slp.sleep_end if slp else "05:35 AM",
            nightWakeups=slp.night_wakeups if slp else 1
        )

    @staticmethod
    def get_pendant(patient_id: str, db: Session) -> PendantResponse:
        pend = db.query(PendantDevice).filter(
            PendantDevice.patient_id == patient_id
        ).first()

        return PendantResponse(
            connected=pend.status == "online" if pend else True,
            batteryLevel=pend.battery_percentage if pend else 78,
            gpsStatus=pend.gps_status if pend else "available",
            speakerStatus=pend.speaker_status if pend else "working",
            lastSync="2 min ago",
            remindersActive=pend.reminders_active if pend else True
        )

    @staticmethod
    def get_safety_events(patient_id: str, db: Session) -> List[SafetyEventResponse]:
        events = db.query(SafetyEvent).filter(
            SafetyEvent.patient_id == patient_id
        ).order_by(desc(SafetyEvent.occurred_at)).all()

        return [
            SafetyEventResponse(
                id=e.id,
                timestamp=e.occurred_at.strftime("%d %b %H:%M"),
                type=e.event_type,
                severity=e.severity,
                resolved=e.resolved,
                description=e.description
            )
            for e in events
        ]

    @staticmethod
    def trigger_sos(patient_id: str, source: str, db: Session) -> SafetyEventResponse:
        now = datetime.now(timezone.utc)
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if patient:
            patient.status = "critical"

        pend = db.query(PendantDevice).filter(PendantDevice.patient_id == patient_id).first()
        if pend:
            pend.battery_percentage = max(10, pend.battery_percentage - 5)

        new_safe = SafetyEvent(
            id=f"safe-sos-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            event_type="sos_button",
            severity="critical",
            resolved=False,
            description="Emergency SOS trigger received via " + source,
            occurred_at=now,
            source=source
        )
        db.add(new_safe)

        # Create critical notification
        notif = Notification(
            id=f"notif-sos-{int(now.timestamp())}-{uuid.uuid4().hex[:6]}",
            patient_id=patient_id,
            notification_type="safety",
            title="🚨 CRITICAL SOS ALERT",
            message=f"{patient.name if patient else 'Patient'} triggered emergency SOS from {source}.",
            severity="alert",
            read=False,
            timestamp_label="Just now"
        )
        db.add(notif)

        db.commit()
        db.refresh(new_safe)

        return SafetyEventResponse(
            id=new_safe.id,
            timestamp="Just now",
            type=new_safe.event_type,
            severity=new_safe.severity,
            resolved=new_safe.resolved,
            description=new_safe.description
        )

    @staticmethod
    def get_summary(patient_id: str, db: Session) -> MonitoringSummaryResponse:
        return MonitoringSummaryResponse(
            location=MonitoringService.get_location(patient_id, db),
            movement=MonitoringService.get_movement(patient_id, db),
            sleep=MonitoringService.get_sleep(patient_id, db),
            pendant=MonitoringService.get_pendant(patient_id, db),
            safetyEvents=MonitoringService.get_safety_events(patient_id, db)
        )
