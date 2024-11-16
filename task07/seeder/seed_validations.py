import functools

from typing import Callable

from sqlmodel import (
    select,
    Session,
)

from core.db import engine
from models.country import Country
from seeder import COUNTRIES


ERROR_DELIMITER = ";\n"
SENTENCE_DELIMITER = ". "


def get_count_countries_message(count_countries: int) -> str:
    count_countries_message_parts: list[str] = []

    if count_countries > len(COUNTRIES):
        count_countries_message_parts.append(SENTENCE_DELIMITER.join([
            f"The total count of countries in the world is {len(COUNTRIES)}",
            "For the count of countries, see https://en.wikipedia.org/wiki/ISO_3166-1",
        ]))

    with Session(engine) as session:
        count_countries_in_database = len(session.exec(select(Country)).all())

        if count_countries + count_countries_in_database > len(COUNTRIES):
            count_countries_message_parts.append(SENTENCE_DELIMITER.join([
                "The requested count of countries greater than the unused countries",
                f"Total unused countries: {len(COUNTRIES) - count_countries_in_database}",
            ]))

    return ERROR_DELIMITER.join(count_countries_message_parts)


def get_invalid_counts(**kwargs) -> list[str]:
    invalid_counts: list[str] = []

    for count_var, count in kwargs.items():
        if not (isinstance(count, int) and count >= 0):
            invalid_counts.append(
                f"'{count_var}' must be greater positive integer (greater than or equal to zero)",
            )
        if count_var == "count_countries" and isinstance(count, int):
            count_countries_message = get_count_countries_message(count_countries=count)
            if count_countries_message:
                invalid_counts.append(
                    f"'{count_var}' is invalid:\n{count_countries_message}",
                )

    return invalid_counts


def validate_counts(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(**kwargs):
        invalid_counts = get_invalid_counts(**kwargs)
        if invalid_counts:
            raise ValueError(ERROR_DELIMITER.join(invalid_counts) + '.')
        func(**kwargs)

    return wrapper
