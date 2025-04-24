from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel

from app.util.enums import Gender


class UserModel(BaseModel):
    id: Optional[int]
    email: str
    hashed_password: str
    role: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    gender: Optional[Gender] = None
    loyalty_points: int = 0
    address_id: Optional[int] = None

    model_config = {'from_attributes': True}


class LoginUser(BaseModel):
    email: str
    password: str

    model_config = {'from_attributes': True}


class RegisterUser(LoginUser):
    first_name: str
    last_name: str

    model_config = {'from_attributes': True}


class AuthResponse(BaseModel):
    token: str
    user: UserModel
