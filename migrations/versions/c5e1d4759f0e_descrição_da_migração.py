"""descrição da migração

Revision ID: c5e1d4759f0e
Revises: e86c2fac634f
Create Date: 2026-04-06 16:26:42.706028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5e1d4759f0e'
down_revision: Union[str, Sequence[str], None] = 'e86c2fac634f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
