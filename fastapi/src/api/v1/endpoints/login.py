from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db.database import get_session #type: ignore
from db.models import Users #type: ignore
from utils.security import get_password_hash, create_access_token, authenticate_user #type: ignore

router = router = APIRouter(prefix="/login")

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
def create_new_user(user: Users, db: Session = Depends(get_session)):

    if db.query(Users).filter(Users.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    user.password = get_password_hash(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=30)
    
    return Token(access_token=access_token, token_type="bearer")

@router.post("/token", response_model=Token)
def login_for_access_token(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(data={"sub": user.username}, expires_delta=30)
    return Token(access_token=access_token, token_type="bearer")
