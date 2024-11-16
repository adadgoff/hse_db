import textwrap

import click

from click import command  # noqa. Autocomplete bug. See more:
# https://youtrack.jetbrains.com/issue/PY-52665
# /False-Expected-type-Command-got-Any-instead-when-click-command-imported-from-other-module.

from seeder import seed
from queries import (
    query_1,
    query_2,
    query_3,
    query_4,
    query_5,
)


@click.command(name="seed", help="Seed the database.")
@click.option("--count-countries", default=10, help="Count of countries to create.")
@click.option("--count-events", default=20, help="Count of events to create.")
@click.option("--count-olympics", default=5, help="Count of olympics to create.")
@click.option("--count-players", default=50, help="Count of players to create.")
@click.option("--count-results", default=30, help="Count of results to create.")
def seeder_cmd(
        count_countries: int,
        count_events: int,
        count_olympics: int,
        count_players: int,
        count_results: int,
) -> None:
    seed(
        count_countries=count_countries,
        count_events=count_events,
        count_olympics=count_olympics,
        count_players=count_players,
        count_results=count_results,
    )
    click.echo("Data was successfully seeded!")


@click.command(name="info", help="Task queries information.")
def info_cmd():
    click.echo(textwrap.dedent(
        """\
        "Task information: [https://classroom.google.com/c/NzEwNjA2OTI2MDQy/a/NzIzNzAxMDczNDI1/details]."
        
        Queries:
        
        1. For the 2004 Olympic Games, generate a list of (year of birth, number of players,
        number of gold medals), including the years in which players were born, the number
        of players born in each of those years who won at least one gold medal, and the
        number of gold medals won by players born in that year.
        
        2. List all individual (non-team) events where there was a tie score, and two or more players won gold medals.

        3. Find all players who won at least one medal (GOLD, SILVER, or BRONZE) in a single Olympic Games:
        (player-name, olympic-id).
        
        4. Which country had the highest percentage of players (from those listed in the dataset) 
        whose names started with a vowel?
        
        5. For the 2000 Olympic Games, find the top 5 countries with the lowest ratio of team medals to population size.
        """
    ))


@click.command(name="query-1", help="Query 1. See more information about the query using command 'info'.")
def query_1_cmd():
    click.echo("Query 1. See more information about the query using command 'info'.")
    results = query_1()
    click.echo("\nResults:")
    for row in results:
        click.echo(
            f"Year of Birth: {row.year_of_birth}, Players: {row.number_of_players}, Gold Medals: {row.gold_medals}")


@click.command(name="query-2", help="Query 2. See more information about the query using command 'info'.")
def query_2_cmd():
    click.echo("Query 2. See more information about the query using command 'info'.")
    results = query_2()
    click.echo("\nIndividual Events with Tie and Multiple Golds:")
    for event in results:
        click.echo(f"Event Name: {event.event_name}")


@click.command(name="query-3", help="Query 3. See more information about the query using command 'info'.")
def query_3_cmd():
    click.echo("Query 3. See more information about the query using command 'info'.")
    results = query_3()
    click.echo("\nPlayers and Olympics:")
    for row in results:
        click.echo(f"Player Name: {row.player_name}, Olympic ID: {row.olympic_id}")


@click.command(name="query-4", help="Query 4. See more information about the query using command 'info'.")
def query_4_cmd():
    click.echo("Query 4. See more information about the query using command 'info'.")
    result = query_4()
    click.echo("\nCountry with Highest Percentage of Players with Names Starting with a Vowel:")
    click.echo(f"Country Name: {result.country_name}, Percentage: {result.percentage:.2%}")


@click.command(name="query-5", help="Query 5. See more information about the query using command 'info'.")
def query_5_cmd():
    click.echo("Query 5. See more information about the query using command 'info'.")
    results = query_5()
    click.echo("\nTop 5 Countries with Lowest Team Medal to Population Ratio:")
    for row in results:
        click.echo(f"Country Name: {row.country_name}, Ratio: {row.ratio:.8f}")
