from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.habit import Habit


def create_habit(
    db: Session,
    user_id: int,
    title: str,
    description: Optional[str] = None,
    category: str = "General",
    frequency: str = "daily",
) -> Optional[Habit]:
    """
    Creates a new habit linked to a specific user_id.

    SQL Equivalent:
    INSERT INTO habits (user_id, title, description, category, frequency)
    VALUES (...);
    """
    habit = Habit(
        user_id=user_id,
        title=title,
        description=description,
        category=category,
        frequency=frequency,
    )
    try:
        db.add(habit)
        db.commit()
        db.refresh(habit)
        return habit
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[Error creating habit]: {e}")
        return None


def get_habit_by_id(db: Session, habit_id: int) -> Optional[Habit]:
    """
    Retrieves a single habit by primary key ID.

    SQL Equivalent:
    SELECT * FROM habits WHERE id = habit_id LIMIT 1;
    """
    return db.query(Habit).filter(Habit.id == habit_id).first()


def get_user_habits(db: Session, user_id: int) -> List[Habit]:
    """
    Retrieves all habits belonging to a specific user.

    SQL Equivalent:
    SELECT * FROM habits WHERE user_id = user_id;
    """
    return db.query(Habit).filter(Habit.user_id == user_id).all()


def update_habit(
    db: Session,
    habit_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    frequency: Optional[str] = None,
) -> Optional[Habit]:
    """
    Updates habit details for the given habit_id.
    """
    habit = get_habit_by_id(db, habit_id)
    if not habit:
        print(f"[Update Failed]: Habit ID {habit_id} not found.")
        return None
    try:
        if title is not None:
            habit.title = title
        if description is not None:
            habit.description = description
        if category is not None:
            habit.category = category
        if frequency is not None:
            habit.frequency = frequency
        db.commit()
        db.refresh(habit)
        return habit
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[Error updating habit]: {e}")
        return None


def delete_habit(db: Session, habit_id: int) -> bool:
    """
    Deletes a habit by ID. Cascades automatically delete associated habit logs.

    SQL Equivalent:
    DELETE FROM habits WHERE id = habit_id;
    """
    habit = get_habit_by_id(db, habit_id)
    if not habit:
        print(f"[Delete Failed]: Habit ID {habit_id} not found.")
        return False
    try:
        db.delete(habit)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[Error deleting habit]: {e}")
        return False
