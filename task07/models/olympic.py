from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from models.event import Event
if TYPE_CHECKING:
    from models.country import Country


class Olympic(SQLModel, table=True):
    __tablename__ = "olympics"

    olympic_id: str = Field(
        max_length=7,
        primary_key=True,
    )

    city: str = Field(max_length=50)
    year: int
    startdate: datetime
    enddate: datetime

    country_id: str = Field(
        foreign_key="countries.country_id",
        max_length=3,
    )

    country: "Country" = Relationship(back_populates="olympics")
    events: list[Event] = Relationship(back_populates="olympic")
