from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .team import Team

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    teams: Mapped[list["Team"]] = relationship("Team", back_populates="owner")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, is_active={self.is_active})>"