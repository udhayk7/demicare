"""
End-to-End Acceptance Test demonstrating the exact sequence from Section 77:
Caregiver Login
  ↓
Patient Dashboard
  ↓
View Raghavan
  ↓
Medication
  ↓
Create / update schedule
  ↓
Simulate medication reminder
  ↓
Medication acknowledged
  ↓
Monitor
  ↓
Mock location update
  ↓
Mock movement data
  ↓
Mock sleep data
  ↓
Camera recognition (Anu - Daughter detected)
  ↓
Timeline updated
  ↓
Notification generated
  ↓
AI analyzes patient data
  ↓
Care recommendation
  ↓
Caregiver completes activity
  ↓
Feedback recorded
  ↓
Insights updated
  ↓
Generate Doctor Report
  ↓
Report generated successfully
"""

import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000/api/v1"


def test_complete_e2e_hackathon_flow():
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    # 1. Caregiver Login
    res_login = client.post("/auth/login", json={
        "email": "anu.menon@carecompanion.in",
        "password": "password123"
    })
    assert res_login.status_code == 200, f"Login failed: {res_login.text}"
    token_data = res_login.json()
    token = token_data["access_token"]
    patient_id = token_data["patient_id"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Patient Dashboard
    res_dash = client.get(f"/patients/{patient_id}/dashboard", headers=headers)
    assert res_dash.status_code == 200
    dash = res_dash.json()
    assert dash["patient"]["name"] == "Raghavan Menon"
    assert dash["patient"]["age"] == 72
    assert dash["patient"]["status"] in ["stable", "attention", "critical"]

    # 3. View Raghavan Profile
    res_pat = client.get(f"/patients/{patient_id}", headers=headers)
    assert res_pat.status_code == 200
    assert res_pat.json()["primaryCaregiver"] == "Anu Menon"

    # 4. Medication List
    res_meds = client.get(f"/patients/{patient_id}/medications", headers=headers)
    assert res_meds.status_code == 200
    meds = res_meds.json()
    assert len(meds) >= 3

    # 5. Create / Update Schedule
    res_new_med = client.post(f"/patients/{patient_id}/medications", json={
        "name": "CoQ10 Heart Support",
        "dosage": "100 mg",
        "scheduled_time": "14:00",
        "instructions": "Take after lunch with water",
        "icon": "HeartPulse"
    }, headers=headers)
    assert res_new_med.status_code == 200
    new_med_id = res_new_med.json()["id"]

    # 6. Simulate Medication Reminder
    res_sim_rem = client.post(f"/simulation/pendant/reminder?patient_id={patient_id}", headers=headers)
    assert res_sim_rem.status_code == 200
    assert res_sim_rem.json()["success"] is True

    # 7. Medication Acknowledged
    res_ack = client.post(
        f"/patients/{patient_id}/medications/{new_med_id}/acknowledge",
        json={"status": "taken"},
        headers=headers
    )
    assert res_ack.status_code == 200
    assert res_ack.json()["status"] == "taken"

    # 8. Monitor Overview (Location, Movement, Sleep)
    res_mon = client.get(f"/patients/{patient_id}/monitoring/summary", headers=headers)
    assert res_mon.status_code == 200
    mon = res_mon.json()
    assert mon["location"]["status"] in ["at_home", "safe_zone_exit"]
    assert mon["movement"]["dailyKm"] > 0
    assert mon["sleep"]["durationHours"] > 0
    assert mon["pendant"]["batteryLevel"] > 0

    # 9. Camera Recognition: Anu - Daughter detected
    res_cam = client.post("/camera/recognitions", json={
        "patient_id": patient_id,
        "detected_name": "Anu Menon",
        "relation": "Daughter",
        "confidence": 99.4,
        "camera_location": "Living Room Cam"
    }, headers=headers)
    assert res_cam.status_code == 200
    rec_event = res_cam.json()
    assert rec_event["personName"] == "Anu Menon"
    assert rec_event["status"] == "recognized"

    # 10. Timeline Updated
    res_timeline = client.get(f"/patients/{patient_id}/timeline?limit=15", headers=headers)
    assert res_timeline.status_code == 200
    timeline = res_timeline.json()
    assert any("Anu Menon" in e["description"] for e in timeline)

    # 11. Notification Generated
    res_notifs = client.get(f"/patients/{patient_id}/notifications", headers=headers)
    assert res_notifs.status_code == 200
    notifs = res_notifs.json()
    assert len(notifs) >= 1

    # 12. AI Analyzes Patient Data & Care Recommendation
    res_recs = client.get(f"/patients/{patient_id}/ai/recommendations", headers=headers)
    assert res_recs.status_code == 200
    recs = res_recs.json()
    assert len(recs) >= 1
    top_rec = recs[0]

    # 13. Caregiver Completes Activity & Feedback Recorded
    res_comp = client.post(
        f"/patients/{patient_id}/ai/recommendations/{top_rec['id']}/complete",
        headers=headers
    )
    assert res_comp.status_code == 200
    assert res_comp.json()["status"] == "completed"

    res_fb = client.post(
        f"/patients/{patient_id}/ai/recommendations/{top_rec['id']}/feedback",
        json={"feedback": "enjoyed", "notes": "Raghavan was calm and attentive during the activity."},
        headers=headers
    )
    assert res_fb.status_code == 200

    # 14. Insights Updated
    res_insights = client.get(f"/patients/{patient_id}/ai/insights", headers=headers)
    assert res_insights.status_code == 200
    insights = res_insights.json()
    assert len(insights) >= 2

    # 15. Generate Doctor Report & Verify PDF Generation
    res_rep = client.post(f"/patients/{patient_id}/reports/generate", json={
        "report_type": "doctor",
        "period": "Last 30 Days"
    }, headers=headers)
    assert res_rep.status_code == 200
    new_report = res_rep.json()
    assert new_report["type"] == "doctor"
    assert new_report["adherenceRate"] > 0

    # Download real PDF
    res_pdf = client.get(f"/patients/{patient_id}/reports/{new_report['id']}/download", headers=headers)
    assert res_pdf.status_code == 200
    assert res_pdf.headers["content-type"] == "application/pdf"
    assert len(res_pdf.content) > 1000  # Valid binary PDF content

    print("End-to-End Acceptance Test PASSED successfully!")
