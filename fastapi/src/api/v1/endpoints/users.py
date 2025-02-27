from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.database import get_session #type: ignore
from db.models import User #type: ignore
from utils.security import hash_password #type: ignore

router = APIRouter()

@router.post("/users/", response_model=User)
def create_new_user(user: User, db: Session = Depends(get_session)):
    user.password = hash_password(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.put("/users/{user_id}", response_model=User)
def update_existing_user(user_id: int, user: User, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=User)
def delete_existing_user(user_id: int, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user