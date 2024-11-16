from typing import TYPE_CHECKING

from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

if TYPE_CHECKING:
    from models.olympic import Olympic
from models.result import Result


class Event(SQLModel, table=True):
    __tablename__ = "events"

    event_id: str = Field(
        max_length=7,
        primary_key=True,
    )

    name: str = Field(max_length=40)
    eventtype: str = Field(
        max_length=20,
    )
    is_team_event: int = Field(
        ge=0,
        le=1,
    )
    num_players_in_team: int = Field(ge=0)
    result_noted_in: str = Field(max_length=100)

    olympic_id: str = Field(
        foreign_key="olympics.olympic_id",
        max_length=7,
    )

    olympic: "Olympic" = Relationship(back_populates="events")
    results: list[Result] = Relationship(back_populates="event")
