"""Add email support for event pending participant

Revision ID: 60e09c23fa7
Revises: 132231d12fcd
Create Date: 2013-04-27 12:20:45.602944

"""

# revision identifiers, used by Alembic.
revision = '60e09c23fa7'
down_revision = '132231d12fcd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('pending_message', sa.UnicodeText))
    op.add_column('event', sa.Column('pending_message_text', sa.UnicodeText))


def downgrade():
    op.drop_column('event', 'pending_message')
    op.drop_column('event', 'pending_message_text')
