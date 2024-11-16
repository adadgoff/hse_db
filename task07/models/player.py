from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

if TYPE_CHECKING:
    from models.country import Country
    from models.result import Result


class Player(SQLModel, table=True):
    __tablename__ = "players"

    player_id: str = Field(
        max_length=10,
        primary_key=True,
    )

    name: str = Field(max_length=40)
    birthdate: datetime

    country_id: str = Field(
        foreign_key="countries.country_id",
        max_length=3,
    )

    country: "Country" = Relationship(back_populates="players")
    results: list["Result"] = Relationship(back_populates="player")
