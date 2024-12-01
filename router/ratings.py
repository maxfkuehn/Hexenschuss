from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, desc, asc
from decimal import Decimal
from model import BoardgameRatings, User
from db import engine
from fastapi import APIRouter, HTTPException,status


router = APIRouter(prefix="/ratings")

@router.get("/boardgame/{id}")
async def get_boardgame_ratings(id: int = id):

    
    with Session(engine) as session:
        """
        meine erste selbe geschriebene Funtion die Funktioniert.
        unten die bessere Lösung durhc CHat GTP.
        Untere Version liest beides direkt aus SQL aus.
        
        statement= select(BoardgameRatings.user_id,BoardgameRatings.rating).where(BoardgameRatings.game_id==id)

        user_name_ratings = session.exec(statement).all()
        
        user_ids = [id for id, rating in user_id_ratings]
        ratings = [rating for id,rating in user_id_ratings ]

        user_names = []
        for id in user_ids:
            user_statement = select(User.name).where(User.id==id)
            user_name= session.exec(user_statement).all()
            user_names.append(user_name)
        
        """
        # Join BoardgameRatings with User to fetch user names and ratings
        statement = (
            select(User.name, BoardgameRatings.rating)
            .join(BoardgameRatings, User.id == BoardgameRatings.user_id)
            .where(BoardgameRatings.game_id == id)
        )
        results = session.exec(statement).all()

        # Extract names and ratings
        user_names = [name for name, rating in results]
        ratings = [rating for name, rating in results]

    return {"username":user_names,"user_ratings":ratings}