import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, field_validator, EmailStr

from app.service.models.address_models import AddressOut
from app.util.enums import Gender


class GuestIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address_id: int
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    gender: Optional[Gender] = None

    model_config = {'from_attributes': True}

    @field_validator("phone_number")
    def validate_phone(cls, v):
        v = v.strip()
        if v and not re.match(r"^\+?[0-9\s\-()]{7,20}$", v):
            raise ValueError("Phone number must be in international format, e.g. +41 79 123 45 67")
        return v


class GuestOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str]
    address: AddressOut
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    gender: Optional[Gender] = None
    loyalty_points: Optional[int] = 0

    model_config = {"from_attributes": True}


class GuestUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address_id: int
    birth_date: Optional[date] = None
    nationality: Optional[str] = None
    gender: Optional[Gender] = None

    @field_validator("phone_number")
    def validate_phone(cls, v):
        v = v.strip()
        if v and not re.match(r"^\+?[0-9\s\-()]{7,20}$", v):
            raise ValueError("Phone number must be in international format, e.g. +41 79 123 45 67")
        return v


model_config = {'from_attributes': True}
