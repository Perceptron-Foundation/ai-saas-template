from datetime import datetime, timedelta, timezone
from typing import Any

from core.config import settings

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")
ALGORITHM = "HS256"

# JWT Token for every request-> stored in browser and expires after certain time
def create_access_token(subject: str | Any, expires_delta: timedelta= None)->str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Password Hashing and verification
def verify_password(plain_password: str, hashed_password: str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str)->str:
    return pwd_context.hash(password)