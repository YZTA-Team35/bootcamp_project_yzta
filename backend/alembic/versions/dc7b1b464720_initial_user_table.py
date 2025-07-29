"""initial user table

Revision ID: dc7b1b464720
Revises: 2eb3947e52e5
Create Date: 2025-07-06 23:47:34.383837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc7b1b464720'
down_revision: Union[str, None] = '2eb3947e52e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
