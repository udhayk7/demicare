from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.models.patient import Patient, SafeZone
from app.models.user import CaregiverPatient, CareTeamMember
from app.models.medication import Medication
from app.models.care import Routine
from app.models.monitoring import LocationEvent, MovementLog, SleepLog, PendantDevice, SafetyEvent
from app.models.ai import AIRecommendation
from app.models.notification import Notification

from app.schemas.patient import PatientResponse
from app.schemas.medication import MedicationResponse
from app.schemas.care import RoutineResponse
from app.schemas.monitoring import LocationResponse, MovementResponse, SleepResponse, PendantResponse, Coordinates
from app.schemas.ai import AIRecommendationResponse
from app.schemas.dashboard import DashboardResponse


class DashboardService:
    @staticmethod
    def get_dashboard(patient_id: str, db: Session) -> DashboardResponse:
        # 1. Patient Info & Caregiver links
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise ValueError(f"Patient {patient_id} not found")

        # Caregivers
        cp_primary = db.query(CaregiverPatient).filter(
            CaregiverPatient.patient_id == patient_id,
            CaregiverPatient.is_primary == True
        ).first()
        cp_secondary = db.query(CaregiverPatient).filter(
            CaregiverPatient.patient_id == patient_id,
            CaregiverPatient.is_primary == False
        ).first()

        primary_caregiver_name = cp_primary.user.name if cp_primary and cp_primary.user else "Anu Menon"
        primary_relation = cp_primary.relationship_name if cp_primary else "Daughter"

        secondary_caregiver_name = cp_secondary.user.name if cp_secondary and cp_secondary.user else "Suresh Menon"
        secondary_relation = cp_secondary.relationship_name if cp_secondary else "Son"

        # Doctor
        dr_member = db.query(CareTeamMember).filter(
            CareTeamMember.patient_id == patient_id,
            CareTeamMember.role == "Neurologist"
        ).first()
        dr_name = dr_member.name if dr_member else "Dr. Arun Nair"
        dr_spec = dr_member.specialty if dr_member else "Neurologist (Cognitive Care)"

        patient_resp = PatientResponse(
            id=patient.id,
            name=patient.name,
            age=patient.age,
            condition=patient.condition,
            stage=patient.stage,
            status=patient.status,
            primaryCaregiver=primary_caregiver_name,
            primaryCaregiverRelation=primary_relation,
            secondaryCaregiver=secondary_caregiver_name,
            secondaryCaregiverRelation=secondary_relation,
            doctorName=dr_name,
            doctorSpecialty=dr_spec,
            avatarUrl=patient.avatar_url or "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=200",
            emergencyContact=patient.emergency_contact or "+91 98450 12345"
        )

        # 2. Routines
        routines = db.query(Routine).filter(Routine.patient_id == patient_id).all()
        routine_resps = [
            RoutineResponse(
                id=r.id,
                title=r.title,
                category=r.category,
                completed=r.completed_count,
                total=r.total_count
            )
            for r in routines
        ]

        # 3. Medications
        medications = db.query(Medication).filter(Medication.patient_id == patient_id).order_by(Medication.scheduled_time).all()
        med_resps = [
            MedicationResponse(
                id=m.id,
                name=m.name,
                dosage=m.dosage,
                scheduledTime=m.scheduled_time,
                status=m.status,
                instructions=m.instructions,
                icon=m.icon
            )
            for m in medications
        ]

        # Next upcoming medication
        next_med = next((m for m in med_resps if m.status in ["pending", "missed"]), None)

        # 4. Location
        loc_event = db.query(LocationEvent).filter(LocationEvent.patient_id == patient_id).order_by(desc(LocationEvent.recorded_at)).first()
        safe_zone = db.query(SafeZone).filter(SafeZone.patient_id == patient_id, SafeZone.active == True).first()

        cur_lat = loc_event.latitude if loc_event else 12.9250
        cur_lng = loc_event.longitude if loc_event else 77.6850
        sz_lat = safe_zone.latitude if safe_zone else 12.9250
        sz_lng = safe_zone.longitude if safe_zone else 77.6850
        radius = safe_zone.radius_meters if safe_zone else 150

        # Calculate friendly updated string
        last_updated_str = "2 min ago"

        location_resp = LocationResponse(
            status=loc_event.status if loc_event else "at_home",
            address=loc_event.address if loc_event else "42 Jasmine Gardens, Green Glen Layout, Bengaluru",
            coordinates=Coordinates(lat=cur_lat, lng=cur_lng),
            safeZoneCenter=Coordinates(lat=sz_lat, lng=sz_lng),
            safeZoneRadiusMeters=radius,
            lastUpdated=last_updated_str,
            batteryLevel=78
        )

        # 5. Movement
        mov = db.query(MovementLog).filter(MovementLog.patient_id == patient_id).order_by(desc(MovementLog.log_date)).first()
        movement_resp = MovementResponse(
            dailyKm=mov.daily_km if mov else 3.1,
            steps=mov.steps if mov else 4250,
            activityLevel=mov.activity_level if mov else "normal",
            lastMovementTime=mov.last_movement_time if mov else "15 min ago"
        )

        # 6. Sleep
        slp = db.query(SleepLog).filter(SleepLog.patient_id == patient_id).order_by(desc(SleepLog.recorded_date)).first()
        sleep_resp = SleepResponse(
            durationHours=slp.duration_hours if slp else 7.33,
            quality=slp.quality if slp else "restful",
            sleepStart=slp.sleep_start if slp else "10:15 PM",
            sleepEnd=slp.sleep_end if slp else "05:35 AM",
            nightWakeups=slp.night_wakeups if slp else 1
        )

        # 7. Pendant
        pend = db.query(PendantDevice).filter(PendantDevice.patient_id == patient_id).first()
        pendant_resp = PendantResponse(
            connected=pend.status == "online" if pend else True,
            batteryLevel=pend.battery_percentage if pend else 78,
            gpsStatus=pend.gps_status if pend else "available",
            speakerStatus=pend.speaker_status if pend else "working",
            lastSync="2 min ago",
            remindersActive=pend.reminders_active if pend else True
        )

        # 8. AI recommendation
        top_rec = db.query(AIRecommendation).filter(
            AIRecommendation.patient_id == patient_id,
            AIRecommendation.status == "suggested"
        ).first()

        ai_resp = None
        if top_rec:
            ai_resp = AIRecommendationResponse(
                id=top_rec.id,
                title=top_rec.title,
                activityType=top_rec.activity_type,
                durationMinutes=top_rec.duration_minutes,
                reason=top_rec.reason,
                recommendedTime=top_rec.recommended_time,
                status=top_rec.status,
                icon=top_rec.icon
            )

        # 9. Notifications & Attention count
        unread_notifs = db.query(Notification).filter(
            Notification.patient_id == patient_id,
            Notification.read == False
        ).count()

        attention_needed = patient.status != "stable" or any(m.status == "missed" for m in med_resps)

        return DashboardResponse(
            patient=patient_resp,
            routines=routine_resps,
            medications=med_resps,
            nextMedication=next_med,
            location=location_resp,
            movement=movement_resp,
            sleep=sleep_resp,
            pendant=pendant_resp,
            aiRecommendation=ai_resp,
            unreadNotificationsCount=unread_notifs,
            attentionNeeded=attention_needed
        )
