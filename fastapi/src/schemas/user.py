from pydantic import BaseModel
from typing import Optional

# Base model shared across other models
class UserBase(BaseModel):
    username: str
    is_active: Optional[bool] = True

# Model for creating a new user
class UserCreate(UserBase):
    password: str  # The plain-text password (will be hashed before storage)

# Model for updating an existing user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None  # Allow password updates
    is_active: Optional[bool] = None

# Model for returning user data in responses
class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models