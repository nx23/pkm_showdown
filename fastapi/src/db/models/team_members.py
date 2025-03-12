from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Team_Members(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    member_name: str
    owner: Optional["Users"] = Relationship(back_populates="team_members")  # type: ignore

    def __repr__(self) -> str:
        return f"<TeamMembers(id={self.id}, member_name={self.member_name})>"
