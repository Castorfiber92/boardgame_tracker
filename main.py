# storage folder
from tracker.storage.database import Base, engine, get_session

# models folder
from tracker.models.player import Player
from tracker.models.boardgame import BoardGame
from tracker.models.session import Session
from tracker.models.result import GameResult

# api folder
from tracker.api.players import router as players_router
from tracker.api.boardgames import router as boardgames_router
from tracker.api.sessions import router as sessions_router

# fastapi imports
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import joinedload

Base.metadata.create_all(engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(players_router)
app.include_router(boardgames_router)
app.include_router(sessions_router)

@app.get("/", response_class=HTMLResponse)
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