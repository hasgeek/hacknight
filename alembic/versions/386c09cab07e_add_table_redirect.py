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
        'event_redirect',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('profile_id', sa.Integer, nullable=False),
        sa.Column('name', sa.Unicode(250), nullable=False),
        sa.Column('event_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.create_foreign_key("fk_event_redirect_event_id", "event_redirect", "event", ["event_id"], ["id"])


def downgrade():
    op.drop_table('event_redirect')
    op.drop_constraint("fk_event_redirect_event_id")
