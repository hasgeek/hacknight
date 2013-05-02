"""Add email support for event participation notice

Revision ID: 132231d12fcd
Revises: 2e8783dd05
Create Date: 2013-04-27 11:09:23.896698

"""

# revision identifiers, used by Alembic.
revision = '132231d12fcd'
down_revision = '2e8783dd05'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('confirmation_message', sa.UnicodeText, nullable=False, server_default=sa.text(u'')))
    op.add_column('event', sa.Column('confirmation_message_text', sa.UnicodeText, nullable=False, server_default=sa.text(u'')))
    op.add_column('event', sa.Column('waitlisted_message', sa.UnicodeText, nullable=False, server_default=sa.text(u'')))
    op.add_column('event', sa.Column('waitlisted_message_text', sa.UnicodeText, nullable=False, server_default=sa.text(u'')))
    op.add_column('event', sa.Column('rejected_message', sa.UnicodeText, nullable=False, server_default=sa.text(u'')))
    op.add_column('event', sa.Column('rejected_message_text', sa.UnicodeText, nullable=False, server_default=sa.text(u'')))


def downgrade():
    op.drop_column('event', 'confirmation_message')
    op.drop_column('event', 'confirmation_message_text')
    op.drop_column('event', 'waitlisted_message')
    op.drop_column('event', 'waitlisted_message_text')
    op.drop_column('event', 'rejected_message')
    op.drop_column('event', 'rejected_message_text')
