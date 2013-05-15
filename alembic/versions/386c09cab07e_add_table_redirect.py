"""Add Table Redirect

Revision ID: 386c09cab07e
Revises: 60e09c23fa7
Create Date: 2013-05-15 19:06:12.665297

"""

# revision identifiers, used by Alembic.
revision = '386c09cab07e'
down_revision = '60e09c23fa7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'redirect',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('profile_id', sa.Integer, nullable=False),
        sa.Column('old_event_name', sa.Unicode(250), nullable=False),
        sa.Column('new_event_name', sa.Unicode(250), nullable=False))


def downgrade():
    op.drop_table('redirect')
