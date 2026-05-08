from pydantic import BaseModel
from datetime import datetime

class PlayerCreate(BaseModel):
    name: str

class BoardGameCreate(BaseModel):
    name: str

class GameResultCreate(BaseModel):
    player_id: int
    score: int
    placement: int

class SessionCreate(BaseModel):
    date: datetime
    boardgame_id: int
    results: list[GameResultCreate]