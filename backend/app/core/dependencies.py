from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, CaregiverPatient, CareTeamMember
from app.models.patient import Patient

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        # For development / hackathon convenience if no token header provided:
        # Default to primary caregiver Anu Menon
        default_user = db.query(User).filter(User.id == "user-anu").first()
        if default_user:
            return default_user
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
    return user


def verify_patient_access(
    patient_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Patient:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    if current_user.role == "admin":
        return patient

    # Check Caregiver-Patient link
    link = db.query(CaregiverPatient).filter(
        CaregiverPatient.caregiver_id == current_user.id,
        CaregiverPatient.patient_id == patient_id
    ).first()

    # Check Care Team Member link
    team_link = db.query(CareTeamMember).filter(
        CareTeamMember.user_id == current_user.id,
        CareTeamMember.patient_id == patient_id
    ).first()

    if not link and not team_link:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have authorization to access this patient's records."
        )

    return patient
