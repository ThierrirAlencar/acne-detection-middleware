"""empty message

Revision ID: e86c2fac634f
Revises: 26bd92185097
Create Date: 2026-04-06 16:24:42.300447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e86c2fac634f'
down_revision: Union[str, Sequence[str], None] = '26bd92185097'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
