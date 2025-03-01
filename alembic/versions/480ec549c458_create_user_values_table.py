"""create user_values table

Revision ID: 480ec549c458
Revises: 21f566abb5a3
Create Date: 2025-03-01 18:49:20.822988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '480ec549c458'
down_revision: Union[str, None] = '21f566abb5a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
