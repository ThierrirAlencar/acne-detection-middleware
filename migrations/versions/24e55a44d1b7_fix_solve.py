"""fix: solve

Revision ID: 24e55a44d1b7
Revises: c5e1d4759f0e
Create Date: 2026-04-13 13:37:39.126600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24e55a44d1b7'
down_revision: Union[str, Sequence[str], None] = 'c5e1d4759f0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
