from datetime import datetime

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from country import Country
from result import Result


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

    country: Country = Relationship(back_populates="players")
    results: list[Result] = Relationship(back_populates="player")
