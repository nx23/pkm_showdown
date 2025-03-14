import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from .models import Team_Members, Users

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    # Create all tables
    SQLModel.metadata.create_all(
        engine,
        tables=[
            Users.metadata.tables["users"],
            Team_Members.metadata.tables["team_members"],
        ],
    )
