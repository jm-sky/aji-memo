from sqlalchemy.orm import Session
from sqlalchemy import and_, func, text
from typing import List, Optional

from app.db.models import Memory
from app.schemas.memory import MemoryCreateRequest, MemoryQueryRequest


def create_memory(db: Session, memory_data: MemoryCreateRequest, user_id: Optional[int] = None) -> Memory:
    """
    Create a new memory entry
    """
    memory = Memory(
        user_id=user_id,
        uid=memory_data.uid,
        namespace=memory_data.namespace,
        text=memory_data.text,
        tags=memory_data.tags,
        created_by=memory_data.created_by,
    )

    db.add(memory)
    db.commit()

    # Update search vector for full-text search
    db.execute(
        text(
            "UPDATE memories SET search_vector = to_tsvector('english', text || ' ' || array_to_string(tags, ' ')) WHERE id = :id"
        ),
        {"id": memory.id}
    )
    db.commit()

    db.refresh(memory)
    return memory


def query_memories(
    db: Session,
    query_request: MemoryQueryRequest,
    user_id: Optional[int] = None
) -> List[Memory]:
    """
    Query memories based on filters
    """
    query = db.query(Memory)

    # Filter by uid and namespace
    filters = [Memory.uid == query_request.uid]

    if query_request.namespace:
        filters.append(Memory.namespace == query_request.namespace)

    # Filter by user if provided
    if user_id:
        filters.append(Memory.user_id == user_id)

    # Apply basic filters
    query = query.filter(and_(*filters))

    # Filter by tags if provided
    if query_request.tags:
        # Use PostgreSQL array overlap operator
        query = query.filter(Memory.tags.op('&&')(query_request.tags))

    # Full-text search if query provided
    if query_request.query:
        search_query = func.plainto_tsquery('english', query_request.query)
        query = query.filter(Memory.search_vector.op('@@')(search_query))

        # Order by relevance (ts_rank)
        query = query.order_by(
            func.ts_rank(Memory.search_vector, search_query).desc()
        )
    else:
        # Default order by creation date (newest first)
        query = query.order_by(Memory.created_at.desc())

    # Apply pagination
    query = query.offset(query_request.offset).limit(query_request.limit)

    return query.all()


def get_memory_by_id(db: Session, memory_id: int, user_id: Optional[int] = None) -> Optional[Memory]:
    """
    Get a specific memory by ID
    """
    query = db.query(Memory).filter(Memory.id == memory_id)

    if user_id:
        query = query.filter(Memory.user_id == user_id)

    return query.first()


def delete_memory(db: Session, memory_id: int, user_id: Optional[int] = None) -> bool:
    """
    Delete a memory entry
    """
    query = db.query(Memory).filter(Memory.id == memory_id)

    if user_id:
        query = query.filter(Memory.user_id == user_id)

    memory = query.first()
    if memory:
        db.delete(memory)
        db.commit()
        return True

    return False


def update_memory(
    db: Session,
    memory_id: int,
    update_data: dict,
    user_id: Optional[int] = None
) -> Optional[Memory]:
    """
    Update a memory entry
    """
    query = db.query(Memory).filter(Memory.id == memory_id)

    if user_id:
        query = query.filter(Memory.user_id == user_id)

    memory = query.first()
    if memory:
        for key, value in update_data.items():
            if hasattr(memory, key):
                setattr(memory, key, value)

        db.commit()

        # Update search vector if text or tags changed
        if 'text' in update_data or 'tags' in update_data:
            db.execute(
                text(
                    "UPDATE memories SET search_vector = to_tsvector('english', text || ' ' || array_to_string(tags, ' ')) WHERE id = :id"
                ),
                {"id": memory.id}
            )
            db.commit()

        db.refresh(memory)
        return memory

    return None
