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

from typing import List

@app.post("/log-tm-session/step2", response_class=HTMLResponse)
def log_tm_session_step2(
    request: Request,
    date: str = Form(...),
    generations: int = Form(None),
    turmoil: bool = Form(False),
    venus_next: bool = Form(False),
    colonies: bool = Form(False),
    prelude: bool = Form(False),
    prelude_2: bool = Form(False),
    player_id: List[int] = Form(...),
    corporation: List[str] = Form(...)
):
    with get_session() as db:
        players = [db.get(Player, pid) for pid in player_id]
    
    return templates.TemplateResponse(
        request=request,
        name="log_tm_session_step2.html",
        context={
            "date": date,
            "generations": generations,
            "turmoil": turmoil,
            "venus_next": venus_next,
            "colonies": colonies,
            "prelude": prelude,
            "prelude_2": prelude_2,
            "player_ids": player_id,
            "corporations": corporation,
            "players": players
        }
    )

@app.post("/log-tm-session/submit")
def log_tm_session_submit(
    request: Request,
    date: str = Form(...),
    generations: str = Form(None),
    turmoil: str = Form("False"),
    venus_next: str = Form("False"),
    colonies: str = Form("False"),
    prelude: str = Form("False"),
    prelude_2: str = Form("False"),
    player_id: List[int] = Form(...),
    corporation: List[str] = Form(...),
    tr_rating: List[int] = Form(...),
    points_milestones_and_awards: List[int] = Form(...),
    points_board: List[int] = Form(...),
    points_on_cards: List[int] = Form(...),
    points_from_cards: List[int] = Form(...)
):
    with get_session() as db:
        # Create the general session
        session_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")

        # Conver generations to int
        generations_value = int(generations) if generations and generations != "None" else None
        
        # Find the Terraforming Mars boardgame
        tm_game = db.query(BoardGame).filter(BoardGame.name == "Terraforming Mars").first()
        
        db_session = Session(
            date=session_date,
            boardgame_id=tm_game.id
        )
        db.add(db_session)
        db.commit()
        db.refresh(db_session)

        # Create TerraformingMarsSession
        tm_session = TerraformingMarsSession(
            session_id=db_session.id,
            generations=generations_value,
            turmoil=turmoil == "True",
            venus_next=venus_next == "True",
            colonies=colonies == "True",
            prelude=prelude == "True",
            prelude_2=prelude_2 == "True"
        )
        db.add(tm_session)
        db.commit()

        # Calculate totals and determine placements
        totals = [
            tr_rating[i] + points_milestones_and_awards[i] + points_board[i] +
            points_on_cards[i] + points_from_cards[i]
            for i in range(len(player_id))
        ]
        
        # Sort totals descending to determine placement
        sorted_totals = sorted(totals, reverse=True)

        # Create GameResult and TerraformingMarsResult for each player
        for i in range(len(player_id)):
            placement = sorted_totals.index(totals[i]) + 1

            game_result = GameResult(
                session_id=db_session.id,
                player_id=player_id[i],
                score=totals[i],
                placement=placement
            )
            db.add(game_result)
            db.commit()
            db.refresh(game_result)

            tm_result = TerraformingMarsResult(
                game_result_id=game_result.id,
                corporation=corporation[i],
                tr_rating=tr_rating[i],
                points_milestones_and_awards=points_milestones_and_awards[i],
                points_board=points_board[i],
                points_on_cards=points_on_cards[i],
                points_from_cards=points_from_cards[i]
            )
            db.add(tm_result)

        db.commit()

    return RedirectResponse(url="/", status_code=303)