from datetime import datetime, timedelta

from jose import jwt, JWTError

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"


def create_access_token(user_id: int, role: str, expires_delta=timedelta(hours=1)):
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now() + expires_delta
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
