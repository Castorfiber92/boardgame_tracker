from datetime import datetime
from tracker.models.player import Player
from tracker.models.game import BoardGame

class Session:
    def __init__(self, date: datetime, boardgame: BoardGame, players: list[Player]):
        self.date = date
        self.boardgame = boardgame
        self.players = players

    def __repr__(self):
        return f"Session(name={self.date}, boardgame={self.boardgame})"
