from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .user import User

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    member: Mapped[str] = mapped_column(String)

    owner: Mapped["User"] = relationship("User", back_populates="teams")