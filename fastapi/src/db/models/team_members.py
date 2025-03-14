from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Team_Members(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    name: str = Field(default="MissingNo")
    species: str = Field(default="MissingNo")
    type1: str = Field(default="normal")
    type2: Optional[str] = None
    hp: int = Field(default=0)
    atk: int = Field(default=0)
    df: int = Field(default=0)
    satk: int = Field(default=0)
    sdf: int = Field(default=0)
    spd: int = Field(default=0)
    owner: Optional["Users"] = Relationship(back_populates="team_members")  # type: ignore

    def __repr__(self) -> str:
        return f"<TeamMembers(id={self.id}, name={self.name})>"
