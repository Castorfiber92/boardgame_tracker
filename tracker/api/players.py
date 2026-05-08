from fastapi import APIRouter, HTTPException
from tracker.api.schemas import PlayerCreate
from tracker.models.player import Player
from tracker.storage.database import get_session

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/")
def create_player(player_data: PlayerCreate):
    with get_session() as db:
        player = Player(name=player_data.name)
        db.add(player)
        db.commit()
        db.refresh(player)
        return {"id": player.id, "name": player.name}

@router.get("/")
def get_players():
    with get_session() as db:
        players = db.query(Player).all()
        return [{"id": p.id, "name": p.name} for p in players]