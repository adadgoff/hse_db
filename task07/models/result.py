from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

if TYPE_CHECKING:
    from models.event import Event
from models.player import Player


class Result(SQLModel, table=True):
    __tablename__ = "results"

    event_id: str = Field(
        foreign_key="events.event_id",
        primary_key=True,
        max_length=7,
    )
    player_id: str = Field(
        foreign_key="players.player_id",
        primary_key=True,
        max_length=10,
    )
    medal: str = Field(max_length=7)
    result: Decimal

    event: "Event" = Relationship(back_populates="results")
    player: Player = Relationship(back_populates="results")
