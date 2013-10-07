"""Added DoAttend Sync details

Revision ID: 4775f70f0303
Revises: 386c09cab07e
Create Date: 2013-10-07 23:05:32.372628

"""

# revision identifiers, used by Alembic.
revision = '4775f70f0303'
down_revision = '386c09cab07e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('doattend_api_key', sa.Unicode(250), nullable=False, server_default=sa.text(u"''")))
    op.add_column('event', sa.Column('doattend_event_id', sa.Integer, nullable=False, server_default=sa.text('0')))
    # Alter column
    op.alter_column('event', 'doattend_api_key', server_default=None)
    op.alter_column('event', 'doattend_event_id', server_default=None)


def downgrade():
    op.drop_column('event', 'doattend_api_key')
    op.drop_column('event', 'doattend_event_id')
