from fastapi import APIRouter, HTTPException
from tracker.api.schemas import BoardGameCreate
from tracker.models.boardgame import BoardGame
from tracker.storage.database import get_session

router = APIRouter(prefix="/boardgames", tags=["boardgames"])

@router.post("/")
def create_boardgame(boardgame_data: BoardGameCreate):
    with get_session() as db:
        boardgame = BoardGame(name=boardgame_data.name)
        db.add(boardgame)
        db.commit()
        db.refresh(boardgame)
        return {"id": boardgame.id, "name": boardgame.name}

@router.get("/")
def get_boardgames():
    with get_session() as db:
        boardgames = db.query(BoardGame).all()
        return [{"id": b.id, "name": b.name} for b in boardgames]