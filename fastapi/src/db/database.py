import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

# Create all tables
SQLModel.metadata.create_all(engine)
