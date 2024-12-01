from typing import Optional
from sqlmodel import SQLModel, create_engine, Session
from decimal import Decimal
from model import Boardgames, User


sql_alchemy_database_url_sketch = 'postgresql://<username>:<password>@<ip-adress:port/hostname>/ <database_name' 

sql_user = 'kuehn'
sql_passoword= 'password'
host = 'localhost'
db = 'boardgames'
port = '5433'

sql_db_url = f'postgresql+psycopg://{sql_user}:{sql_passoword}@{host}:{port}/{db}' 

engine = create_engine(sql_db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

