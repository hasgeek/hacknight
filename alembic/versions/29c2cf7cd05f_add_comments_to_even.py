"""Add comments to events

Revision ID: 29c2cf7cd05f
Revises: 2e8783dd05
Create Date: 2013-04-19 21:29:32.485229

"""

# revision identifiers, used by Alembic.
revision = '29c2cf7cd05f'
down_revision = '2e8783dd05'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('comments_id', sa.Integer, sa.ForeigenKey('commentspace.id')))


def downgrade():
    op.remove_column('event', 'comments_id')
