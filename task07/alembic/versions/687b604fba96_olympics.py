"""olympics

Revision ID: 687b604fba96
Revises: 00ad3f3a7a78
Create Date: 2024-11-14 23:27:21.764310

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from sqlmodel import SQLModel

# revision identifiers, used by Alembic.
revision: str = '687b604fba96'
down_revision: Union[str, None] = '00ad3f3a7a78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sqltext="""
    insert into public.olympics (olympic_id, country_id, city, year, startdate, enddate)
    values  ('SYD2000', 'AUS', 'Sydney                                            ', 2000, '2000-09-15', '2000-10-01'),
            ('ATH2004', 'GRE', 'Athens                                            ', 2004, '2004-07-19', '2004-08-04');
    """)


def downgrade() -> None:
    op.execute(sqltext="""
    TRUNCATE public.olympics CASCADE;
    """)
