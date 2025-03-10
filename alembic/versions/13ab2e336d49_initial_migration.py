"""Initial migration

Revision ID: 13ab2e336d49
Revises: c65a7bd43e21
Create Date: 2025-03-10 20:09:52.579800

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13ab2e336d49'
down_revision: Union[str, None] = 'c65a7bd43e21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
