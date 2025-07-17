"""FastAPI dependencies."""

from typing import Generator
from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.models import User, ApiToken
from app.crud.users import get_user_by_id
from app.utils.security import verify_token, verify_api_token

security = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    return current_user


def validate_api_token(token: str, db: Session) -> ApiToken:
    """Validate API token and return the token object."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required"
        )

    # Query all active tokens and verify against hash
    active_tokens = db.query(ApiToken).filter(
        ApiToken.is_active.is_(True)
    ).all()

    for api_token in active_tokens:
        if verify_api_token(token, api_token.token_hash): # type: ignore
            # Check if token is expired
            if api_token.expires_at and api_token.expires_at < datetime.now(timezone.utc): # type: ignore
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="API token has expired"
                )

            # Update last_used_at
            api_token.last_used_at = datetime.now(timezone.utc) # type: ignore
            db.commit()

            return api_token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token"
    )
