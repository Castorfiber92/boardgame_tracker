from datetime import datetime
from tracker.models.player import Player
from tracker.models.game import BoardGame
from tracker.models.session import Session
from tracker.models.result import Result

def test_player():
    player = Player("Karl")
    assert player.name == "Karl"

def test_player_no_email():
    player = Player("Karl")
    assert player.email == None

def test_boardgame():
    boardgame = BoardGame("Terraforming Mars")
    assert boardgame.name == "Terraforming Mars"

def test_session():
    date = datetime.now()
    boardgame = BoardGame("Terraforming Mars")
    player = Player("Karl")
    session = Session(date, boardgame, [player])

    assert session.boardgame.name == "Terraforming Mars"

def test_result():
    date = datetime.now()
    boardgame = BoardGame("Terraforming Mars")
    player = Player("Karl")
    session = Session(date, boardgame, [player])
    score = 17
    placement = 1
    result = Result(session, player, score, placement)
    
    assert result.score == 17
    assert result.placement == 1
    assert result.player.name == "Karl"

    