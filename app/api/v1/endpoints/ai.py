from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import secrets
from datetime import datetime, timedelta, timezone

from app.schemas.ai import (
    AIRegistrationResponse,
    AIRegistrationData,
    AITokenResponse,
    AITokenData,
)
from app.deps import get_db
from app.crud.users import get_user_by_email, create_user
from app.utils.security import hash_api_token
from app.db.models import ApiToken

router = APIRouter()


@router.get("/register", response_model=AIRegistrationResponse)
async def register_ai_user(
    namespace: str = Query(..., description="Namespace for the AI user"),
    uid: str = Query(..., description="User identifier"),
    token: Optional[str] = Query(None, description="Optional API token (will be generated if not provided)"),
    db: Session = Depends(get_db),
):
    """
    Register AI user via GET request

    - **namespace**: Namespace for the AI user
    - **uid**: User identifier
    - **token**: Optional API token (will be generated if not provided)
    """

    # Create email from namespace and uid
    email = f"{uid}@{namespace}.ai"

    # Check if user already exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        # User exists, check if they have an active token
        active_token = db.query(ApiToken).filter(
            ApiToken.user_id == existing_user.id,
            ApiToken.is_active.is_(True)
        ).first()

        if active_token:
            return AIRegistrationResponse(
                data=AIRegistrationData(
                    uid=uid,
                    namespace=namespace,
                    email=email,
                    token="***existing***",  # Don't expose existing token
                    message="User already registered with active token"
                ),
                success=True
            )

    # Generate token if not provided
    if not token:
        token = secrets.token_urlsafe(32)

    # Create user if doesn't exist
    if not existing_user:
        # Generate a random password for AI users
        temp_password = secrets.token_urlsafe(16)
        user = create_user(
            db,
            email=email,
            password=temp_password,
            name=f"AI User {uid}",
            plan="ai"
        )
    else:
        user = existing_user

    # Create API token
    try:
        token_hash = hash_api_token(token)
        expires_at = datetime.now(timezone.utc) + timedelta(days=365)  # 1 year expiry for AI tokens

        api_token = ApiToken(
            user_id=user.id,
            token_name=f"AI Token for {uid}",
            token_hash=token_hash,
            permissions={"memory": ["read", "write"]},
            rate_limit_per_hour=1000,  # Higher limit for AI
            expires_at=expires_at,
            is_active=True
        )

        db.add(api_token)
        db.commit()

        return AIRegistrationResponse(
            data=AIRegistrationData(
                uid=uid,
                namespace=namespace,
                email=email,
                token=token,
                message="Registration successful"
            ),
            success=True
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create API token: {str(e)}"
        )


@router.get("/token/validate", response_model=AITokenResponse)
async def validate_ai_token(
    token: str = Query(..., description="API token to validate"),
    db: Session = Depends(get_db),
):
    """
    Validate AI token via GET request

    - **token**: API token to validate
    """

    try:
        from app.deps import validate_api_token
        api_token = validate_api_token(token, db)

        return AITokenResponse(
            data=AITokenData(
                token_name=api_token.token_name, # type: ignore
                user_id=api_token.user_id, # type: ignore
                permissions=api_token.permissions, # type: ignore
                rate_limit_per_hour=api_token.rate_limit_per_hour, # type: ignore
                expires_at=api_token.expires_at, # type: ignore
                last_used_at=api_token.last_used_at, # type: ignore
                is_active=api_token.is_active # type: ignore
            ),
            success=True
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token validation failed: {str(e)}"
        )
