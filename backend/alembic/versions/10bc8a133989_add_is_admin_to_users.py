"""add_is_admin_to_users

Revision ID: 10bc8a133989
Revises: 931366abc0c3
Create Date: 2025-10-19 15:28:48.470447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10bc8a133989'
down_revision: Union[str, Sequence[str], None] = '931366abc0c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.alter_column('users', 'is_admin', server_default=None)

def downgrade() -> None:
    op.drop_column('users', 'is_admin')