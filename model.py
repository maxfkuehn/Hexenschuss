from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel
from datetime import datetime
from pydantic import field_validator
from sqlalchemy import CheckConstraint
# define of table classes

#boardgames
class Boardgames(SQLModel, table=True):

    __tablename__ = "boardgames"

    id: Optional[int] = Field(default=None, primary_key=True, nullable= False)
    name : str = Field(nullable=False, index=True)
    bgg_rating: Optional[int] = Field(default=None,nullable=True)
    image: Optional[str] = Field(default=None,nullable=True) # default no Image machen ?
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

#user

class User(SQLModel, table=True):

    __tablename__ = 'user'

    id: Optional[int] = Field(default=None, primary_key=True, nullable= False)
    email: str = Field(nullable= False, unique=True)
    name : str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

#user ratings of boardgames

class BoardgameRatings(SQLModel, table=True):
    __tablename__ = 'user_ratings'
    __table_args__ = (
        CheckConstraint('rating >= 0 and rating <= 10', name='check_rating_range'),
    )  # Enforce range in DB

    id: Optional[int] = Field(default=None, primary_key=True, nullable= False)
    user_id: int = Field(foreign_key= "user.id",  primary_key=True,nullable= False)
    game_id: int = Field(foreign_key="boardgames.id", primary_key=True ,nullable= False)
    rating: Decimal = Field(nullable=False, max_digits=3, decimal_places=1)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

       # Alternatively, use Pydantic validator for custom validation
    # Using @field_validator for input validation (Pydantic v2 style)
    @field_validator("rating")
    def check_rating_value(cls, value):
        if value < 0 or value > 10:
            raise ValueError("Rating must be between 0 and 10")
        return value

class PlayedGame(SQLModel, table=True):
    __tablename__ = 'played_games'

    user_ids: int = Field(primary_key=True,foreign_key= "user.id", nullable= False) 
    game_id: int = Field(foreign_key="boardgames.id", nullable= False)
    play_id: int = Field(primary_key=True,nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

