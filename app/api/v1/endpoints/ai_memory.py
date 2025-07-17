from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.memory import (
    MemoryResponse,
    MemoryListResponse,
    MemoryCreateRequest,
    MemoryQueryRequest,
    MemoryData,
)
from app.deps import get_db, validate_api_token
from app.crud.memory import create_memory, query_memories

router = APIRouter()


@router.get("/save", response_model=MemoryResponse)
async def save_memory_ai(
    uid: str = Query(..., description="User or session identifier"),
    token: str = Query(..., description="API token"),
    text: str = Query(..., description="Memory text content"),
    namespace: Optional[str] = Query(None, description="Memory namespace"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    db: Session = Depends(get_db),
):
    """
    Save memory via GET request (AI/LLM integration)

    - **uid**: User or session identifier
    - **token**: API token for authentication
    - **text**: Memory text content
    - **namespace**: Optional namespace (defaults to uid)
    - **tags**: Optional comma-separated tags
    """

    # Validate API token
    api_token = validate_api_token(token, db)

    # Parse tags
    parsed_tags = []
    if tags:
        parsed_tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

    # Set namespace default
    if not namespace:
        namespace = uid

    # Create memory entry
    memory_data = MemoryCreateRequest(
        uid=uid,
        namespace=namespace,
        text=text,
        tags=parsed_tags,
        created_by=f"ai_token:{token[:8]}..."  # Truncated token for audit
    )

    try:
        memory = create_memory(db, memory_data, user_id=api_token.user_id) # type: ignore

        return MemoryResponse(
            data=MemoryData(
                id=memory.id, # type: ignore
                uid=memory.uid, # type: ignore
                namespace=memory.namespace, # type: ignore
                text=memory.text, # type: ignore
                tags=memory.tags, # type: ignore
                created_by=memory.created_by, # type: ignore
                created_at=memory.created_at, # type: ignore
                updated_at=memory.updated_at, # type: ignore
            ),
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save memory: {str(e)}"
        )


@router.get("/query", response_model=MemoryListResponse)
async def query_memory_ai(
    uid: str = Query(..., description="User or session identifier"),
    token: str = Query(..., description="API token"),
    namespace: Optional[str] = Query(None, description="Memory namespace"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    query: Optional[str] = Query(None, description="Full-text search query"),
    limit: int = Query(10, description="Maximum number of results", ge=1, le=100),
    offset: int = Query(0, description="Offset for pagination", ge=0),
    db: Session = Depends(get_db),
):
    """
    Query memories via GET request (AI/LLM integration)

    - **uid**: User or session identifier
    - **token**: API token for authentication
    - **namespace**: Optional namespace filter
    - **tags**: Optional comma-separated tags to filter by
    - **query**: Optional full-text search query
    - **limit**: Maximum number of results (1-100)
    - **offset**: Offset for pagination
    """

    # Validate API token
    api_token = validate_api_token(token, db)

    # Parse tags
    parsed_tags = []
    if tags:
        parsed_tags = [tag.strip() for tag in tags.split(",") if tag.strip()]

    # Set namespace default
    if not namespace:
        namespace = uid

    # Create query request
    query_request = MemoryQueryRequest(
        uid=uid,
        namespace=namespace,
        tags=parsed_tags,
        query=query,
        limit=limit,
        offset=offset
    )

    try:
        memories = query_memories(db, query_request, user_id=api_token.user_id) # type: ignore

        memory_data = [
            MemoryData(
                id=memory.id, # type: ignore
                uid=memory.uid, # type: ignore
                namespace=memory.namespace, # type: ignore
                text=memory.text, # type: ignore
                tags=memory.tags, # type: ignore
                created_by=memory.created_by, # type: ignore
                created_at=memory.created_at, # type: ignore
                updated_at=memory.updated_at, # type: ignore
            )
            for memory in memories
        ]

        return MemoryListResponse(
            data=memory_data,
            success=True
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query memories: {str(e)}"
        )
