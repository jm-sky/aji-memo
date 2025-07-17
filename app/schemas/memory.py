from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.schemas.base import ApiResponse


class MemoryCreateRequest(BaseModel):
    uid: str = Field(..., description="User or session identifier")
    namespace: str = Field(..., description="Memory namespace")
    text: str = Field(..., description="Memory text content")
    tags: List[str] = Field(default_factory=list, description="List of tags")
    created_by: Optional[str] = Field(None, description="Who created this memory")


class MemoryQueryRequest(BaseModel):
    uid: str = Field(..., description="User or session identifier")
    namespace: Optional[str] = Field(None, description="Memory namespace filter")
    tags: List[str] = Field(default_factory=list, description="List of tags to filter by")
    query: Optional[str] = Field(None, description="Full-text search query")
    limit: int = Field(10, description="Maximum number of results", ge=1, le=100)
    offset: int = Field(0, description="Offset for pagination", ge=0)


class MemoryData(BaseModel):
    id: int
    uid: str
    namespace: str
    text: str
    tags: List[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MemoryResponse(ApiResponse):
    data: MemoryData


class MemoryListResponse(ApiResponse):
    data: List[MemoryData]
