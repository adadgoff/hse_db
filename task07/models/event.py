from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from olympic import Olympic
from result import Result


class Event(SQLModel, table=True):
    __tablename__ = "events"

    event_id: str = Field(
        max_length=7,
        primary_key=True,
    )

    name: str = Field(max_length=40)
    event_type = Field(
        alias="event_type",
        max_length=20,
    )
    is_team_event: int = Field(
        ge=0,
        le=1,
    )
    num_players_in_team: int = Field(ge=0)
    result_noted_int: str = Field(max_length=100)

    olympic_id: str = Field(
        foreign_key="olympics.id",
        max_length=7,
    )

    olympic: Olympic = Relationship(back_populates="events")
    results: list[Result] = Relationship(back_populates="result")
