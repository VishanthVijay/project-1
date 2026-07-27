from datetime import date
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.habit_crud import get_habit_by_id
from app.crud.habit_log_crud import (
    create_habit_log,
    get_habit_log_by_id,
    get_habit_log_by_date,
    delete_habit_log,
    get_habit_logs,
    count_habit_completed_days,
    get_latest_habit_log,
)
from app.schemas.habit_log_schemas import (
    HabitCompletionCreate,
    HabitLogResponse,
    HabitStatsResponse,
)
from app.models.user import User
from app.utils.logger import logger
from app.utils.streak_calculator import calculate_streaks


def _verify_habit_ownership(db: Session, current_user: User, habit_id: int):
    """
    Helper to verify that habit exists and belongs to current_user.
    Returns HTTP 404 if missing or unauthorized to prevent resource existence leaks.
    """
    habit = get_habit_by_id(db=db, habit_id=habit_id)
    if not habit or habit.user_id != current_user.id:
        logger.warning(
            f"Unauthorized habit log access attempt for Habit ID {habit_id} by User ID {current_user.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit with ID {habit_id} was not found.",
        )
    return habit


def mark_habit_completed(
    db: Session, current_user: User, habit_id: int, completion_in: HabitCompletionCreate
) -> HabitLogResponse:
    """
    Marks a habit as completed for a given date (defaults to today).
    Prevents duplicate completion entries for the same date.
    """
    _verify_habit_ownership(db, current_user, habit_id)

    target_date = completion_in.completed_date or date.today()

    # Prevent Duplicate Entry for Same Date
    existing_log = get_habit_log_by_date(db, habit_id=habit_id, completed_date=target_date)
    if existing_log:
        logger.warning(
            f"Duplicate completion attempt for Habit ID {habit_id} on date {target_date}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Habit is already marked as completed for date {target_date}.",
        )

    log_entry = create_habit_log(db=db, habit_id=habit_id, completed_date=target_date)
    logger.info(
        f"Habit ID {habit_id} completed on {target_date} by User ID {current_user.id}"
    )
    return HabitLogResponse.model_validate(log_entry)


def remove_habit_completion(
    db: Session, current_user: User, habit_id: int, log_id: int
) -> bool:
    """
    Removes a habit completion record by log ID.
    Validates ownership and verifies that log_id belongs to habit_id.
    """
    _verify_habit_ownership(db, current_user, habit_id)

    log_entry = get_habit_log_by_id(db, log_id=log_id)
    if not log_entry or log_entry.habit_id != habit_id:
        logger.warning(
            f"Invalid or unauthorized log delete attempt for Log ID {log_id} on Habit ID {habit_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Habit log entry with ID {log_id} was not found for this habit.",
        )

    delete_habit_log(db=db, log_id=log_id)
    logger.info(
        f"Habit log ID {log_id} removed from Habit ID {habit_id} by User ID {current_user.id}"
    )
    return True


def get_habit_completion_history(
    db: Session, current_user: User, habit_id: int
) -> List[HabitLogResponse]:
    """
    Retrieves completion history for a habit ordered by date (newest first).
    """
    _verify_habit_ownership(db, current_user, habit_id)
    logs = get_habit_logs(db=db, habit_id=habit_id)
    return [HabitLogResponse.model_validate(log) for log in logs]


def get_habit_statistics(
    db: Session, current_user: User, habit_id: int
) -> HabitStatsResponse:
    """
    Calculates streak statistics:
    - current_streak
    - longest_streak
    - total_completed_days
    - last_completed_date
    """
    _verify_habit_ownership(db, current_user, habit_id)

    logs = get_habit_logs(db=db, habit_id=habit_id)
    completion_dates = [log.completed_date for log in logs if log.completed]

    current_streak, longest_streak = calculate_streaks(completion_dates)
    total_days = len(completion_dates)

    latest_log = get_latest_habit_log(db=db, habit_id=habit_id)
    last_date = latest_log.completed_date if latest_log else None

    logger.info(
        f"Stats calculated for Habit ID {habit_id}: current_streak={current_streak}, longest_streak={longest_streak}, total={total_days}"
    )

    return HabitStatsResponse(
        habit_id=habit_id,
        current_streak=current_streak,
        longest_streak=longest_streak,
        total_completed_days=total_days,
        last_completed_date=last_date,
    )
