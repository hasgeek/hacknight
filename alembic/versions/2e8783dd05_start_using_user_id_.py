"""start using user_id as foreign key for comments, project

Revision ID: 2e8783dd05
Revises: 2bc8921a82b1
Create Date: 2013-01-25 14:33:08.327389

"""

# revision identifiers, used by Alembic.
revision = '2e8783dd05'
down_revision = '2bc8921a82b1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    """Add a foreign key user_id to project table, then drop participant_id and
    similarily for project_member
    """
    op.add_column('project', sa.Column('user_id', sa.Integer))
    op.create_foreign_key("fk_project_user_id", "project", "user", ["user_id"], ["id"])
    connection = op.get_bind()
    connection.execute("update project set user_id=participant.user_id from participant where project.participant_id=participant.id")
    op.drop_column('project', 'participant_id')
    op.add_column('project_member', sa.Column('user_id', sa.Integer))
    op.create_foreign_key("fk_project_member_user_id", "project_member", "user", ["user_id"], ["id"])
    op.create_unique_constraint("uq_project_member", "project_member", ["project_id", "user_id"])
    connection.execute("update project_member set user_id=participant.user_id from participant where project_member.participant_id=participant.id")
    op.drop_column('project_member', 'participant_id')


def downgrade():
    connection = op.get_bind()
    # project table
    op.add_column('project', sa.Column('participant_id', sa.Integer))
    op.create_foreign_key("fk_project_participant_id", "project", "participant", ["participant_id"], ["id"])
    connection.execute("update project set participant_id=participant.id from participant where project.user_id=participant.user_id")
    op.drop_column('project', 'user_id')
    # project_member table
    op.add_column('project_member', sa.Column('participant_id', sa.Integer))
    op.create_foreign_key("fk_project_member_partcipant_id", "project_member", "participant", ["participant_id"], ["id"])
    connection.execute("update project_member set participant_id=participant.id from participant where project_member.user_id=participant.user_id")
    op.drop_column('project_member', 'user_id')
