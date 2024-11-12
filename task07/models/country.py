from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
)

from olympic import Olympic
from player import Player


class Country(SQLModel, table=True):
    __tablename__ = "countries"

    country_id: str = Field(
        max_length=3,
        primary_key=True,
    )

    name: str = Field(max_length=40)
    area_sqkm: int
    population: int

    olympics: list[Olympic] = Relationship(back_populates="country")
    players: list[Player] = Relationship(back_populates="country")
