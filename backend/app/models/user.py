from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class User(Base):
    """
    Represents a user account in the application.

    Fields:
    - id: Unique integer primary key.
    - username: Unique display name.
    - email: Unique email address used for login/communication.
    - password_hash: Securely hashed password (never store plain text passwords!).
    - created_at: Timestamp when the user account was created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # 1-to-Many Relationship: One User has Many Habits
    # - back_populates="user": Syncs with Habit.user
    # - cascade="all, delete-orphan": Deleting a user automatically deletes their habits
    habits: Mapped[List["Habit"]] = relationship(
        "Habit", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
