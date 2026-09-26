from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    patients,
    medications,
    care,
    monitoring,
    camera,
    ai,
    timeline,
    reports,
    notifications,
    simulation
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(patients.router, prefix="/patients", tags=["Patients"])
api_router.include_router(medications.router, prefix="/patients", tags=["Medication"])
api_router.include_router(care.router, prefix="/patients", tags=["Care"])
api_router.include_router(monitoring.router, prefix="/patients", tags=["Monitoring"])
api_router.include_router(camera.router, tags=["Camera"])
api_router.include_router(ai.router, prefix="/patients", tags=["AI"])
api_router.include_router(timeline.router, prefix="/patients", tags=["Timeline"])
api_router.include_router(reports.router, prefix="/patients", tags=["Reports"])
api_router.include_router(notifications.router, prefix="/patients", tags=["Notifications"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])


@api_router.get("/health", tags=["Health"])
def api_v1_health():
    return {"status": "ok"}
