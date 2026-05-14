from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import List
from tracker.storage.database import get_session
from tracker.models.player import Player
from tracker.models.boardgame import BoardGame
from tracker.models.session import Session
from tracker.models.game_result import GameResult

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/log-tm-session", response_class=HTMLResponse)
def log_tm_session_page(request: Request):
    with get_session() as db:
        players = db.query(Player).all()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    return templates.TemplateResponse(
        request=request,
        name="log_tm_session_step1.html",
        context={"players": players, "default_date": now}
    )


@router.post("/log-tm-session/step2", response_class=HTMLResponse)
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

@router.post("/log-tm-session/submit")
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
        # Error handling if Terraforming Mars is missing from database.
        if tm_game is None:
            return templates.TemplateResponse(
                request=request,
                name="error.html",
                context={"message": "Terraforming Mars not found in the database. Please add it via the boardgames endpoint."}
            )
        
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