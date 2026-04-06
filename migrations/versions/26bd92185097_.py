"""empty message

Revision ID: 26bd92185097
Revises: 382ff211761a
Create Date: 2026-04-06 16:23:27.748338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26bd92185097'
down_revision: Union[str, Sequence[str], None] = '382ff211761a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
