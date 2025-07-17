from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, exceptions
from app.config import settings


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify a JWT token and return its payload."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except exceptions.JWTError:
        return None


def hash_api_token(token: str) -> str:
    """Hash an API token using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(token.encode('utf-8'), salt).decode('utf-8')


def verify_api_token(token: str, hashed_token: str) -> bool:
    """Verify an API token against its hash."""
    return bcrypt.checkpw(token.encode('utf-8'), hashed_token.encode('utf-8'))
