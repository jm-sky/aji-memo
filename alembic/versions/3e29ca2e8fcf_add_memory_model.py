"""Add Memory model

Revision ID: 3e29ca2e8fcf
Revises: 
Create Date: 2025-07-17 20:50:48.055051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR


# revision identifiers, used by Alembic.
revision: str = '3e29ca2e8fcf'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create memories table
    op.create_table(
        'memories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('uid', sa.String(length=255), nullable=False),
        sa.Column('namespace', sa.String(length=255), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('tags', ARRAY(sa.String()), nullable=False),
        sa.Column('created_by', sa.String(length=255), nullable=True),
        sa.Column('search_vector', TSVECTOR(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_memories_id'), 'memories', ['id'], unique=False)
    op.create_index(op.f('ix_memories_uid'), 'memories', ['uid'], unique=False)
    op.create_index(op.f('ix_memories_namespace'), 'memories', ['namespace'], unique=False)
    op.create_index('idx_uid_namespace', 'memories', ['uid', 'namespace'], unique=False)
    op.create_index('idx_tags', 'memories', ['tags'], unique=False, postgresql_using='gin')
    op.create_index('idx_search_vector', 'memories', ['search_vector'], unique=False, postgresql_using='gin')
    op.create_index('idx_created_at', 'memories', ['created_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop indexes
    op.drop_index('idx_created_at', table_name='memories')
    op.drop_index('idx_search_vector', table_name='memories')
    op.drop_index('idx_tags', table_name='memories')
    op.drop_index('idx_uid_namespace', table_name='memories')
    op.drop_index(op.f('ix_memories_namespace'), table_name='memories')
    op.drop_index(op.f('ix_memories_uid'), table_name='memories')
    op.drop_index(op.f('ix_memories_id'), table_name='memories')
    
    # Drop table
    op.drop_table('memories')
