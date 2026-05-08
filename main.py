from tracker.storage.database import Base, engine
from tracker.models.player import Player
from tracker.models.boardgame import BoardGame
from tracker.models.session import Session
from tracker.models.result import GameResult

from tracker.api.players import router as players_router
from tracker.api.boardgames import router as boardgames_router
from tracker.api.sessions import router as sessions_router

from fastapi import FastAPI

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(players_router)
app.include_router(boardgames_router)
app.include_router(sessions_router)
@app.get("/")
def root():
    return {"message": "Boardgame Tracker API"}