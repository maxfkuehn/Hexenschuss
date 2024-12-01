from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    created_at: datetime

class UserCreate(UserBase):
    email: EmailStr
    password: str


class Boardgame(BaseModel):

    name : str 

class UserGamePair(BaseModel):

    user_id: int
    game_id: int

class BoardgameRatings(UserGamePair):
    
    rating: int

class PlayedGames(UserGamePair):

    play_id_: int
