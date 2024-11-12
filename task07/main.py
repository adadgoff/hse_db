from sqlmodel import SQLModel

from core.db import engine

SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
