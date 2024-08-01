"""Add user_id to StudentInfo

Revision ID: 4b38ba24dae3
Revises: 1aba310bd3fc
Create Date: 2024-07-15 21:44:40.839714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b38ba24dae3'
down_revision = '1aba310bd3fc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('student_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            'fk_student_info_user',  # Name of the constraint
            'user', ['user_id'], ['id']
        )
    # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('student_info', schema=None) as batch_op:
        batch_op.drop_constraint('fk_student_info_user', type_='foreignkey')
        batch_op.drop_column('user_id')
        

    # ### end Alembic commands ###
