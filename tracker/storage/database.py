import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///boardgame_tracker.db")

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    return Session(engine)