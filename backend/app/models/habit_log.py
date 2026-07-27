from datetime import date
from sqlalchemy import Boolean, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base


class HabitLog(Base):
    """
    Represents a daily completion entry for a specific habit.

    Fields:
    - id: Unique integer primary key.
    - habit_id: Foreign key referencing habits.id.
    - completed_date: The calendar date (YYYY-MM-DD) for this log entry.
    - completed: Boolean flag indicating if completed on that date.
    """

    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    completed_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Ensure a habit has at most ONE log entry per date
    __table_args__ = (
        UniqueConstraint("habit_id", "completed_date", name="uq_habit_date"),
    )

    # Many-to-1 Relationship back to Habit
    habit: Mapped["Habit"] = relationship("Habit", back_populates="logs")

    def __repr__(self) -> str:
        return (
            f"<HabitLog(id={self.id}, habit_id={self.habit_id}, "
            f"date={self.completed_date}, completed={self.completed})>"
        )
