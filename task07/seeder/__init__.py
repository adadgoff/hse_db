import itertools
import random
import uuid

from datetime import datetime
from decimal import Decimal

import faker

from sqlmodel import (
    select,
    Session,
)

from core.db import engine
from models.country import Country
from models.event import Event
from models.olympic import Olympic
from models.player import Player
from models.result import Result
from seeder.consts import COUNTRIES
from seeder.seed_validations import validate_counts

fake = faker.Faker()


# Uncomment if you want to configure the seed.
# fake.seed_instance(seed=42)


@validate_counts
def seed(
        count_countries: int,
        count_events: int,
        count_olympics: int,
        count_players: int,
        count_results: int,
) -> None:
    # Did not use the 'Repository' layer
    # because the project is small
    # and there is (almost) no duplication of code.

    with Session(engine) as session:
        country_ids_in_database = set(country.country_id for country in session.exec(select(Country)).all())
        country_ids = set(country.alpha_3 for country in list(COUNTRIES))
        # Guaranteed len(unused_country_ids) = count_countries. See decorator '@validate_counts'.
        unused_country_ids = list(country_ids - country_ids_in_database)[:count_countries]

        countries: list[Country] = []
        for country_id in unused_country_ids:
            country = Country(
                country_id=country_id,
                name=COUNTRIES.get(alpha_3=country_id).name,
                # TODO: Possible to improve 'area_sqkm' and 'population' via 'requests'.
                area_sqkm=random.randint(a=10_000, b=500_000),
                population=random.randint(a=100_000, b=50_000_000),
            )
            countries.append(country)
            session.add(country)
        session.commit()

        olympics: list[Olympic] = []
        for _ in range(count_olympics):
            year = random.randint(a=1950, b=2024)
            olympic = Olympic(
                olympic_id=str(uuid.uuid4())[:7],
                city=fake.city(),
                year=year,
                startdate=datetime(
                    day=random.randint(a=1, b=20),
                    month=random.randint(a=1, b=6),
                    year=year,
                ),
                enddate=datetime(
                    day=random.randint(a=1, b=20),
                    month=random.randint(a=7, b=12),
                    year=year,
                ),
                country=random.choice(countries),
            )
            olympics.append(olympic)
            session.add(olympic)
        session.commit()

        players: list[Player] = []
        for _ in range(count_players):
            player = Player(
                player_id=str(uuid.uuid4())[:10],
                name=fake.name(),
                birthdate=fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=40,
                ),
                country=random.choice(countries),
            )
            players.append(player)
            session.add(player)
        session.commit()

        events: list[Event] = []
        event_types = [
            "Acrobatic Gymnastics",
            "Alpine Skiing",
            "Archery",
            "Artistic Gymnastics",
            "Artistic Swimming",
            "Athletics",
        ]
        for _ in range(count_events):
            event_type = random.choice(event_types)
            event = Event(
                event_id=str(uuid.uuid4())[:7],
                name=f"{event_type}: '{fake.word()}'",
                eventtype=event_type,
                is_team_event=random.randint(a=0, b=1),
                num_players_in_team=random.randint(a=1, b=5),
                # TODO: Possible to improve 'result_noted_in' value.
                result_noted_in=fake.word(),
                olympic=random.choice(olympics),
            )
            events.append(event)
            session.add(event)
        session.commit()

        medals = [
            "Gold",
            "Silver",
            "Bronze",
            "None",
        ]
        # TODO: The maximum value of 'count_results' depends on 'count_events', 'count_players'.
        #  It is better to validate.
        for event, player in itertools.islice(
                itertools.product(events, players),
                count_results,
        ):
            result = Result(
                # TODO: Possible to improve awarding 'medal' logic according to the 'result' value.
                medal=random.choice(medals),
                result=Decimal(random.uniform(a=10, b=100)),
                event=event,
                player=player,
            )
            session.add(result)
        session.commit()
