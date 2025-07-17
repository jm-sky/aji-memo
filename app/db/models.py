from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    ARRAY,
    Text,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    plan = Column(String(20), default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active = Column(Boolean, default=True)

    # Relationships
    api_tokens = relationship("ApiToken", back_populates="user")
    usage_logs = relationship("ApiUsage", back_populates="user")
    memories = relationship("Memory", back_populates="user")


class ApiToken(Base):
    __tablename__ = "api_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token_name = Column(String(100), nullable=False)
    token_hash = Column(String(255), nullable=False)
    permissions = Column(JSONB, default={})
    rate_limit_per_hour = Column(Integer, default=5)
    last_used_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    user = relationship("User", back_populates="api_tokens")
    usage_logs = relationship("ApiUsage", back_populates="token")


class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token_id = Column(
        Integer, ForeignKey("api_tokens.id", ondelete="CASCADE"), nullable=False
    )
    endpoint = Column(String(100), nullable=False)
    response_status = Column(Integer, nullable=False)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="usage_logs")
    token = relationship("ApiToken", back_populates="usage_logs")


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    uid = Column(String(255), nullable=False, index=True)
    namespace = Column(String(255), nullable=False, index=True)
    text = Column(Text, nullable=False)
    tags = Column(ARRAY(String), default=[], nullable=False)
    created_by = Column(String(255), nullable=True)
    search_vector = Column(TSVECTOR)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="memories")

    # Indexes for better performance
    __table_args__ = (
        Index("idx_uid_namespace", "uid", "namespace"),
        Index("idx_tags", "tags", postgresql_using="gin"),
        Index("idx_search_vector", "search_vector", postgresql_using="gin"),
        Index("idx_created_at", "created_at"),
    )
