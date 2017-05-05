"""add colum apply_instructions

Revision ID: 2bc8921a82b1
Revises: None
Create Date: 2013-01-21 15:31:03.211356

"""

# revision identifiers, used by Alembic.
revision = '2bc8921a82b1'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('apply_instructions', sa.UnicodeText))


def downgrade():
    op.drop_column('event', 'apply_instructions')
