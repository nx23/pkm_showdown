from pydantic import BaseModel
from typing import Optional

# Base model shared across other models
class TeamMemberBase(BaseModel):
    owner_id: int
    member: str

# Model for creating a new TeamMember
class TeamMemberCreate(TeamMemberBase):
    pass

# Model for updating an existing TeamMember
class TeamMemberUpdate(BaseModel):
    owner_id: Optional[int] = None
    member: Optional[str] = None

# Model for returning TeamMember data in responses
class TeamMemberOut(TeamMemberBase):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models