from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection

# revision identifiers, used by Alembic.
revision = '9183ea4e9f46'
down_revision = 'de13624e5514'
branch_labels = None
depends_on = None

def table_exists(table_name, conn):
    """Check if a table exists in the database."""
    inspector = reflection.Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    return table_name in tables

def column_exists(table_name, column_name, conn):
    """Check if a column exists in a given table."""
    inspector = reflection.Inspector.from_engine(conn)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def upgrade():
    conn = op.get_bind()

    # Check if the 'role' column already exists before adding it
    if not column_exists('user', 'role', conn):
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=False, server_default='user'))

    # Check if the 'subject' table already exists before creating it
    if not table_exists('subject', conn):
        op.create_table(
            'subject',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('name', sa.String(length=100), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade():
    conn = op.get_bind()

    # Check if the 'role' column exists before dropping it
    if column_exists('user', 'role', conn):
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.drop_column('role')

    # Check if the 'subject' table exists before dropping it
    if table_exists('subject', conn):
        op.drop_table('subject')
