from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.util.enums import Role
from app.util.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload["role"]


def admin_only(role: str = Depends(get_current_user_role)):
    if role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin privileges required")
