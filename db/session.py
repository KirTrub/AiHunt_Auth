import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv, dotenv_values
load_dotenv()

db_name=os.getenv("DB_NAME")
db_user=os.getenv("DB_USER")
db_pass=os.getenv("DB_PASSWORD")
dburl = "postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host=/var/lib/postgresql/data"

engine = create_async_engine(dburl)

async_session = async_sessionmaker(
    bind=engine,          
    class_=AsyncSession,   
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session

class Base(DeclarativeBase):
    pass