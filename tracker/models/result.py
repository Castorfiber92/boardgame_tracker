from tracker.models.player import Player
from tracker.models.session import Session

class Result:
    def __init__(self, session: Session, player: Player, score: int, placement: int):
        self.session = session
        self.player = player
        self.score = score
        self.placement = placement

    def __repr__(self):
        return f"Session(name={self.date}, player={self.player}, score={self.score}))"
