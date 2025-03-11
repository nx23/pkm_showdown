from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError #type: ignore
from db.database import get_session #type: ignore
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from db.models import Users #type: ignore

import dotenv
import os

dotenv.load_dotenv()

# Create a CryptContext for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for security. Did you forget to set it in the .env file?")

REFRESH_TOKEN_ALGORITHM = os.getenv("REFRESH_TOKEN_ALGORITHM")
if not REFRESH_TOKEN_ALGORITHM:
    raise ValueError("No ALGORITHM set for security. Did you forget to set it in the .env file?")

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    if expires_delta:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=REFRESH_TOKEN_ALGORITHM)

def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[REFRESH_TOKEN_ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        user = db.query(Users).filter(Users.username == username).first()

    except JWTError:
        raise credentials_exception
    
    return user

def authenticate_user(username: str, password: str, db: Session = Depends(get_session)) -> Users:
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user