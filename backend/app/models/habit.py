from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class Habit(Base):
    """
    Represents a habit created by a user.

    Fields:
    - id: Unique integer primary key.
    - user_id: Foreign key referencing users.id (who owns this habit).
    - title: Short name of the habit (e.g., 'Morning Meditation').
    - description: Optional detailed description.
    - category: Category tag (e.g., 'Health', 'Fitness', 'Study', 'Productivity').
    - frequency: How often the habit should occur (default: 'daily').
    - created_at: Timestamp when habit was created.
    """

    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(50), default="General", nullable=False)
    frequency: Mapped[str] = mapped_column(String(20), default="daily", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Many-to-1 Relationship back to User
    user: Mapped["User"] = relationship("User", back_populates="habits")

    # 1-to-Many Relationship: One Habit has Many HabitLogs
    # - cascade="all, delete-orphan": Deleting a habit automatically deletes all its logs
    logs: Mapped[List["HabitLog"]] = relationship(
        "HabitLog", back_populates="habit", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Habit(id={self.id}, title='{self.title}', user_id={self.user_id})>"
