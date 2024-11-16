from sqlmodel import Session, func

from core.db import engine
from models.country import Country
from models.event import Event
from models.olympic import Olympic
from models.player import Player
from models.result import Result


def query_1():
    with Session(engine) as session:
        results = (
            session.query(
                func.extract("year", Player.birthdate).label("year_of_birth"),
                func.count(func.distinct(Player.player_id)).label("number_of_players"),
                func.count(Result.medal).filter(Result.medal == "Gold").label("gold_medals"),
            )
            .join(Result, Result.player_id == Player.player_id)
            .join(Event, Event.event_id == Result.event_id)
            .join(Olympic, Olympic.olympic_id == Event.olympic_id)
            .filter(Olympic.year == 2004)
            .group_by(func.extract("year", Player.birthdate))
            .all()
        )
        return results


def query_2():
    with Session(engine) as session:
        results = (
            session.query(Event.name.label("event_name"))
            .join(Result, Result.event_id == Event.event_id)
            .filter(Event.is_team_event == 0)
            .filter(Result.medal == "Gold")
            .group_by(Event.event_id, Result.result)
            .having(func.count(Result.player_id) > 1)
            .all()
        )
        return results


def query_3():
    with Session(engine) as session:
        results = (
            session.query(
                Player.name.label("player_name"),
                Olympic.olympic_id.label("olympic_id"),
            )
            .join(Result, Result.player_id == Player.player_id)
            .join(Event, Event.event_id == Result.event_id)
            .join(Olympic, Olympic.olympic_id == Event.olympic_id)
            .filter(Result.medal.in_(["Gold", "Silver", "Bronze"]))
            .distinct()
            .all()
        )
        return results


def query_4():
    with Session(engine) as session:
        total_players_subquery = (
            session.query(
                Country.country_id,
                func.count(Player.player_id).label("total_players")
            )
            .join(Player, Player.country_id == Country.country_id)
            .group_by(Country.country_id)
            .subquery()
        )

        results = (
            session.query(
                Country.name.label("country_name"),
                (func.count(Player.player_id) / total_players_subquery.c.total_players).label("percentage"),
            )
            .join(Player, Player.country_id == Country.country_id)
            .join(total_players_subquery, total_players_subquery.c.country_id == Country.country_id)
            .filter(
                Player.name.ilike("a%") |
                Player.name.ilike("e%") |
                Player.name.ilike("i%") |
                Player.name.ilike("o%") |
                Player.name.ilike("u%")
            )
            .group_by(Country.country_id, Country.name, total_players_subquery.c.total_players)
            .order_by(func.count(Player.player_id).desc())
            .first()
        )

        return results


def query_5():
    with Session(engine) as session:
        results = (
            session.query(
                Country.name.label("country_name"),
                (func.count(Result.medal).filter(Event.is_team_event == 1) / Country.population).label("ratio"),
            )
            .join(Olympic, Olympic.country_id == Country.country_id)
            .join(Event, Event.olympic_id == Olympic.olympic_id)
            .join(Result, Result.event_id == Event.event_id)
            .filter(Olympic.year == 2000)
            .group_by(Country.country_id)
            .order_by(func.count(Result.medal).filter(Event.is_team_event == 1) / Country.population)
            .limit(5)
            .all()
        )
        return results
