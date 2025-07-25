"""add resolved_at to complaints

Revision ID: 3b7a25a849c2
Revises: 0e66df501a97
Create Date: 2025-07-09 16:33:05.546685
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3b7a25a849c2'
down_revision: Union[str, Sequence[str], None] = '0e66df501a97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('complaints', sa.Column('resolved_at', sa.DateTime(), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('complaints', 'resolved_at')
