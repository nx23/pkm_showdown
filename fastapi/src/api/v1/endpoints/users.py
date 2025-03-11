from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.database import get_session #type: ignore
from db.models import Users #type: ignore
from utils.security import get_current_user #type: ignore

router = APIRouter(prefix="/users")

@router.get("/me", response_model=Users)
def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=Users)
def read_user(user_id: int, db: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
    db_user = db.get(Users, user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user

@router.get("/", response_model=List[Users])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    users = db.query(Users).offset(skip).limit(limit).all()
    return users

@router.put("/{user_id}", response_model=Users)
def update_existing_user(user_id: int, user: Users, db: Session = Depends(get_session)):
    db_user = db.get(Users, user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    for key, value in user.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=Users)
def delete_existing_user(user_id: int, db: Session = Depends(get_session)):
    db_user = db.get(Users, user_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user