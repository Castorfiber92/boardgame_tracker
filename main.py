# storage folder
from tracker.storage.database import Base, engine

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

# pages folder
from tracker.pages.home import router as home_router
from tracker.pages.sessions import router as page_sessions_router
from tracker.pages.tm_sessions import router as page_tm_sessions_router

# fastapi imports
from fastapi import FastAPI

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(players_router)
app.include_router(boardgames_router)
app.include_router(sessions_router)
app.include_router(home_router)
app.include_router(page_sessions_router)
app.include_router(page_tm_sessions_router)


