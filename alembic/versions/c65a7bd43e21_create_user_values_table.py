"""create user_values table

Revision ID: c65a7bd43e21
Revises: dd0817a4cdf5
Create Date: 2025-03-01 19:42:36.705887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c65a7bd43e21'
down_revision: Union[str, None] = 'dd0817a4cdf5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
