"""create user_values table

Revision ID: dd0817a4cdf5
Revises: 480ec549c458
Create Date: 2025-03-01 19:26:25.447090

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd0817a4cdf5'
down_revision: Union[str, None] = '480ec549c458'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
