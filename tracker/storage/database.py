from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///boardgame_tracker.db", echo=True)

def get_session():
    return Session(engine)