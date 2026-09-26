from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.medication import MedicationEvent
from app.models.care import HabilitationEvent, CognitiveEvent
from app.models.lifestyle import BehaviourObservation
from app.models.monitoring import SafetyEvent, LocationEvent
from app.models.camera import RecognitionEvent
from app.schemas.timeline import TimelineEventResponse


class TimelineService:
    @staticmethod
    def get_timeline(
        patient_id: str,
        category: str,
        limit: int,
        db: Session
    ) -> List[TimelineEventResponse]:
        events: List[TimelineEventResponse] = []

        # 1. Medication events
        if category in ["all", "medication"]:
            med_evts = db.query(MedicationEvent).filter(
                MedicationEvent.patient_id == patient_id
            ).order_by(desc(MedicationEvent.scheduled_at)).limit(limit).all()

            for me in med_evts:
                is_taken = me.status == "taken"
                severity = "success" if is_taken else "warning" if me.status == "missed" else "info"
                icon = "CheckCircle2" if is_taken else "AlertCircle" if me.status == "missed" else "Pill"
                events.append(TimelineEventResponse(
                    id=f"tl-{me.id}",
                    timestamp=me.scheduled_at.isoformat(),
                    timeDisplay=me.scheduled_at.strftime("%I:%M %p"),
                    title=f"Medication {me.status.capitalize()}: {me.medication_name}",
                    description=f"{me.medication_name} ({me.dosage}) {me.status}. Acknowledged by: {me.acknowledged_by or 'Caregiver'}.",
                    category="medication",
                    severity=severity,
                    iconName=icon
                ))

        # 2. Habilitation & Cognitive activities
        if category in ["all", "activities", "care_plan"]:
            hab_evts = db.query(HabilitationEvent).filter(
                HabilitationEvent.patient_id == patient_id
            ).order_by(desc(HabilitationEvent.scheduled_at)).limit(limit).all()

            for he in hab_evts:
                events.append(TimelineEventResponse(
                    id=f"tl-{he.id}",
                    timestamp=he.scheduled_at.isoformat(),
                    timeDisplay=he.scheduled_at.strftime("%I:%M %p"),
                    title=f"Activity Completed: {he.activity.title if he.activity else 'Care Activity'}",
                    description=f"{he.caregiver_note or 'Completed successfully by patient.'} Response: {he.patient_response}.",
                    category="activities",
                    severity="success",
                    iconName="Sparkles"
                ))

            cog_evts = db.query(CognitiveEvent).filter(
                CognitiveEvent.patient_id == patient_id
            ).order_by(desc(CognitiveEvent.completed_at)).limit(limit).all()

            for ce in cog_evts:
                events.append(TimelineEventResponse(
                    id=f"tl-{ce.id}",
                    timestamp=ce.completed_at.isoformat(),
                    timeDisplay=ce.completed_at.strftime("%I:%M %p"),
                    title=f"Cognitive Task: {ce.activity.title if ce.activity else 'Cognitive Exercise'}",
                    description=f"Performance: {ce.performance or 'Completed'}. {ce.caregiver_note or ''}",
                    category="activities",
                    severity="success",
                    iconName="Brain"
                ))

        # 3. Behaviour observations
        if category in ["all", "behaviour"]:
            obs_evts = db.query(BehaviourObservation).filter(
                BehaviourObservation.patient_id == patient_id
            ).order_by(desc(BehaviourObservation.observed_at)).limit(limit).all()

            for obs in obs_evts:
                sev = "warning" if obs.intensity in ["moderate", "severe"] else "info"
                events.append(TimelineEventResponse(
                    id=f"tl-{obs.id}",
                    timestamp=obs.observed_at.isoformat(),
                    timeDisplay=obs.observed_at.strftime("%I:%M %p"),
                    title=f"Caregiver Observation: {obs.observation_type.capitalize()}",
                    description=f"{obs.note} ({obs.caregiver_action_taken or ''})",
                    category="behaviour",
                    severity=sev,
                    iconName="Eye"
                ))

        # 4. Safety events (SOS, geofence)
        if category in ["all", "safety"]:
            saf_evts = db.query(SafetyEvent).filter(
                SafetyEvent.patient_id == patient_id
            ).order_by(desc(SafetyEvent.occurred_at)).limit(limit).all()

            for se in saf_evts:
                sev = "alert" if se.severity in ["critical", "high"] else "warning"
                icon = "AlertTriangle" if "sos" in se.event_type else "MapPin"
                events.append(TimelineEventResponse(
                    id=f"tl-{se.id}",
                    timestamp=se.occurred_at.isoformat(),
                    timeDisplay=se.occurred_at.strftime("%I:%M %p"),
                    title=f"Safety Alert: {se.event_type.replace('_', ' ').title()}",
                    description=se.description,
                    category="safety",
                    severity=sev,
                    iconName=icon
                ))

        # 5. Location / Safe Zone events
        if category in ["all", "location"]:
            loc_evts = db.query(LocationEvent).filter(
                LocationEvent.patient_id == patient_id
            ).order_by(desc(LocationEvent.recorded_at)).limit(limit).all()

            for le in loc_evts:
                sev = "alert" if le.status != "at_home" else "success"
                title = "Safe Zone Exit Alert" if le.status != "at_home" else "Location Safe (At Home)"
                events.append(TimelineEventResponse(
                    id=f"tl-{le.id}",
                    timestamp=le.recorded_at.isoformat(),
                    timeDisplay=le.recorded_at.strftime("%I:%M %p"),
                    title=title,
                    description=f"Current address: {le.address} (Source: {le.source})",
                    category="location",
                    severity=sev,
                    iconName="MapPin" if le.status != "at_home" else "Home"
                ))

        # 6. Camera Recognition events
        if category in ["all", "camera"]:
            cam_evts = db.query(RecognitionEvent).filter(
                RecognitionEvent.patient_id == patient_id
            ).order_by(desc(RecognitionEvent.detected_at)).limit(limit).all()

            for ce in cam_evts:
                is_rec = ce.status == "recognized"
                sev = "info" if is_rec else "warning"
                title = "Familiar Person Detected" if is_rec else "Unidentified Visitor at Doorstep"
                description_text = f"{ce.detected_name} ({ce.relation}) detected by {ce.camera_location} ({ce.confidence_score:.1f}% confidence)."
                events.append(TimelineEventResponse(
                    id=f"tl-{ce.id}",
                    timestamp=ce.detected_at.isoformat(),
                    timeDisplay=ce.detected_at.strftime("%I:%M %p"),
                    title=title,
                    description=description_text,
                    category="camera",
                    severity=sev,
                    iconName="UserCheck" if is_rec else "UserX"
                ))

        # Sort all aggregated events descending by timestamp
        events.sort(key=lambda e: e.timestamp, reverse=True)
        return events[:limit]
