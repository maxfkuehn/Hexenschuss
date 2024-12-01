from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, desc, asc
from decimal import Decimal
from model import Boardgames, User
from db import engine
from passlib.context import CryptContext
from fastapi import APIRouter, HTTPException, status
from schemas import UserBase


router = APIRouter(prefix="/user")

# hasing 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_password_hash(password):

    return pwd_context.hash(password)

#create_user
@router.post("/")
async def create_user(user: User):
    hashed_pw = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email,password=hashed_pw)
    
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    
    return user

@router.get("/{id}",response_model= UserBase)
async def get_single_user(id:int):

    with Session(engine) as session:
        statement = select(User).filter(User.id==id)
        selected_user = session.exec(statement).first()

        if not selected_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND
                                ,detail=f"User with id: {id} does not exist")
        
        
    
    return selected_user
