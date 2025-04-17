from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.service.entity.user import User
from app.database.database import SessionLocal
from app.util.jwt import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter_by(email=data.email).first()
    if not user or user.hashed_password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id, user.role)
    return {"access_token": token, "token_type": "bearer"}
