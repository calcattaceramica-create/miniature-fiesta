"""add invoice_template to company

Revision ID: add_invoice_template
Revises: 
Create Date: 2026-01-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_invoice_template'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add invoice_template column to companies table
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('invoice_template', sa.String(length=50), nullable=True))
    
    # Set default value for existing records
    op.execute("UPDATE companies SET invoice_template = 'modern' WHERE invoice_template IS NULL")


def downgrade():
    # Remove invoice_template column from companies table
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_column('invoice_template')

