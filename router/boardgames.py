from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, desc, asc
from decimal import Decimal
from model import Boardgames
from db import engine
from fastapi import APIRouter, HTTPException,status

router = APIRouter(prefix="/boardgames")


@router.post("/")
async def create_boardgame(boardgame: Boardgames):

    game = Boardgames(name=boardgame.name, bgg_rating=boardgame.bgg_rating, image=boardgame.image)#, bgg_rating=bgg_rating, image=image
    """muss noch Bild unf BGG wertung von bgg bekommen bevor ich das dann speichern kann"""
    with Session(engine) as session:
        session.add(game)
        session.commit()
        session.refresh(game)

    return game


@router.get("/")
async def get_boardgames(
    order: str = 'bgg_rating',
    search: Optional[str] = "",
    limit: int = 10):

    order_column = getattr(Boardgames, order, None)
    # Add wildcards for partial matching
    search_pattern = f"%{search}%" if search else "%"


    with Session(engine) as session:
        if order == 'name':
            statement = select(Boardgames).where(Boardgames.name.ilike(search_pattern)).order_by(asc(order_column)).limit(limit)
        else:
            statement = select(Boardgames).where(Boardgames.name.ilike(search_pattern)).order_by(desc(order_column)).limit(limit)
        boardgames = session.exec(statement).all()

    return boardgames

@router.get('/{id}', response_model= Boardgames)
async def get_single_game(id:int=id):
    
    with Session(engine) as session:
        statement = select(Boardgames).where(Boardgames.id == id)
        boardgames = session.exec(statement).one_or_none()

        if not boardgames:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                            ,detail=f"Boardgame with id: {id} does not exist")

    return boardgames

@router.delete('/{id}')
async def delete_single_game(id:int=id):

    with Session(engine) as session:
        statement = select(Boardgames).where(Boardgames.id == id)
        boardgame = session.exec(statement).one_or_none()
        if not boardgame:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                ,detail=f"Boardgame with id: {id} does not exist")

        else:
            session.delete(boardgame)
            session.commit()

    return {"message": f"Boardgame with id {id} has been deleted successfully"}