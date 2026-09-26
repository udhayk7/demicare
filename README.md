# CareCompanion / DementiaCare Full-Stack Platform

A mobile-first healthcare coordination and monitoring platform engineered specifically for caregivers supporting persons living with dementia.

The platform provides an end-to-end caregiver-first ecosystem: daily medication tracking with adherence metrics, personalized non-pharmacological care suggestions, safe-zone geofencing, pendant telemetry, familiar-person camera recognition, chronological timeline aggregation, and automated physician report generation with verifiable PDF downloads.

---

## Architecture Overview

```
Frontend (React 19 + TypeScript + Vite)
      │
      ├── [REST API Client with JWT Bearer Authentication]
      │
      ▼
Backend (Python 3.9+ / FastAPI + SQLAlchemy 2.0 + Pydantic v2)
      │
      ├── Alembic Database Migrations
      ├── Authentication & Multi-Tenant Caregiver Authorization
      ├── Care Domain Services: Dashboard, Care, Medication, Monitoring, AI, Timeline, Reports
      ├── Hardware Integration Gateway (Simulated Pendant, Geofence, SOS, Battery)
      ├── Camera Recognition Ingestion Gateway (Python CV Ready)
      │
      ▼
Database (PostgreSQL Relational Schema)
```

### Components
* **Frontend**: Mobile-first React 19 application with TypeScript, Tailwind CSS, Lucide Icons, and accessible touch targets.
* **Backend**: FastAPI asynchronous Python service implementing RESTful endpoints with strict Pydantic schemas and SQLAlchemy ORM.
* **Database**: PostgreSQL 16 relational database with normalized foreign keys, cascade safety, and Alembic version-controlled migrations.
* **AI Care Companion**: Context-aware care pattern assistant synthesizing non-pharmacological caregiver interventions with an active feedback loop.
* **Simulation Layer**: Realistic mock hardware layer representing wearable IoT pendant telemetry and computer vision camera feeds.

---

## Core Features

1. **Daily Medication Coordination**: Timed medication reminders, adherence scoring (91%), and click-to-acknowledge workflows.
2. **Comprehensive Care Routines**: Habilitation exercises, cognitive memory games, hydration tracking, and meal intake logging.
3. **Continuous Monitoring**: GPS safe zone (150m perimeter), wearable pendant battery/status telemetry, sleep duration, and daily movement.
4. **Safety & Geofencing**: Real-time geofence breach detection, pendant SOS emergency button, and one-click alert resolution.
5. **Familiar-Person Recognition**: Simulated door camera recognition distinguishing family members (Anu Menon) from unknown visitors.
6. **Unified Patient Timeline**: Single source of truth recording medications, routines, safety events, caregiver notes, and AI interventions.
7. **Clinical Report Generation**: Instant Doctor and Weekly Care summaries with cryptographic adherence stats and authenticated PDF export.

---

## AI Care Companion & Safety Boundaries

The **AI Care Companion** acts as a **Care Pattern & Non-Pharmacological Activity Assistant**. It analyzes multi-modal patient context—including sleep duration, evening movement, hydration levels, behavior observations, and patient preferences—to recommend evidence-based care actions.

### Clinical Response Structure (Section 11)
Every recommendation adheres to a rigorous clinical structure:
1. **OBSERVED**: Specific recorded evidence (e.g., shorter sleep + sundown restlessness).
2. **WHY IT MATTERS**: Plain-language clinical explanation based on dementia care literature.
3. **SUGGESTED ACTION**: Concrete non-pharmacological activity (e.g., supervised Carnatic music and family photograph reminiscence).
4. **WHY THIS ACTIVITY**: Grounded in the patient's recorded personal preferences and hobbies.
5. **SAFETY / CARE PLAN**: Explicit confirmation that it complies with the physician's care plan and supervision rules.
6. **EXPECTED OUTCOME**: Measurable behavioral cues for the caregiver to observe.
7. **CAREGIVER FEEDBACK**: Interactive outcome tracking (`Enjoyed it`, `Stayed neutral`, `Disliked it`, `Became tired`, `Needed assistance`, `Refused`) which updates future recommendations.

### Strict AI Safety Boundaries
* **NO Prescriptions**: AI never prescribes medications or adjusts dosages.
* **NO Diagnoses**: AI does not diagnose dementia, comorbidities, or other conditions.
* **NO Doctor Overrides**: AI recommendations are strictly supportive, non-pharmacological, and subordinate to the physician's care plan.
* **NO Fabrications**: All observations derive strictly from actual database records.
* **Clinical Disclaimer**: Prominently displayed across all AI interfaces and generated reports:
  > *"AI Care Companion provides supportive, non-pharmacological suggestions based on recorded care data. It is not a diagnostic tool and does not replace professional medical advice from the attending care team."*

---

## Demo Credentials & Seed Data

The database comes pre-seeded with the exact hackathon scenario:

