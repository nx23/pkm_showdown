from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import env

engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
