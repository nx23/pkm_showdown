from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str
    password: str
    is_active: bool = True

    team_members: Optional[list[TeamMembers]] = Relationship(back_populates="owner")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, is_active={self.is_active})>"

# Import at the end to avoid circular import
from .team import TeamMembers  # type: ignore