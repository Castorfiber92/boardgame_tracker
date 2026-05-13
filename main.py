# storage folder
from tracker.storage.database import Base, engine, get_session

# models folder
from tracker.models.player import Player
from tracker.models.boardgame import BoardGame
from tracker.models.session import Session
from tracker.models.game_result import GameResult
from tracker.models.terraforming_mars_session import TerraformingMarsSession
from tracker.models.terraforming_mars_result import TerraformingMarsResult

# api folder
from tracker.api.players import router as players_router
from tracker.api.boardgames import router as boardgames_router
from tracker.api.sessions import router as sessions_router

# fastapi imports
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import joinedload
from datetime import datetime
from typing import List

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

@app.get("/log-session", response_class=HTMLResponse)
def log_session_page(request: Request):
    with get_session() as db:
        boardgames = db.query(BoardGame).all()
        players = db.query(Player).all()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return templates.TemplateResponse(
        request=request,
        name="log_session.html",
        context={
            "boardgames": boardgames,
            "players": players,
            "default_date": now
        }
    )

@app.post("/log-session")
def log_session_submit(
    request: Request,
    boardgame_id: int = Form(...),
    date: str = Form(...),
    player_id: List[int] = Form(...),
    score: List[int] = Form(...),
    placement: List[int] = Form(...)
):
    with get_session() as db:
        session_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        db_session = Session(
            date=session_date,
            boardgame_id=boardgame_id
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        for i in range(len(player_id)):
            game_result = GameResult(
                session_id=db_session.id,
                player_id=player_id[i],
                score=score[i],
                placement=placement[i]
            )
            db.add(game_result)
        db.commit()

    return RedirectResponse(url="/", status_code=303)

@app.get("/add-game", response_class=HTMLResponse)
def add_game_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add_game.html",
        context={}
    )

@app.post("/add-game")
def add_game_submit(name: str = Form(...)):
    with get_session() as db:
        game = BoardGame(name=name)
        db.add(game)
        db.commit()
    return RedirectResponse(url="/log-session", status_code=303)


@app.get("/add-player", response_class=HTMLResponse)
def add_player_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add_player.html",
        context={}
    )

@app.post("/add-player")
def add_player_submit(name: str = Form(...)):
    with get_session() as db:
        player = Player(name=name)
        db.add(player)
        db.commit()
    return RedirectResponse(url="/log-session", status_code=303)

@app.get("/log-tm-session", response_class=HTMLResponse)
def log_tm_session_page(request: Request):
    with get_session() as db:
        players = db.query(Player).all()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return templates.TemplateResponse(
        request=request,
        name="log_tm_session_step1.html",
        context={"players": players, "default_date": now}
    )