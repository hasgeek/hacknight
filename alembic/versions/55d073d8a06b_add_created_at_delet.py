"""Add created_at, deleted_at column

Revision ID: 55d073d8a06b
Revises: 386c09cab07e
Create Date: 2013-05-15 19:49:26.825172

"""

# revision identifiers, used by Alembic.
revision = '55d073d8a06b'
down_revision = '386c09cab07e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('redirect', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('redirect', sa.Column('updated_at', sa.DateTime(), nullable=False))


def downgrade():
    op.delete_column('redirect', 'created_at')
    op.delete_column('redirect', 'updated_at')
