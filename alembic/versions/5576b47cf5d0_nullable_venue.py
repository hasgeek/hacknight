"""Nullable venue

Revision ID: 5576b47cf5d0
Revises: 155bdd6d893d
Create Date: 2014-03-06 15:23:02.513275

"""

# revision identifiers, used by Alembic.
revision = '5576b47cf5d0'
down_revision = '155bdd6d893d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('event', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade():
    op.alter_column('event', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
