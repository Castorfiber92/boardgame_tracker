from tracker.storage.database import Base, engine
from tracker.models.player import Player
from tracker.models.game import BoardGame
from tracker.models.session import Session
from tracker.models.result import GameResult

Base.metadata.create_all(engine)

print("Database tables created!")