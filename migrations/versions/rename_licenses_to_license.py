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
    
    # Update foreign key references
    # Drop old foreign key in license_checks
    with op.batch_alter_table('license_checks', schema=None) as batch_op:
        batch_op.drop_constraint('license_checks_license_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('license_checks_license_id_fkey', 'license', ['license_id'], ['id'])
    
    # Drop old foreign key in users
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_license_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_users_license_id', 'license', ['license_id'], ['id'])


def downgrade():
    # Revert foreign keys
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_license_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_users_license_id', 'licenses', ['license_id'], ['id'])
    
    with op.batch_alter_table('license_checks', schema=None) as batch_op:
        batch_op.drop_constraint('license_checks_license_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('license_checks_license_id_fkey', 'licenses', ['license_id'], ['id'])
    
    # Rename table back
    op.rename_table('license', 'licenses')

