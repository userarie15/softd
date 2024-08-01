"""Add email field to StudentInfo model

Revision ID: 81cd70b2dcf2
Revises: 4b38ba24dae3
Create Date: 2024-07-15 22:33:35.768871

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = '81cd70b2dcf2'
down_revision = '4b38ba24dae3'
branch_labels = None
depends_on = None


def upgrade():
    # Check if the 'email' column already exists in 'student_info'
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)
    columns = [col['name'] for col in inspector.get_columns('student_info')]

    if 'email' not in columns:
        with op.batch_alter_table('student_info', schema=None) as batch_op:
            batch_op.add_column(sa.Column('email', sa.String(length=150), nullable=False))

def downgrade():
    # Remove 'email' column if it exists
    bind = op.get_bind()
    inspector = reflection.Inspector.from_engine(bind)
    columns = [col['name'] for col in inspector.get_columns('student_info')]

    if 'email' in columns:
        with op.batch_alter_table('student_info', schema=None) as batch_op:
            batch_op.drop_column('email')