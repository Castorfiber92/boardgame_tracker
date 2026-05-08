from fastapi import APIRouter, HTTPException
from tracker.api.schemas import BoardGameCreate
from tracker.models.boardgame import BoardGame
from tracker.storage.database import get_session

router = APIRouter(prefix="/boardgames", tags=["boardgames"])

@router.post("/")
def create_boardgame(boardgame_data: BoardGameCreate):
    with get_session() as session:
        boardgame = BoardGame(name=boardgame_data.name)
        session.add(boardgame)
        session.commit()
        session.refresh(boardgame)
        return {"id": boardgame.id, "name": boardgame.name}

@router.get("/")
def get_boardgames():
    with get_session() as session:
        boardgames = session.query(BoardGame).all()
        return [{"id": b.id, "name": b.name} for b in boardgames]