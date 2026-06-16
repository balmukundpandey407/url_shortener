from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
from dotenv import load_dotenv

load_dotenv()

DB_url=os.getenv('Database_URL')

engine=create_engine(DB_url)

local_session=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()

def get_db():
    db=local_session()
    try:
        yield db
    finally:
        db.close()