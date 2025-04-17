import re
from typing import Optional

from pydantic import BaseModel, field_validator, EmailStr

from app.service.models.address_models import AddressOut


class GuestIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address_id: int

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

    model_config = {"from_attributes": True}


class GuestUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    address_id: int

    @field_validator("phone_number")
    def validate_phone(cls, v):
        v = v.strip()
        if v and not re.match(r"^\+?[0-9\s\-()]{7,20}$", v):
            raise ValueError("Phone number must be in international format, e.g. +41 79 123 45 67")
        return v


model_config = {'from_attributes': True}
