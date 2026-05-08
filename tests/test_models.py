from datetime import datetime
from tracker.models.player import Player
from tracker.models.game import BoardGame
from tracker.models.session import Session
from tracker.models.result import GameResult

def test_player():
    player = Player(name = "Karl")
    assert player.name == "Karl"

def test_boardgame():
    boardgame = BoardGame(name = "Terraforming Mars")
    assert boardgame.name == "Terraforming Mars"

def test_session():
    date = datetime.now()
    boardgame = BoardGame(name = "Terraforming Mars")
    player = Player(name = "Karl")
    session = Session(date = date, boardgame = boardgame)

    assert session.boardgame.name == "Terraforming Mars"

def test_result():
    date = datetime.now()
    boardgame = BoardGame(name = "Terraforming Mars")
    player = Player(name = "Karl")
    session = Session(date = date, boardgame = boardgame)
    score = 17
    placement = 1
    result = GameResult(session = session, player = player, score = score, placement = placement)
    
    assert result.score == 17
    assert result.placement == 1
    assert result.player.name == "Karl"

    