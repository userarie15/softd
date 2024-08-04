"""Remove last_name and first_name from user

Revision ID: de13624e5514
Revises: 81cd70b2dcf2
Create Date: 2024-08-04 12:00:00
"""

# revision identifiers, used by Alembic.
revision = 'de13624e5514'
down_revision = '81cd70b2dcf2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    # Drop columns from the 'user' table directly
    # Using raw SQL to avoid batch_alter_table issues
    op.execute('ALTER TABLE user DROP COLUMN last_name')
    op.execute('ALTER TABLE user DROP COLUMN first_name')

def downgrade():
    # Re-add the columns to the 'user' table
    # Using raw SQL to avoid batch_alter_table issues
    op.execute('ALTER TABLE user ADD COLUMN last_name VARCHAR(150) NOT NULL')
    op.execute('ALTER TABLE user ADD COLUMN first_name VARCHAR(150) NOT NULL')
