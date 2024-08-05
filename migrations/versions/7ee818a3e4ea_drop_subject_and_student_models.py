"""Drop Subject and Student models

Revision ID: 7ee818a3e4ea
Revises: f90b9e3640ce
Create Date: 2024-08-05 23:09:08.690094

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import OperationalError

# revision identifiers, used by Alembic.
revision = '7ee818a3e4ea'
down_revision = 'f90b9e3640ce'
branch_labels = None
depends_on = None

def upgrade():
    # Create a temporary table to hold existing data
    try:
        op.create_table(
            '_alembic_tmp_user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('password', sa.String(), nullable=True),
            sa.Column('role', sa.String(), nullable=True),  # Allow NULL values temporarily
            sa.PrimaryKeyConstraint('id')
        )
    except OperationalError as e:
        if 'table _alembic_tmp_user already exists' not in str(e):
            raise

    # Copy existing data into the temporary table
    op.execute("""
    INSERT INTO _alembic_tmp_user (id, email, password, role)
    SELECT id, email, password, role FROM user
    """)

    # Drop the old user table
    op.drop_table('user')

    # Recreate the user table with NOT NULL constraints and a default value
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False, server_default='student'),  # Default value for role
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data back from the temporary table to the new user table
    op.execute("""
    INSERT INTO user (id, email, password, role)
    SELECT id, email, password, COALESCE(role, 'student') FROM _alembic_tmp_user
    """)

    # Drop the temporary table
    op.drop_table('_alembic_tmp_user')

def downgrade():
    pass  # Implement if needed