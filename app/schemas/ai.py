from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.schemas.base import ApiResponse


class AIRegistrationData(BaseModel):
    uid: str
    namespace: str
    email: str
    token: str
    message: str


class AIRegistrationResponse(ApiResponse):
    data: AIRegistrationData


class AITokenData(BaseModel):
    token_name: str
    user_id: int
    permissions: Dict[str, Any]
    rate_limit_per_hour: int
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True


class AITokenResponse(ApiResponse):
    data: AITokenData
