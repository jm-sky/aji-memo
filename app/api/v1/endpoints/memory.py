from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.memory import (
    MemoryResponse,
    MemoryListResponse,
    MemoryCreateRequest,
    MemoryQueryRequest,
    MemoryData,
)
from app.deps import get_db, get_current_active_user
from app.crud.memory import create_memory, query_memories
from app.db.models import User

router = APIRouter()


@router.post("/save", response_model=MemoryResponse)
async def save_memory_post(
    request: MemoryCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Save memory via POST request (for web interface)
    """

    # Set created_by to current user
    request.created_by = f"user:{current_user.id}"

    try:
        memory = create_memory(db, request, user_id=current_user.id) # type: ignore

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


@router.post("/query", response_model=MemoryListResponse)
async def query_memory_post(
    request: MemoryQueryRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Query memories via POST request (for web interface)
    """

    try:
        memories = query_memories(db, request, user_id=current_user.id) # type: ignore

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
