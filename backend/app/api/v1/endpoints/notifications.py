from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.session import get_db
from app.core.dependencies import verify_patient_access
from app.models.patient import Patient
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter()


@router.get("/{patient_id}/notifications", response_model=List[NotificationResponse])
def get_notifications(
    patient_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    notifs = db.query(Notification).filter(
        Notification.patient_id == patient_id
    ).order_by(desc(Notification.created_at)).all()

    return [
        NotificationResponse(
            id=n.id,
            title=n.title,
            message=n.message,
            timestamp=n.timestamp_label,
            read=n.read,
            type=n.notification_type
        )
        for n in notifs
    ]


@router.put("/{patient_id}/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    patient_id: str,
    notification_id: str,
    db: Session = Depends(get_db),
    patient: Patient = Depends(verify_patient_access)
):
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.patient_id == patient_id
    ).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.read = True
    db.commit()
    db.refresh(notif)

    return NotificationResponse(
        id=notif.id,
        title=notif.title,
        message=notif.message,
        timestamp=notif.timestamp_label,
        read=notif.read,
        type=notif.notification_type
    )
