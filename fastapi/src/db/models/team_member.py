from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class TeamMember(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    member_name: str

    def __repr__(self) -> str:
        return f"<TeamMembers(id={self.id}, member_name={self.member_name})>"

