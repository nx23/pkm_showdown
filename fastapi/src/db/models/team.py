from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .base import Base

class TeamMembers(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    member_name: Mapped[str] = mapped_column(String)

    owner: Mapped["User"] = relationship("User", back_populates="team_members")

    def __repr__(self) -> str:
        return f"<TeamMembers(id={self.id}, member_name={self.member_name})>"

from .user import User  # Import at the end to avoid circular import