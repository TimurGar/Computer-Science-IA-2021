"""timestamp to Project table added

Revision ID: 7273d9901bd2
Revises: a07788ff4ffd
Create Date: 2021-07-20 11:51:39.779356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7273d9901bd2'
down_revision = 'a07788ff4ffd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_project_timestamp'), 'project', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_project_timestamp'), table_name='project')
    op.drop_column('project', 'timestamp')
    # ### end Alembic commands ###