| Role | Name | Email | Password |
| :--- | :--- | :--- | :--- |
| **Primary Caregiver** | Anu Menon | `anu.menon@carecompanion.in` | `password123` |
| **Secondary Caregiver** | Suresh Menon | `suresh.menon@carecompanion.in` | `password123` |
| **Attending Neurologist** | Dr. Arun Nair | `dr.arun@neurocare.in` | `doctorpass123` |

### Seeded Patient Profile: Raghavan Menon
* **Age**: 72 years old
* **Diagnosis**: Mild-to-Moderate Dementia (Stage 2 · Moderate)
* **Status**: Stable
* **Medication Adherence**: 91%
* **Habilitation Adherence**: 83%
* **Cognitive Tasks**: 86%
* **Safe Zone Center**: 42 Jasmine Gardens, Green Glen Layout, Bengaluru (150m radius)
* **Wearable Pendant**: Online (78% battery, GPS locked)
* **Preferences**: Enjoys Carnatic flute music, gardening, filter coffee, and family photo albums; easily frustrated by complex multi-step puzzles.

---

## Quickstart Setup & Run

### 1. Database Setup (PostgreSQL)
Ensure PostgreSQL is running locally on port `5432`:
```bash
createdb demicare
```

### 2. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Seed initial demonstration data
python -m app.db.seed

