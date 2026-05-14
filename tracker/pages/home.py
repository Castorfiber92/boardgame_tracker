from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import joinedload
from tracker.storage.database import get_session
from tracker.models.session import Session
from tracker.models.game_result import GameResult

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    with get_session() as db:
        sessions = db.query(Session).options(
            joinedload(Session.boardgame),
            joinedload(Session.results).joinedload(GameResult.player)
        ).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"sessions": sessions}
    )