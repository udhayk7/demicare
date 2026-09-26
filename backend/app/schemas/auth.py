from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    name: str
    role: str
    patient_id: Optional[str] = "pat-101"


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    profile_photo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "caregiver"
    phone: Optional[str] = None
