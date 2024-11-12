from decimal import Decimal

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from event import Event
from player import Player


class Result(SQLModel, table=True):
    __tablename__ = "results"

    event_id: int = Field(
        foreign_key="events.id",
        max_length=7,
    )
    player_id: int = Field(
        foreign_key="players.id",
        max_length=10,
    )
    medal: str = Field(max_length=7)
    result: Decimal

    event: Event = Relationship(back_populates="results")
    player: Player = Relationship(back_populates="results")
