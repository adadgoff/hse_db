from sqlmodel import create_engine

from .config import settings

engine = create_engine(
    url=str(settings.SQLALCHEMY_DATABASE_URI),
)
