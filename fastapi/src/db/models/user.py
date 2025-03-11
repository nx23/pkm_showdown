from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
from .team_members import Team_Members

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str
    password: str
    is_active: bool = True
    team_members: Optional[List[Team_Members]] = Relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, is_active={self.is_active})>"