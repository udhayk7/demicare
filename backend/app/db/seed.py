from datetime import datetime, timedelta, timezone
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models import (
    User,
    CaregiverPatient,
    CareTeamMember,
    Patient,
    SafeZone,
    Medication,
    MedicationEvent,
    Routine,
    HabilitationActivity,
    HabilitationEvent,
    CognitiveActivity,
    CognitiveEvent,
    DoctorCarePlan,
    MealLog,
    HydrationLog,
    BehaviourObservation,
    Appointment,
    LocationEvent,
    MovementLog,
    SleepLog,
    SafetyEvent,
    PendantDevice,
    FamiliarPerson,
    RecognitionEvent,
    AIRecommendation,
    AIInsight,
    PatientPreference,
    Notification,
    CareReport,
    MedicalDocument
)


def seed_db():
    db = SessionLocal()
    try:
        # Check if already seeded
        existing_user = db.query(User).filter_by(id="user-anu").first()
        if existing_user:
            print("Database already contains seed data.")
            return

        now = datetime.now(timezone.utc)
        today_date = now.date()

        print("Seeding Users...")
        anu = User(
            id="user-anu",
            name="Anu Menon",
            email="anu.menon@carecompanion.in",
            phone="+91 98450 12345",
            password_hash=get_password_hash("password123"),
            role="caregiver",
            profile_photo="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=150"
        )
        suresh = User(
            id="user-suresh",
            name="Suresh Menon",
            email="suresh.menon@carecompanion.in",
            phone="+91 98450 54321",
            password_hash=get_password_hash("password123"),
            role="secondary_caregiver",
            profile_photo="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150"
        )
        dr_arun = User(
            id="user-dr-arun",
            name="Dr. Arun Nair",
            email="dr.arun@neurocare.in",
            phone="+91 98451 99887",
            password_hash=get_password_hash("doctorpass123"),
            role="doctor",
            profile_photo="https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=150"
        )
        db.add_all([anu, suresh, dr_arun])
        db.flush()

        print("Seeding Patient Raghavan Menon...")
        raghavan = Patient(
            id="pat-101",
            name="Raghavan Menon",
            age=72,
            gender="Male",
            condition="Mild-to-Moderate Dementia",
            stage="Stage 2 · Moderate",
            status="stable",
            avatar_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=200",
            address="42 Jasmine Gardens, Green Glen Layout, Bengaluru",
            emergency_contact="+91 98450 12345",
            medical_notes="Diagnosed with mild-to-moderate Alzheimer's type dementia 18 months ago. Responsive to music reminiscence and consistent daily morning routine.",
            mobility_level="Independent with occasional evening disorientation",
            communication_preferences="Prefers gentle Malayalam and English short phrases; calms with Carnatic music",
            known_triggers="Loud television noises, sudden dusk/sundowning disorientation"
        )
        db.add(raghavan)
        db.flush()

        print("Seeding Caregiver Relationships & Care Team...")
        rel_anu = CaregiverPatient(
            id="cp-1",
            caregiver_id=anu.id,
            patient_id=raghavan.id,
            relationship_name="Daughter",
            is_primary=True,
            permissions="admin,write,read"
        )
        rel_suresh = CaregiverPatient(
            id="cp-2",
            caregiver_id=suresh.id,
            patient_id=raghavan.id,
            relationship_name="Son",
            is_primary=False,
            permissions="read,write"
        )
        db.add_all([rel_anu, rel_suresh])

        team_dr = CareTeamMember(
            id="ct-1",
            patient_id=raghavan.id,
            user_id=dr_arun.id,
            name="Dr. Arun Nair",
            role="Neurologist",
            specialty="Cognitive Care & Neurodegenerative Disorders",
            contact="+91 98451 99887",
            permissions="write,prescribe,read"
        )
        team_anu = CareTeamMember(
            id="ct-2",
            patient_id=raghavan.id,
            user_id=anu.id,
            name="Anu Menon",
            role="Primary Caregiver",
            specialty="Daughter / Primary Daily Care",
            contact="+91 98450 12345",
            permissions="admin"
        )
        team_suresh = CareTeamMember(
            id="ct-3",
            patient_id=raghavan.id,
            user_id=suresh.id,
            name="Suresh Menon",
            role="Secondary Caregiver",
            specialty="Son / Emergency Contact",
            contact="+91 98450 54321",
            permissions="read,write"
        )
        team_nurse = CareTeamMember(
            id="ct-4",
            patient_id=raghavan.id,
            user_id=None,
            name="Lakshmi Amma",
            role="Family Nurse / Care Assistant",
            specialty="Home Care Nurse",
            contact="+91 98452 33445",
            permissions="read,write"
        )
        db.add_all([team_dr, team_anu, team_suresh, team_nurse])

        print("Seeding Safe Zone...")
        home_zone = SafeZone(
            id="zone-home",
            patient_id=raghavan.id,
            name="Home Safe Zone",
            latitude=12.9250,
            longitude=77.6850,
            radius_meters=150,
            address="42 Jasmine Gardens, Green Glen Layout, Bengaluru",
            active=True
        )
        db.add(home_zone)

        print("Seeding Pendant Device...")
        pendant = PendantDevice(
            id="pendant-101",
            patient_id=raghavan.id,
            device_identifier="PENDANT-CARE-7789",
            status="online",
            battery_percentage=78,
            gps_status="available",
            speaker_status="working",
            reminders_active=True,
            last_sync_at=now - timedelta(minutes=2),
            firmware_version="v2.1.4-build26"
        )
        db.add(pendant)

        print("Seeding Medications & Historical Events (91% adherence)...")
        med1 = Medication(
            id="med-1",
            patient_id=raghavan.id,
            name="Donepezil",
            dosage="5 mg",
            scheduled_time="08:00",
            status="taken",
            instructions="Take 1 tablet after morning breakfast with warm water",
            icon="Pill"
        )
        med2 = Medication(
            id="med-2",
            patient_id=raghavan.id,
            name="Vitamin D3 & Calcium",
            dosage="1000 IU",
            scheduled_time="13:00",
            status="taken",
            instructions="Take 1 capsule after lunch",
            icon="Sun"
        )
        med3 = Medication(
            id="med-3",
            patient_id=raghavan.id,
            name="Memantine",
            dosage="10 mg",
            scheduled_time="18:00",
            status="missed",
            instructions="Take 1 tablet before evening tea",
            icon="HeartPulse"
        )
        med4 = Medication(
            id="med-4",
            patient_id=raghavan.id,
            name="Donepezil",
            dosage="5 mg",
            scheduled_time="21:00",
            status="pending",
            instructions="Take 1 tablet 30 minutes before sleep",
            icon="Moon"
        )
        med5 = Medication(
            id="med-5",
            patient_id=raghavan.id,
            name="Melatonin",
            dosage="3 mg",
            scheduled_time="21:30",
            status="pending",
            instructions="Take as needed for sleep routine support",
            icon="Sparkles"
        )
        db.add_all([med1, med2, med3, med4, med5])
        db.flush()

        # Seed 30 days of medication events (91% taken)
        med_events = []
        for day in range(30):
            day_dt = now - timedelta(days=day)
            # Morning Donepezil (always taken)
            med_events.append(MedicationEvent(
                id=f"me-m1-{day}",
                medication_id=med1.id,
                patient_id=raghavan.id,
                medication_name=med1.name,
                dosage=med1.dosage,
                scheduled_at=day_dt.replace(hour=8, minute=0, second=0),
                status="taken",
                acknowledged_at=day_dt.replace(hour=8, minute=12, second=0),
                acknowledged_by="Anu Menon",
                source="app"
            ))
            # Noon Vitamin D (taken 28 out of 30 days)
            status_noon = "taken" if day != 5 and day != 14 else "missed"
            med_events.append(MedicationEvent(
                id=f"me-m2-{day}",
                medication_id=med2.id,
                patient_id=raghavan.id,
                medication_name=med2.name,
                dosage=med2.dosage,
                scheduled_at=day_dt.replace(hour=13, minute=0, second=0),
                status=status_noon,
                acknowledged_at=day_dt.replace(hour=13, minute=5, second=0) if status_noon == "taken" else None,
                acknowledged_by="Anu Menon" if status_noon == "taken" else None,
                source="app"
            ))
            # Evening Memantine (missed occasional evenings)
            status_eve = "missed" if day in [0, 4, 11, 19, 24] else "taken"
            med_events.append(MedicationEvent(
                id=f"me-m3-{day}",
                medication_id=med3.id,
                patient_id=raghavan.id,
                medication_name=med3.name,
                dosage=med3.dosage,
                scheduled_at=day_dt.replace(hour=18, minute=0, second=0),
                status=status_eve,
                acknowledged_at=day_dt.replace(hour=18, minute=15, second=0) if status_eve == "taken" else None,
                acknowledged_by="Anu Menon" if status_eve == "taken" else None,
                source="app"
            ))
            # Night Donepezil
            if day > 0:
                med_events.append(MedicationEvent(
                    id=f"me-m4-{day}",
                    medication_id=med4.id,
                    patient_id=raghavan.id,
                    medication_name=med4.name,
                    dosage=med4.dosage,
                    scheduled_at=day_dt.replace(hour=21, minute=0, second=0),
                    status="taken",
                    acknowledged_at=day_dt.replace(hour=21, minute=10, second=0),
                    acknowledged_by="Anu Menon",
                    source="app"
                ))
        db.add_all(med_events)

        print("Seeding Routines...")
        routines = [
            Routine(id="rout-1", patient_id=raghavan.id, title="Medication", category="medication", completed_count=4, total_count=5),
            Routine(id="rout-2", patient_id=raghavan.id, title="Activities", category="activities", completed_count=6, total_count=7),
            Routine(id="rout-3", patient_id=raghavan.id, title="Cognitive", category="cognitive", completed_count=2, total_count=3),
            Routine(id="rout-4", patient_id=raghavan.id, title="Hydration", category="hydration", completed_count=5, total_count=7),
            Routine(id="rout-5", patient_id=raghavan.id, title="Nutrition", category="nutrition", completed_count=3, total_count=3),
            Routine(id="rout-6", patient_id=raghavan.id, title="Behaviour Log", category="behaviour", completed_count=1, total_count=1),
        ]
        db.add_all(routines)

        print("Seeding Habilitation Activities (83% adherence)...")
        hab1 = HabilitationActivity(
            id="hab-1",
            patient_id=raghavan.id,
            title="Morning Balcony Walk",
            category="Physical",
            duration_minutes=20,
            completed=True,
            scheduled_time="07:30"
        )
        hab2 = HabilitationActivity(
            id="hab-2",
            patient_id=raghavan.id,
            title="Gentle Chair Yoga & Stretch",
            category="Physical",
            duration_minutes=15,
            completed=True,
            scheduled_time="10:00"
        )
        hab3 = HabilitationActivity(
            id="hab-3",
            patient_id=raghavan.id,
            title="Plant Watering & Gardening",
            category="Sensory",
            duration_minutes=15,
            completed=False,
            scheduled_time="16:30"
        )
        hab4 = HabilitationActivity(
            id="hab-4",
            patient_id=raghavan.id,
            title="Evening Classical Music Session",
            category="Auditory",
            duration_minutes=25,
            completed=False,
            scheduled_time="19:00"
        )
        db.add_all([hab1, hab2, hab3, hab4])
        db.flush()

        hab_events = [
            HabilitationEvent(
                id="he-1",
                activity_id=hab1.id,
                patient_id=raghavan.id,
                scheduled_at=now.replace(hour=7, minute=30, second=0),
                completed_at=now.replace(hour=7, minute=50, second=0),
                status="completed",
                assistance_level="independent",
                patient_response="enjoyed",
                caregiver_note="Walked briskly on balcony in morning sunlight."
            ),
            HabilitationEvent(
                id="he-2",
                activity_id=hab2.id,
                patient_id=raghavan.id,
                scheduled_at=now.replace(hour=10, minute=0, second=0),
                completed_at=now.replace(hour=10, minute=18, second=0),
                status="completed",
                assistance_level="gentle_guidance",
                patient_response="enjoyed",
                caregiver_note="Completed neck and shoulder mobility stretches."
            )
        ]
        db.add_all(hab_events)

        print("Seeding Cognitive Activities (86% adherence)...")
        cog1 = CognitiveActivity(
            id="cog-1",
            patient_id=raghavan.id,
            title="Family Photo Album Recognition",
            activity_type="Reminiscence",
            duration_minutes=15,
            completed=True,
            score="9/10 Correct"
        )
        cog2 = CognitiveActivity(
            id="cog-2",
            patient_id=raghavan.id,
            title="Simple Pattern Matching Game",
            activity_type="Executive Function",
            duration_minutes=10,
            completed=True,
            score="Completed"
        )
        cog3 = CognitiveActivity(
            id="cog-3",
            patient_id=raghavan.id,
            title="Story Recall & Naming",
            activity_type="Memory Retrieval",
            duration_minutes=15,
            completed=False
        )
        db.add_all([cog1, cog2, cog3])
        db.flush()

        cog_events = [
            CognitiveEvent(
                id="ce-1",
                activity_id=cog1.id,
                patient_id=raghavan.id,
                completed_at=now.replace(hour=10, minute=15, second=0),
                performance="9/10 Correct",
                patient_response="enjoyed",
                caregiver_note="Recognized Anu, Suresh, and old ancestral home easily."
            ),
            CognitiveEvent(
                id="ce-2",
                activity_id=cog2.id,
                patient_id=raghavan.id,
                completed_at=now.replace(hour=11, minute=30, second=0),
                performance="Completed",
                patient_response="neutral",
                caregiver_note="Matched color card sequences with calm focus."
            )
        ]
        db.add_all(cog_events)

        print("Seeding Doctor Care Plans...")
        plans = [
            DoctorCarePlan(
                id="dcp-1",
                patient_id=raghavan.id,
                created_by="Dr. Arun Nair",
                title="Daily Morning Sunlight Balcony Walk",
                description="20 minutes gentle outdoor walk between 7:30 and 8:30 AM to maintain circadian rhythm and natural Vitamin D synthesis.",
                category="Physical Mobility",
                frequency="Daily",
                target="Daily 20 mins"
            ),
            DoctorCarePlan(
                id="dcp-2",
                patient_id=raghavan.id,
                created_by="Dr. Arun Nair",
                title="Structured Reminiscence & Cognitive Engagement",
                description="Engage in positive autobiographical memory stimulation (family photo albums, familiar classical songs) 15 minutes daily.",
                category="Cognitive Stimulation",
                frequency="Daily",
                target="15 mins"
            ),
            DoctorCarePlan(
                id="dcp-3",
                patient_id=raghavan.id,
                created_by="Dr. Arun Nair",
                title="Regular Hydration & Scheduled Fluid Prompts",
                description="Offer 150ml water/tender coconut water every 2 hours during daytime to reduce evening confusion and urinary risks.",
                category="Hydration",
                frequency="Daily",
                target="7 glasses/day"
            )
        ]
        db.add_all(plans)

        print("Seeding Lifestyle Logs (Meals, Hydration, Observations, Appointments)...")
        meals = [
            MealLog(id="ml-1", patient_id=raghavan.id, meal_type="breakfast", recorded_at=now.replace(hour=8, minute=15, second=0), intake_level="good", appetite="good", notes="Idli, sambar, warm tea"),
            MealLog(id="ml-2", patient_id=raghavan.id, meal_type="lunch", recorded_at=now.replace(hour=13, minute=10, second=0), intake_level="good", appetite="good", notes="Rice, dal, steamed vegetables"),
            MealLog(id="ml-3", patient_id=raghavan.id, meal_type="snack", recorded_at=now.replace(hour=16, minute=30, second=0), intake_level="moderate", appetite="normal", notes="Roasted nuts and warm milk")
        ]
        db.add_all(meals)

        hydrations = [
            HydrationLog(id=f"hyd-{i}", patient_id=raghavan.id, amount=1, unit="glass", recorded_at=now - timedelta(hours=i*2), source="caregiver")
            for i in range(1, 6)
        ]
        db.add_all(hydrations)

        obs1 = BehaviourObservation(
            id="obs-1",
            patient_id=raghavan.id,
            observation_type="confusion",
            note="Slight confusion regarding time of day after afternoon nap. Settled quickly after cup of herbal tea.",
            intensity="mild",
            caregiver_action_taken="Guided to living room window and showed evening sun.",
            possible_trigger="Awakening suddenly from deep daytime sleep",
            observed_at=now.replace(hour=16, minute=45, second=0),
            created_by="Anu Menon"
        )
        db.add(obs1)

        app1 = Appointment(
            id="app-1",
            patient_id=raghavan.id,
            title="Quarterly Cognitive Assessment",
            doctor="Dr. Arun Nair",
            specialty="Neurology",
            date_str="28 Sep 2026",
            time_str="10:30 AM",
            location="Apollo Healthcare Center, Clinic 304",
            status="upcoming",
            reminder_enabled=True
        )
        app2 = Appointment(
            id="app-2",
            patient_id=raghavan.id,
            title="Routine Blood Panel & BP Check",
            doctor="Dr. Meera Sen",
            specialty="General Physician",
            date_str="12 Oct 2026",
            time_str="09:00 AM",
            location="Home Visit by Nurse",
            status="upcoming",
            reminder_enabled=True
        )
        db.add_all([app1, app2])

        print("Seeding Monitoring History (Movement 3.1 km/day, Sleep 7.33 hrs)...")
        loc1 = LocationEvent(
            id="loc-current",
            patient_id=raghavan.id,
            latitude=12.9250,
            longitude=77.6850,
            address="42 Jasmine Gardens, Green Glen Layout, Bengaluru",
            status="at_home",
            recorded_at=now - timedelta(minutes=2),
            source="mock_pendant"
        )
        db.add(loc1)

        movements = []
        sleeps = []
        for i in range(30):
            d = now - timedelta(days=i)
            movements.append(MovementLog(
                id=f"mov-{i}",
                patient_id=raghavan.id,
                log_date=d,
                daily_km=3.1 if i % 4 != 0 else 2.8,
                steps=4250 if i % 4 != 0 else 3900,
                active_minutes=45,
                activity_level="normal",
                last_movement_time="15 min ago",
                source="mock_pendant"
            ))
            sleeps.append(SleepLog(
                id=f"slp-{i}",
                patient_id=raghavan.id,
                sleep_start="10:15 PM",
                sleep_end="05:35 AM",
                duration_hours=7.33 if i % 3 != 0 else 6.8,
                quality="restful" if i % 5 != 0 else "restless",
                night_wakeups=1 if i % 5 != 0 else 2,
                movement_level="low",
                recorded_date=d,
                source="mock_pendant"
            ))
        db.add_all(movements)
        db.add_all(sleeps)

        print("Seeding Safety Events...")
        safe1 = SafetyEvent(
            id="safe-1",
            patient_id=raghavan.id,
            event_type="geofence_exit",
            severity="medium",
            resolved=True,
            description="Patient stepped beyond 150m boundary into front park lane. Escorted back safely by daughter.",
            occurred_at=now - timedelta(days=1, hours=4),
            resolved_at=now - timedelta(days=1, hours=3, minutes=45),
            source="mock_pendant"
        )
        db.add(safe1)

        print("Seeding Familiar People & Recognition Events...")
        fam1 = FamiliarPerson(
            id="fam-1",
            patient_id=raghavan.id,
            name="Anu Menon",
            relation="Daughter (Primary)",
            avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=150",
            status="frequent",
            last_recognized_at=now - timedelta(minutes=5),
            active=True
        )
        fam2 = FamiliarPerson(
            id="fam-2",
            patient_id=raghavan.id,
            name="Suresh Menon",
            relation="Son",
            avatar="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150",
            status="frequent",
            last_recognized_at=now - timedelta(days=1, hours=2),
            active=True
        )
        fam3 = FamiliarPerson(
            id="fam-3",
            patient_id=raghavan.id,
            name="Lakshmi Amma",
            relation="Family Nurse / Care Assistant",
            avatar="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=150",
            status="recent",
            last_recognized_at=now - timedelta(hours=6),
            active=True
        )
        db.add_all([fam1, fam2, fam3])
        db.flush()

        rec1 = RecognitionEvent(
            id="rec-1",
            patient_id=raghavan.id,
            familiar_person_id=fam1.id,
            detected_name="Anu Menon",
            relation="Daughter",
            confidence_score=98.4,
            camera_location="Living Room Smart Cam",
            status="recognized",
            detected_at=now.replace(hour=10, minute=42, second=0),
            source="python_cv_service"
        )
        db.add(rec1)

        print("Seeding AI Recommendations, Insights & Preferences...")
        pref = PatientPreference(
            id="pref-1",
            patient_id=raghavan.id,
            likes="gardening, Carnatic flute music, morning balcony walks, family photograph albums",
            dislikes="complex puzzles, sudden loud television sounds"
        )
        db.add(pref)

        ai_recs = [
            AIRecommendation(
                id="ai-rec-1",
                patient_id=raghavan.id,
                title="Short Balcony Gardening Activity",
                activity_type="Sensory Habilitation",
                duration_minutes=15,
                reason="Recent activity logs show that familiar outdoor plant care activities consistently lower afternoon restlessness.",
                recommended_time="16:30 PM (In 15 mins)",
                status="suggested",
                icon="Sprout",
                priority="normal",
                observed="Movement tracking and behavioral notes indicate mild pacing during late afternoon hours (3:30 - 4:30 PM).",
                why_it_matters="Structured sensory engagement during late afternoon anchors attention and mitigates early sundowning restlessness.",
                suggested_action="Invite Raghavan to water the balcony jasmine plants and check on flowering pots with caregiver supervision.",
                why_this_activity="Gardening has been Raghavan's lifelong hobby; tactile plant interaction triggers calming sensory memory.",
                safety_care_plan="Non-pharmacological sensory routine. Caregiver accompanies on balcony with slip-resistant footwear.",
                expected_outcome="Calm posture, reduced pacing, and relaxed conversation about favorite flowering varieties."
            ),
            AIRecommendation(
                id="ai-rec-2",
                patient_id=raghavan.id,
                title="Supervised Carnatic Music & Family Album Reminiscence",
                activity_type="Calm Sensory & Reminiscence",
                duration_minutes=15,
                reason="Recent records show shorter sleep and lower evening activity alongside increased evening confusion.",
                recommended_time="18:15 PM",
                status="suggested",
                icon="Music",
                priority="high",
                observed="Recent records show sleep duration decreased over several days (6.1h vs 7.3h baseline), evening movement dropped by 22%, and caregiver recorded increased evening confusion during sunset hours.",
                why_it_matters="Disrupted sleep and lower daytime activity are frequent precursors to evening disorientation ('sundowning') in mild-to-moderate Alzheimer's care.",
                suggested_action="Initiate a 15-minute supervised soothing session: play familiar Carnatic flute melodies followed by browsing the family photo album together in comfortable lighting.",
                why_this_activity="Patient preferences show strong emotional affinity for Carnatic music and family photographs; these calm sensory cues reduce anxiety and orient memory without cognitive strain.",
                safety_care_plan="Strictly non-pharmacological, supportive caregiver interaction. Does not alter doctor's prescription or clinical schedule.",
                expected_outcome="Caregiver can observe reduced restlessness, relaxed posture, improved eye contact, and a calmer transition into evening routines."
            ),
            AIRecommendation(
                id="ai-rec-3",
                patient_id=raghavan.id,
                title="Hydration Gentle Prompt",
                activity_type="Daily Care",
                duration_minutes=5,
                reason="Hydration tracking shows 5/7 glasses consumed. Offering warm water with lemon before 5 PM aligns with peak daily routines.",
                recommended_time="16:45 PM",
                status="suggested",
                icon="Droplets",
                priority="normal",
                observed="Hydration logs show 5 of 7 target glasses logged today, with a 3-hour interval since last intake.",
                why_it_matters="Even mild dehydration exacerbates cognitive fatigue and confusion in elderly individuals.",
                suggested_action="Offer a warm cup of water with a slice of lemon or tender coconut water in a familiar cup.",
                why_this_activity="Raghavan prefers warm beverages served in his accustomed steel tumbler.",
                safety_care_plan="Routine daily wellness support. No swallowing difficulties noted in care plan.",
                expected_outcome="Maintains optimal daytime hydration without evening fluid overload."
            )
        ]
        db.add_all(ai_recs)


        ai_insights = [
            AIInsight(
                id="ins-1",
                patient_id=raghavan.id,
                category="sleep",
                title="Stable Night Sleep Pattern",
                description="Raghavan averaged 7h 20m of continuous sleep this week with minimal nocturnal wandering.",
                timestamp_label="Today",
                metric="7.3 hrs avg"
            ),
            AIInsight(
                id="ins-2",
                patient_id=raghavan.id,
                category="medication",
                title="High Morning Adherence",
                description="Morning medication adherence reached 98% over the past 30 days.",
                timestamp_label="This Week",
                metric="98% adherence"
            )
        ]
        db.add_all(ai_insights)

        print("Seeding Reports & Notifications...")
        reports = [
            CareReport(
                id="rep-1",
                patient_id=raghavan.id,
                title="Weekly Comprehensive Care Report",
                report_type="weekly",
                generated_date_label="22 Sep 2026",
                period="15 Sep - 21 Sep 2026",
                summary="Overall care adherence remained strong at 87%. Patient displayed stable mood and consistent sleep routines.",
                adherence_rate=87,
                medication_rate=91,
                cognitive_rate=86,
                file_size="1.4 MB"
            ),
            CareReport(
                id="rep-2",
                patient_id=raghavan.id,
                title="Doctor Consultation Briefing",
                report_type="doctor",
                generated_date_label="20 Sep 2026",
                period="Last 30 Days",
                summary="Clinical summary prepared for Dr. Arun Nair including medication adherence, cognitive scores, and incident logs.",
                adherence_rate=89,
                medication_rate=94,
                cognitive_rate=83,
                file_size="2.1 MB"
            ),
            CareReport(
                id="rep-3",
                patient_id=raghavan.id,
                title="Medication Adherence Log",
                report_type="medication",
                generated_date_label="15 Sep 2026",
                period="August 2026",
                summary="Full monthly audit log of prescribed dosages, timestamps, and caregiver acknowledgments.",
                adherence_rate=91,
                medication_rate=91,
                cognitive_rate=85,
                file_size="890 KB"
            )
        ]
        db.add_all(reports)

        notifs = [
            Notification(
                id="notif-1",
                user_id=anu.id,
                patient_id=raghavan.id,
                notification_type="medication",
                title="Medication Reminder Pending",
                message="Evening Donepezil 5 mg is scheduled for 9:00 PM.",
                severity="warning",
                read=False,
                timestamp_label="10 min ago"
            ),
            Notification(
                id="notif-2",
                user_id=anu.id,
                patient_id=raghavan.id,
                notification_type="system",
                title="Pendant Synced Successfully",
                message="Battery level at 78%. GPS lock active.",
                severity="info",
                read=True,
                timestamp_label="1 hour ago"
            )
        ]
        db.add_all(notifs)

        db.commit()
        print("Database successfully seeded with demo dataset!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
