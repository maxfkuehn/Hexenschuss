from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
from contextlib import asynccontextmanager
from db import create_db_and_tables
from router import boardgames, user, ratings
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://192.168.178.26:8080",  # Allowing Vue app running on this IP/port
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    #on start before request
    create_db_and_tables()
    yield
    #after server gets closed


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers)
)

#User crud

app.include_router(user.router)

#boardgame cruds
app.include_router(boardgames.router)

#ratings cruds

app.include_router(ratings.router)