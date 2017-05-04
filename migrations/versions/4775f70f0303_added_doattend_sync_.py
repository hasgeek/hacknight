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
    op.add_column('event', sa.Column('sync_credentials', sa.Unicode(100), nullable=True))
    op.add_column('event', sa.Column('sync_service', sa.Unicode(100), nullable=True))
    op.add_column('event', sa.Column('sync_eventsid', sa.Unicode(100), nullable=True))


def downgrade():
    op.drop_column('event', 'sync_credentials')
    op.drop_column('event', 'sync_service')
    op.drop_column('event', 'sync_eventsid')
