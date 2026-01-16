"""Merge heads

Revision ID: d2add373c12c
Revises: 66305e49e1e0, add_license_system
Create Date: 2026-01-15 03:50:57.135750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2add373c12c'
down_revision = ('66305e49e1e0', 'add_license_system')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
