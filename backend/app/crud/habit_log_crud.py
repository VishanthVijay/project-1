from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog


def create_habit_log(
    db: Session, habit_id: int, completed_date: date, completed: bool = True
) -> HabitLog:
    """Creates a new HabitLog entry in the database."""
    log_entry = HabitLog(
        habit_id=habit_id,
        completed_date=completed_date,
        completed=completed,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry


def get_habit_log_by_id(db: Session, log_id: int) -> Optional[HabitLog]:
    """Finds a HabitLog record by primary key ID."""
    return db.query(HabitLog).filter(HabitLog.id == log_id).first()


def get_habit_log_by_date(
    db: Session, habit_id: int, completed_date: date
) -> Optional[HabitLog]:
    """Finds a HabitLog entry for a specific habit and completed date."""
    return (
        db.query(HabitLog)
        .filter(
            HabitLog.habit_id == habit_id,
            HabitLog.completed_date == completed_date,
        )
        .first()
    )


def delete_habit_log(db: Session, log_id: int) -> bool:
    """Deletes a HabitLog entry by primary key ID."""
    log_entry = get_habit_log_by_id(db, log_id)
    if not log_entry:
        return False
    db.delete(log_entry)
    db.commit()
    return True


def get_habit_logs(db: Session, habit_id: int) -> List[HabitLog]:
    """Retrieves all completion logs for a habit ordered by completed_date descending."""
    return (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit_id)
        .order_by(HabitLog.completed_date.desc())
        .all()
    )


def count_habit_completed_days(db: Session, habit_id: int) -> int:
    """Counts total completed log entries for a habit."""
    return (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit_id, HabitLog.completed == True)
        .count()
    )


def get_latest_habit_log(db: Session, habit_id: int) -> Optional[HabitLog]:
    """Retrieves the most recent completion log for a habit."""
    return (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit_id, HabitLog.completed == True)
        .order_by(HabitLog.completed_date.desc())
        .first()
    )
