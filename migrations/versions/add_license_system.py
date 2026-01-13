"""add license system

Revision ID: add_license_system
Revises: 
Create Date: 2024-01-12 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = 'add_license_system'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create licenses table
    op.create_table('licenses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('license_key', sa.String(length=64), nullable=False),
        sa.Column('company_name', sa.String(length=128), nullable=False),
        sa.Column('machine_id', sa.String(length=32), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('expiry_date', sa.DateTime(), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=True),
        sa.Column('license_type', sa.String(length=32), nullable=True),
        sa.Column('max_users', sa.Integer(), nullable=True),
        sa.Column('features', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('activation_count', sa.Integer(), nullable=True),
        sa.Column('last_check', sa.DateTime(), nullable=True),
        sa.Column('contact_email', sa.String(length=120), nullable=True),
        sa.Column('contact_phone', sa.String(length=20), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on license_key
    op.create_index(op.f('ix_licenses_license_key'), 'licenses', ['license_key'], unique=True)
    
    # Add license_id column to users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('license_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_users_license_id', 'licenses', ['license_id'], ['id'])


def downgrade():
    # Remove license_id from users
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_license_id', type_='foreignkey')
        batch_op.drop_column('license_id')
    
    # Drop licenses table
    op.drop_index(op.f('ix_licenses_license_key'), table_name='licenses')
    op.drop_table('licenses')

