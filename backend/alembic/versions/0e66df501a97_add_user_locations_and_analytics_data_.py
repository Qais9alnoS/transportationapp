"""add user_locations and analytics_data tables

Revision ID: 0e66df501a97
Revises: 6390f52d2174
Create Date: 2025-07-08 17:06:05.514876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e66df501a97'
down_revision: Union[str, Sequence[str], None] = '6390f52d2174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('analytics_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_type', sa.String(), nullable=True),
    sa.Column('value', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analytics_data_id'), 'analytics_data', ['id'], unique=False)
    op.create_table('user_locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lng', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_locations_id'), 'user_locations', ['id'], unique=False)
    op.create_unique_constraint(None, 'routes', ['name'])
    op.create_unique_constraint(None, 'stops', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'stops', type_='unique')
    op.drop_constraint(None, 'routes', type_='unique')
    op.create_table('spatial_ref_sys',
    sa.Column('srid', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('auth_name', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('auth_srid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('srtext', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.Column('proj4text', sa.VARCHAR(length=2048), autoincrement=False, nullable=True),
    sa.CheckConstraint('srid > 0 AND srid <= 998999', name=op.f('spatial_ref_sys_srid_check')),
    sa.PrimaryKeyConstraint('srid', name=op.f('spatial_ref_sys_pkey'))
    )
    op.drop_index(op.f('ix_user_locations_id'), table_name='user_locations')
    op.drop_table('user_locations')
    op.drop_index(op.f('ix_analytics_data_id'), table_name='analytics_data')
    op.drop_table('analytics_data')
    # ### end Alembic commands ###
