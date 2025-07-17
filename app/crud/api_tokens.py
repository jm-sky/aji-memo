from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.db.models import ApiToken
from app.utils.security import hash_api_token


def create_api_token(
    db: Session,
    user_id: int,
    token_name: str,
    token: str,
    permissions: Optional[dict] = None,
    rate_limit_per_hour: int = 5,
    expires_at: Optional[datetime] = None
) -> ApiToken:
    """Create a new API token."""
    if permissions is None:
        permissions = {}

    token_hash = hash_api_token(token)

    api_token = ApiToken(
        user_id=user_id,
        token_name=token_name,
        token_hash=token_hash,
        permissions=permissions,
        rate_limit_per_hour=rate_limit_per_hour,
        expires_at=expires_at,
        is_active=True
    )

    db.add(api_token)
    db.commit()
    db.refresh(api_token)

    return api_token


def get_token_by_hash(db: Session, token_hash: str) -> Optional[ApiToken]:
    """Get API token by hash."""
    return db.query(ApiToken).filter(
        ApiToken.token_hash == token_hash,
        ApiToken.is_active.is_(True)
    ).first()


def get_user_tokens(db: Session, user_id: int) -> list[ApiToken]:
    """Get all active tokens for a user."""
    return db.query(ApiToken).filter(
        ApiToken.user_id == user_id,
        ApiToken.is_active.is_(True)
    ).all()


def deactivate_token(db: Session, token_id: int, user_id: int) -> bool:
    """Deactivate an API token."""
    token = db.query(ApiToken).filter(
        ApiToken.id == token_id,
        ApiToken.user_id == user_id
    ).first()

    if token:
        token.is_active = False  # type: ignore
        db.commit()
        return True

    return False


def validate_token_permissions(token: ApiToken, required_permission: str) -> bool:
    """Validate if token has required permissions."""
    if not token.permissions:  # type: ignore
        return False

    # Check if token has the required permission
    # Format: {"memory": ["read", "write"], "admin": ["read"]}
    parts = required_permission.split(":")
    if len(parts) != 2:
        return False

    resource, action = parts

    if resource not in token.permissions:  # type: ignore
        return False

    return action in token.permissions[resource]  # type: ignore
