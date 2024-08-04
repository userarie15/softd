from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# Revision identifiers, used by Alembic.
revision = '2d55a57ee8fa'
down_revision = '9183ea4e9f46'
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()

    # Check if the column exists before adding it
    result = connection.execute(text("PRAGMA table_info(user)"))
    column_names = [row[1] for row in result]  # Adjusted index for column names

    if 'new_column' not in column_names:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.add_column(sa.Column('new_column', sa.String(length=50)))

    # Alter existing column type if it exists
    if 'existing_column' in column_names:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.alter_column('existing_column', type_=sa.String(length=100))

def downgrade():
    connection = op.get_bind()
    result = connection.execute(text("PRAGMA table_info(user)"))
    column_names = [row[1] for row in result]  # Adjusted index for column names

    if 'new_column' in column_names:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.drop_column('new_column')

    if 'existing_column' in column_names:
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.alter_column('existing_column', type_=sa.String(length=50))
