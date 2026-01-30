"""merge_all_heads

Revision ID: 07bf4700b3a4
Revises: add_invoice_template, b1ab24d9e06d
Create Date: 2026-01-23 02:49:43.241484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07bf4700b3a4'
down_revision = ('add_invoice_template', 'b1ab24d9e06d')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
