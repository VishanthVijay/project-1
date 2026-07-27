from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.habit_crud import (
    create_habit,
    get_habit_by_id,
    get_user_habits,
    update_habit,
    delete_habit,
)
from app.schemas.habit_schemas import HabitCreate, HabitUpdate, HabitResponse
from app.models.user import User
from app.utils.logger import logger


def create_user_habit(
    db: Session, current_user: User, habit_in: HabitCreate
) -> HabitResponse:
    """
    Business logic for habit creation:
    1. Associates habit with authenticated current_user.id
    2. Logs habit creation
    3. Persists habit in DB via CRUD layer
    """
    logger.info(
        f"Creating habit '{habit_in.title}' for User ID: {current_user.id}"
    )
    habit = create_habit(
        db=db,
        user_id=current_user.id,
        title=habit_in.title,
        description=habit_in.description,
        category=habit_in.category,
        frequency=habit_in.frequency,
    )
    if not habit:
        logger.error(f"Failed to create habit for User ID: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create habit.",
        )
    return HabitResponse.model_validate(habit)


def get_user_habits_list(db: Session, current_user: User) -> List[HabitResponse]:
    """
    Retrieves all habits belonging to the authenticated user ordered by creation date.
    Does not return habits belonging to other users.
    """
    logger.info(f"Fetching habits for User ID: {current_user.id}")
    habits = get_user_habits(db=db, user_id=current_user.id)
    return [HabitResponse.model_validate(h) for h in habits]


def get_user_habit_by_id(
    db: Session, current_user: User, habit_id: int
) -> HabitResponse:
    """
    Retrieves a single habit by ID.
    Enforces ownership validation: If habit does not exist or belongs to another user,
    returns HTTP 404 Not Found to prevent resource existence leaking.
    """
    habit = get_habit_by_id(db=db, habit_id=habit_id)
    if not habit or habit.user_id != current_user.id:
        logger.warning(
            f"Unauthorized or invalid access attempt for Habit ID {habit_id} by User ID {current_user.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with ID {habit_id} was not found.",
        )
    return HabitResponse.model_validate(habit)


def update_user_habit(
    db: Session, current_user: User, habit_id: int, habit_in: HabitUpdate
) -> HabitResponse:
    """
    Updates a habit belonging to the current user (supports partial updates).
    Enforces ownership validation before executing updates.
    """
    # 1. Ownership check
    habit = get_habit_by_id(db=db, habit_id=habit_id)
    if not habit or habit.user_id != current_user.id:
        logger.warning(
            f"Unauthorized update attempt on Habit ID {habit_id} by User ID {current_user.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with ID {habit_id} was not found.",
        )

    # 2. Update via CRUD layer
    updated = update_habit(
        db=db,
        habit_id=habit_id,
        title=habit_in.title,
        description=habit_in.description,
        category=habit_in.category,
        frequency=habit_in.frequency,
    )
    logger.info(f"Habit ID {habit_id} updated by User ID {current_user.id}")
    return HabitResponse.model_validate(updated)


def delete_user_habit(db: Session, current_user: User, habit_id: int) -> bool:
    """
    Deletes a habit belonging to the current user.
    Cascade deletion automatically removes all associated daily habit logs.
    Enforces ownership validation.
    """
    habit = get_habit_by_id(db=db, habit_id=habit_id)
    if not habit or habit.user_id != current_user.id:
        logger.warning(
            f"Unauthorized delete attempt on Habit ID {habit_id} by User ID {current_user.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with ID {habit_id} was not found.",
        )

    success = delete_habit(db=db, habit_id=habit_id)
    logger.info(f"Habit ID {habit_id} deleted by User ID {current_user.id}")
    return success
