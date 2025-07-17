from fastapi import APIRouter
from app.api.v1.endpoints import auth, memory, ai, ai_memory

api_router = APIRouter()

# Human/Web interface routes
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])

# AI/LLM interface routes (GET-only for simplicity)
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(ai_memory.router, prefix="/ai/memory", tags=["ai-memory"])
