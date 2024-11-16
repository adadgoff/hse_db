"""init

Revision ID: 577cdab6393a
Revises: 
Create Date: 2024-11-14 23:26:58.392077

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from sqlmodel import SQLModel

from core.db import engine

from models.country import Country  # noqa.
from models.event import Event  # noqa.
from models.olympic import Olympic  # noqa.
from models.player import Player  # noqa.
from models.result import Result  # noqa.

# revision identifiers, used by Alembic.
revision: str = '577cdab6393a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # It's better to declare explicit.
    SQLModel.metadata.create_all(engine)


def downgrade() -> None:
    # It's better to declare explicit.
    SQLModel.metadata.drop_all(engine)
