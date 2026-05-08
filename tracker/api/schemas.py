from pydantic import BaseModel

class PlayerCreate(BaseModel):
    name: str

class BoardGameCreate(BaseModel):
    name: str
    