import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_auth_login_success():
    response = client.post("/api/v1/auth/login", json={
        "email": "anu.menon@carecompanion.in",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "caregiver"
    assert data["patient_id"] == "pat-101"


def test_auth_login_invalid_password():
    response = client.post("/api/v1/auth/login", json={
        "email": "anu.menon@carecompanion.in",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_dashboard_endpoint():
    response = client.get("/api/v1/patients/pat-101/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["patient"]["name"] == "Raghavan Menon"
    assert len(data["medications"]) > 0
    assert len(data["routines"]) > 0
    assert data["location"]["safeZoneRadiusMeters"] == 150


def test_medication_acknowledge():
    response = client.post(
        "/api/v1/patients/pat-101/medications/med-4/acknowledge",
        json={"status": "taken"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "taken"


def test_care_routines_and_toggle():
    res_routines = client.get("/api/v1/patients/pat-101/care/routines")
    assert res_routines.status_code == 200

    res_hab = client.get("/api/v1/patients/pat-101/care/habilitation")
    assert res_hab.status_code == 200
    hab_id = res_hab.json()[0]["id"]

    res_toggle = client.post(f"/api/v1/patients/pat-101/care/habilitation/{hab_id}/toggle")
    assert res_toggle.status_code == 200


def test_monitoring_endpoints():
    res_loc = client.get("/api/v1/patients/pat-101/monitoring/location")
    assert res_loc.status_code == 200

    res_mov = client.get("/api/v1/patients/pat-101/monitoring/movement")
    assert res_mov.status_code == 200
    assert res_mov.json()["dailyKm"] > 0

    res_slp = client.get("/api/v1/patients/pat-101/monitoring/sleep")
    assert res_slp.status_code == 200
    assert res_slp.json()["durationHours"] > 0


def test_safety_sos_trigger():
    response = client.post("/api/v1/patients/pat-101/monitoring/safety/sos")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "sos_button"
    assert data["severity"] == "critical"


def test_camera_recognition_ingest():
    response = client.post("/api/v1/camera/recognitions", json={
        "patient_id": "pat-101",
        "detected_name": "Anu Menon",
        "relation": "Daughter",
        "confidence": 98.7,
        "camera_location": "Front Door Camera"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["personName"] == "Anu Menon"
    assert data["status"] == "recognized"


def test_ai_recommendations_and_complete():
    res = client.get("/api/v1/patients/pat-101/ai/recommendations")
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) > 0

    rec_id = recs[0]["id"]
    res_complete = client.post(f"/api/v1/patients/pat-101/ai/recommendations/{rec_id}/complete")
    assert res_complete.status_code == 200
    assert res_complete.json()["status"] == "completed"


def test_timeline_unified_aggregation():
    res = client.get("/api/v1/patients/pat-101/timeline?limit=10")
    assert res.status_code == 200
    events = res.json()
    assert len(events) > 0
    categories = {e["category"] for e in events}
    assert len(categories) >= 1


def test_report_generation_and_download():
    res_gen = client.post("/api/v1/patients/pat-101/reports/generate", json={
        "report_type": "doctor",
        "period": "Last 30 Days"
    })
    assert res_gen.status_code == 200
    report_id = res_gen.json()["id"]

    res_pdf = client.get(f"/api/v1/patients/pat-101/reports/{report_id}/download")
    assert res_pdf.status_code == 200
    assert res_pdf.headers["content-type"] == "application/pdf"
    assert len(res_pdf.content) > 1000


def test_care_hydration_logging():
    res = client.post(
        "/api/v1/patients/pat-101/care/hydration",
        json={"amount": 1, "unit": "glass"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["amount"] == 1
    assert data["todayTotal"] >= 1


def test_care_nutrition_logging():
    res = client.post(
        "/api/v1/patients/pat-101/care/nutrition",
        json={
            "mealType": "lunch",
            "intakeLevel": "good",
            "notes": "Steamed idlis and mild vegetable sambar"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mealType"] == "lunch"
    assert data["intakeLevel"] == "good"


def test_care_observation_logging():
    res = client.post(
        "/api/v1/patients/pat-101/care/observations",
        json={
            "type": "confusion",
            "intensity": "moderate",
            "note": "Mild evening confusion observed near sundown"
        }
    )
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "confusion"
    assert data["intensity"] == "moderate"


def test_simulation_low_battery():
    res = client.post("/api/v1/simulation/pendant/low-battery?patient_id=pat-101")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True

    # Verify pendant battery is now 14%
    res_pendant = client.get("/api/v1/patients/pat-101/monitoring/pendant")
    assert res_pendant.status_code == 200
    assert res_pendant.json()["batteryLevel"] == 14


def test_simulation_geofence_and_return():
    # Geofence breach
    res_breach = client.post("/api/v1/simulation/pendant/geofence?patient_id=pat-101")
    assert res_breach.status_code == 200
    assert res_breach.json()["success"] is True

    # Return home
    res_return = client.post("/api/v1/simulation/pendant/return-home?patient_id=pat-101")
    assert res_return.status_code == 200
    assert res_return.json()["success"] is True


def test_simulation_safety_resolve():
    # Trigger SOS first
    client.post("/api/v1/monitoring/safety/sos")

    # Resolve safety alerts
    res_res = client.post("/api/v1/simulation/safety/resolve?patient_id=pat-101")
    assert res_res.status_code == 200
    assert res_res.json()["success"] is True

    # Verify patient status is stable
    res_dash = client.get("/api/v1/patients/pat-101/dashboard")
    assert res_dash.status_code == 200
    assert res_dash.json()["patient"]["status"] == "stable"


def test_ai_recommendation_structured_feedback():
    res = client.get("/api/v1/patients/pat-101/ai/recommendations")
    assert res.status_code == 200
    recs = res.json()
    assert len(recs) > 0

    top_rec = recs[0]
    # Verify Section 11 structured clinical fields exist (camelCase in JSON)
    assert "observed" in top_rec
    assert "whyItMatters" in top_rec
    assert "suggestedAction" in top_rec

    # Complete with feedback
    res_comp = client.post(
        f"/api/v1/patients/pat-101/ai/recommendations/{top_rec['id']}/complete",
        json={"feedback": "enjoyed", "notes": "Patient enjoyed listening to Carnatic flute"}
    )
    assert res_comp.status_code == 200
    data = res_comp.json()
    assert data["status"] == "completed"
    assert data["caregiverFeedback"] == "enjoyed"


def test_simulation_reset_to_baseline():
    res = client.post("/api/v1/simulation/reset?patient_id=pat-101")
    assert res.status_code == 200
    assert res.json()["success"] is True

    # Verify baseline state restored
    dash = client.get("/api/v1/patients/pat-101/dashboard").json()
    assert dash["patient"]["status"] == "stable"
    assert dash["pendant"]["batteryLevel"] == 78
    assert dash["location"]["status"] == "at_home"


