# Task07

> Author: Dadykov Artemy, BSE225.
>
> Автор: Дадыков Артемий, БПИ225.

```shell
# Use Unix OS (macOS | Linux).

# Activate database.
docker-compose up -d

# Setup virtual environment.
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install

# Run migrations.
alembic upgrade head

# It is possible to roll back migrations.
# alembic downgrade base

# Generate database data.
python3 main.py seed

# Run queries.
python3 main.py query-1
python3 main.py query-2
python3 main.py query-3
python3 main.py query-4
python3 main.py query-5
```