from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.database.database import SessionLocal
from app.entities.user import User
from app.services.models.user_models import RegisterUser, AuthResponse, UserModel, LoginUser
from app.util.enums import Role
from app.util.jwt import create_access_token
from app.util.password import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(data: LoginUser):
    db = SessionLocal()
    user = db.query(User).filter_by(email=data.email).first()

    if not user:
        print("❌ Kein Benutzer mit dieser E-Mail gefunden:", data.email)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print("✅ Benutzer gefunden:", user.email)

    if not verify_password(data.password, user.hashed_password):
        print("❌ Passwort stimmt nicht")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    print("✅ Passwort korrekt")
    token = create_access_token(user.id, user.role)

    return AuthResponse(
        token=token,
        user=UserModel(**user.__dict__)
    )


@router.post("/register", response_model=AuthResponse)
def register(data: RegisterUser):
    db = SessionLocal()

    existing_user = db.query(User).filter_by(email=data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email bereits registriert")

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        role=Role.GUEST,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user.id, new_user.role)

    return AuthResponse(
        token=token,
        user=UserModel(**new_user.__dict__)
    )
