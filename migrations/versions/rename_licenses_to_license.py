"""rename licenses table to license

Revision ID: rename_licenses_to_license
Revises: 07bf4700b3a4
Create Date: 2024-01-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_licenses_to_license'
down_revision = '07bf4700b3a4'
branch_labels = None
depends_on = None


def upgrade():
    # Rename table from 'licenses' to 'license'
    op.rename_table('licenses', 'license')

    # Note: Foreign key constraints will automatically reference the new table name
    # in most databases. If issues occur, they can be manually recreated.


def downgrade():
    # Rename table back to 'licenses'
    op.rename_table('license', 'licenses')

