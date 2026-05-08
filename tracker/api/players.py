from fastapi import APIRouter, HTTPException
from tracker.api.schemas import PlayerCreate
from tracker.models.player import Player
from tracker.storage.database import get_session

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/")
def create_player(player_data: PlayerCreate):
    with get_session() as session:
        player = Player(name=player_data.name)
        session.add(player)
        session.commit()
        session.refresh(player)
        return {"id": player.id, "name": player.name}

@router.get("/")
def get_players():
    with get_session() as session:
        players = session.query(Player).all()
        return [{"id": p.id, "name": p.name} for p in players]