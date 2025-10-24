"""Add advanced subscription fields

Revision ID: 001
Revises: 
Create Date: 2025-10-24 14:33:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add advanced subscription fields to subscriptions table
    op.add_column('subscriptions', sa.Column('subscription_type', sa.String(), nullable=False, server_default='recurring'))
    op.add_column('subscriptions', sa.Column('interval_unit', sa.String(), nullable=True))
    op.add_column('subscriptions', sa.Column('interval_count', sa.Integer(), nullable=True, server_default='1'))
    op.add_column('subscriptions', sa.Column('has_trial', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('subscriptions', sa.Column('trial_start_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('trial_end_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('start_date', sa.Date(), nullable=True))
    op.add_column('subscriptions', sa.Column('duration_type', sa.String(), nullable=True))
    op.add_column('subscriptions', sa.Column('duration_value', sa.Integer(), nullable=True))
    op.add_column('subscriptions', sa.Column('end_date', sa.Date(), nullable=True))


def downgrade() -> None:
    # Remove advanced subscription fields from subscriptions table
    op.drop_column('subscriptions', 'end_date')
    op.drop_column('subscriptions', 'duration_value')
    op.drop_column('subscriptions', 'duration_type')
    op.drop_column('subscriptions', 'start_date')
    op.drop_column('subscriptions', 'trial_end_date')
    op.drop_column('subscriptions', 'trial_start_date')
    op.drop_column('subscriptions', 'has_trial')
    op.drop_column('subscriptions', 'interval_count')
    op.drop_column('subscriptions', 'interval_unit')
    op.drop_column('subscriptions', 'subscription_type')

