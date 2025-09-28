"""Add database indexes for performance

Revision ID: 931366abc0c3
Revises: c476d7c2b095
Create Date: 2025-09-28 13:48:28.337861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '931366abc0c3'
down_revision: Union[str, Sequence[str], None] = 'c476d7c2b095'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add indexes for performance
    op.create_index('ix_orders_user_id_created_at', 'orders', ['user_id', 'created_at'])
    op.create_index('ix_orders_status', 'orders', ['status'])
    op.create_index('ix_order_items_order_id', 'order_items', ['order_id'])
    op.create_index('ix_order_items_product_id', 'order_items', ['product_id'])


def downgrade() -> None:
    """Downgrade schema."""
    # Remove indexes
    op.drop_index('ix_order_items_product_id', table_name='order_items')
    op.drop_index('ix_order_items_order_id', table_name='order_items')
    op.drop_index('ix_orders_status', table_name='orders')
    op.drop_index('ix_orders_user_id_created_at', table_name='orders')