# Start FastAPI development server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive API documentation:
* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **OpenAPI Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### 3. Frontend Setup
From the repository root:
```bash
npm install
npm run dev
```
Open [http://127.0.0.1:5173](http://127.0.0.1:5173) in your browser.

---

## Testing on a Physical Mobile Device

Follow these steps to open and interact with the application on your physical mobile phone over the same local Wi-Fi network:

### Step 1 — Connect Both Devices
Ensure both your Mac (running backend, frontend & database) and physical mobile phone are connected to the **same Wi-Fi network**.

### Step 2 — Find Your Mac's LAN IP
Run the following command in terminal on macOS:
```bash
ipconfig getifaddr en0
```
*(If Wi-Fi uses a different interface, run `ifconfig | grep "inet " | grep -v 127.0.0.1`)*.  
Example output: `192.168.1.25` (or `192.0.0.2`).

### Step 3 — Configure Frontend (Optional / Automatic)
The frontend includes automatic mobile LAN hostname routing: when loaded from `http://<MAC_LAN_IP>:5173`, it automatically connects to `http://<MAC_LAN_IP>:8000/api/v1`.  
To explicitly set the API address in `.env`:
```bash
VITE_API_BASE_URL=http://<MAC_LAN_IP>:8000
```
*(Example: `VITE_API_BASE_URL=http://192.168.1.25:8000`)*.

### Step 4 — Start Backend on 0.0.0.0:8000
```bash
cd backend
PYTHONPATH=. venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5 — Start Frontend on 0.0.0.0:5173
```bash
npm run dev
```
*(Vite is pre-configured with `server.host: '0.0.0.0'` in `vite.config.ts`)*.

### Step 6 — Open on Physical Mobile Phone
In Safari / Chrome on your phone, navigate to:
```
http://<MAC_LAN_IP>:5173
```
*(Example: `http://192.168.1.25:5173`)*.

### Step 7 — Verify Backend Health from Phone
Test the API health endpoint directly in your phone browser:
```
http://<MAC_LAN_IP>:8000/api/v1/health
```
*(Expected response: `{"status":"ok"}`)*.

> [!NOTE]
> **macOS Firewall Notice**: If the page loads indefinitely or fails to connect from your phone, check **System Settings > Network > Firewall**. Ensure incoming connections are allowed for `Python` and `node`, or temporarily allow local connections during the hackathon demonstration.

> [!CAUTION]
> **Important Security & LAN Notice**:
> * LAN testing is designed exclusively for hackathon evaluation on a private Wi-Fi network, not public deployment.
> * PostgreSQL (`5432`) remains bound locally and is **never** exposed to the LAN.
> * Private LAN IP addresses should never be committed as permanent production environment variables.
> * Production environments should enforce HTTPS, domain-restricted CORS, and managed cloud infrastructure.

---

## Environment Variables

### Frontend (`.env` / `.env.example`)
```bash
# Local Development (Mac localhost):
VITE_API_BASE_URL=http://127.0.0.1:8000
# Alternatively: VITE_API_URL=http://127.0.0.1:8000/api/v1

# Physical Mobile LAN Testing (Same Wi-Fi Network):
# VITE_API_BASE_URL=http://<MAC_LAN_IP>:8000

# Hackathon Demo Mode (set to true for judge auto-login; false for production auth)
VITE_DEMO_MODE=true

# Demo credentials (only active when VITE_DEMO_MODE=true)
VITE_DEMO_CAREGIVER_EMAIL=anu.menon@carecompanion.in
VITE_DEMO_CAREGIVER_PASSWORD=password123
```

### Backend (`backend/.env` / `backend/.env.example`)
```bash
PROJECT_NAME="DementiaCare CareCompanion"
VERSION="1.0.0"
API_V1_STR="/api/v1"
DATABASE_URL=postgresql://udhaykrishna@localhost:5432/demicare
JWT_SECRET=supersecretjwtkey_demicare_hackathon_2026_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256
CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173","http://localhost:3000"]
AI_PROVIDER=mock
```

---

## Automated Test Suite

A comprehensive test suite of 21 tests verifies the full system:
```bash
cd backend
PYTHONPATH=. venv/bin/pytest tests/
```
Expected output:
```
============================== 21 passed in 2.00s ==============================
```

Tests verify:
- Caregiver authentication (login, invalid password, JWT claims)
- Patient multi-tenant authorization
- Dashboard consolidated aggregation
- Medication schedule & acknowledgement
- Habilitation, cognitive, hydration, and nutrition logging
- Behaviour observation creation
- Location, movement, and sleep telemetry
- Simulated pendant SOS button & low battery warning
- Safe zone geofence breach & return-home resolution
- Camera familiar-person recognition & unknown visitor alert
- AI recommendation generation, structured rationale, and caregiver feedback persistence
- Unified timeline chronological ordering
- Clinical report creation and authentic ReportLab PDF streaming
- Demo baseline reset

---

## Hardware Simulation & Computer Vision

> **Important Architectural Limitation & Clarification**:
> The physical IoT pendant and camera hardware are simulated for the hackathon demonstration via a dedicated Simulation Gateway:
> ```
> REAL HARDWARE INTEGRATION LAYER (Future BLE / MQTT / RTSP)
>                 │
>                 ▼
> SIMULATION IMPLEMENTATION FOR HACKATHON (REST Simulation Gateway)
> ```
> In a production deployment, this layer will be replaced with real IoT MQTT brokers and edge computer vision inference nodes (OpenCV/YOLOv8) without altering the frontend or database schemas.

### Simulation Triggers via UI Floating Bar
* **Pill Reminder**: Simulates pendant audio-chime for Donepezil 5mg.
* **Geofence Breach**: Simulates Raghavan stepping 175m away (outside the 150m boundary).
* **Return Home**: Restores GPS coordinates to 42 Jasmine Gardens and resolves alert.
* **SOS Alert**: Activates urgent caregiver alarm with critical status.
* **Low Battery**: Simulates pendant battery dropping to 14% with warning toast.
* **Camera: Familiar Face**: Ingests door camera recognition for daughter Anu Menon.
* **Camera: Unknown Person**: Ingests unidentified visitor alert.
* **Reset Demo**: Restores the complete database state to the pristine baseline.

---

## Final Judge Demonstration Flow (5–7 Minutes)

Follow this exact story to demonstrate the full healthcare journey:

1. **Caregiver Login & Dashboard**:
   - Open [http://127.0.0.1:5173](http://127.0.0.1:5173).
   - Show Raghavan Menon's live clinical dashboard (adherence scores, attention alerts, vitals).
2. **Medication Coordination**:
   - In "Needs Attention" or "Next Up", click the pending Donepezil 5mg dose.
   - Mark as **Taken**. Notice immediate adherence update (91% → 100%) and pending card resolution.
3. **Care Plan & Nutrition**:
   - Switch to the **Care** tab.
   - Click to complete a cognitive activity ("Memory Match").
   - Click "+ Log Glass" under Hydration (instantly updates progress).
   - Log a lunch meal.
4. **Continuous Monitoring & Safety Simulation**:
   - Switch to the **Monitor** tab. Show live GPS pin, 150m safe perimeter, and pendant telemetry.
   - Using the bottom demo bar, click **Geofence Exit**.
   - Notice immediate status change to *Exit Safe Zone*, warning banner, and pulse animation.
   - Click **Return Home** to safely resolve.
   - Click **SOS** to demonstrate emergency dispatch, then resolve it with one click.
5. **Familiar-Person Recognition**:
   - Click **Recognize Anu** in the simulation controls.
   - Show door camera banner confirming daughter's arrival with 98.7% confidence.
6. **AI Care Companion & Personalization Loop**:
   - Switch to the **AI Companion** tab.
   - Highlight the Section 11 structured response: *Observed*, *Why It Matters*, *Suggested Action*, *Safety / Care Plan*, and *Expected Outcome*.
   - Click **Start Supervised Activity**, then **Mark Completed**.
   - Select caregiver feedback: **Enjoyed it** with notes. Submit feedback.
   - Notice the personalization loop update in AI insights!
7. **Unified Timeline**:
   - Switch to the **Timeline** tab.
   - Point out that every action just taken (medication, hydration, geofence, SOS, camera, AI activity) is aggregated chronologically into the single source of truth.
8. **Doctor Report & PDF Export**:
   - Switch to the **Reports** tab.
   - Click **Generate Doctor Report**.
   - Click **Download PDF** — browser instantly downloads the authentic ReportLab clinical briefing document with full metrics and disclaimers.
9. **Demo Reset**:
   - Click **Reset Demo** on the floating control bar.
   - The application instantly resets back to baseline, ready for the next judge!
