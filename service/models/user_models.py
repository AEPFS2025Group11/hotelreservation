from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    email: str
    hashed_password: str
    role: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


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
