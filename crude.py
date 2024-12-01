from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, desc, asc
from decimal import Decimal
from model import Boardgames, User
from db import engine
from passlib.context import CryptContext




# create boardgame in db function
def create_boardgame(
    name: str,
    #bgg_rating: Optional[int],
    #image: Optional[str]

) -> Boardgames:
    # Create an item instance using the provided parameters
    game = Boardgames(name=name)#, bgg_rating=bgg_rating, image=image
    """muss noch Bild unf BGG wertung von bgg bekommen bevor ich das dann speichern kann"""

    with Session(engine) as session:
        session.add(game)
        session.commit()
        session.refresh(game)

    return game


#create user
def create_user(
        name: str,
        email: str,
        password: str
)-> User:
    hashed_pw = get_password_hash(password)
    user = User(name=name, email=email,password=hashed_pw)
    
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    
    return user

def get_all_boardgames()->Boardgames:

    with Session(engine) as session:
        statement = select(Boardgames).order_by(asc(Boardgames.name)).limit(5)
        all_boardgames = session.exec(statement).all()
    
    return all_boardgames
