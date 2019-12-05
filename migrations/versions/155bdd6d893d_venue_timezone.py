"""Venue timezone

Revision ID: 155bdd6d893d
Revises: 4775f70f0303
Create Date: 2013-12-19 10:55:24.058607

"""

# revision identifiers, used by Alembic.
revision = '155bdd6d893d'
down_revision = '4775f70f0303'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('venue', sa.Column('timezone', sa.Unicode(length=40), nullable=False, server_default='UTC'))
    op.alter_column('venue', 'timezone', server_default=None)


def downgrade():
    op.drop_column('venue', 'timezone')
