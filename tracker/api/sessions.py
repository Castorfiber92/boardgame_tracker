from fastapi import APIRouter, HTTPException

from tracker.api.schemas import SessionCreate, GameResultCreate
from tracker.models.session import Session
from tracker.models.result import GameResult

from tracker.storage.database import get_session

from sqlalchemy.orm import joinedload

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/")
def create_session(session_data: SessionCreate):
    with get_session() as db:
        db_session = Session(
            date=session_data.date,
            boardgame_id=session_data.boardgame_id,
            
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        for result_data in session_data.results:
            game_result = GameResult(
                session_id=db_session.id,
                player_id=result_data.player_id,
                score=result_data.score,
                placement=result_data.placement
            )
            db.add(game_result)
        db.commit()
        return {"id": db_session.id, "date": db_session.date}

@router.get("/")
def get_sessions():
    with get_session() as db:
        sessions = db.query(Session).options(
            joinedload(Session.boardgame),
            joinedload(Session.results).joinedload(GameResult.player)
        ).all()
        return [
            {
                "id": s.id, 
                "date": s.date, 
                "boardgame": s.boardgame.name,
                "players": [
                    {
                        "player": r.player.name
                    }
                    for r in s.results
                ]
            } 
            for s in sessions]