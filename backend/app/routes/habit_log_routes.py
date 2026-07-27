from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.habit_log_schemas import (
    HabitCompletionCreate,
    HabitLogResponse,
    HabitStatsResponse,
)
from app.schemas.response_schemas import ApiResponse
from app.services.habit_log_service import (
    mark_habit_completed,
    remove_habit_completion,
    get_habit_completion_history,
    get_habit_statistics,
)

router = APIRouter(prefix="/habits", tags=["Habit Completion & Streaks"])


@router.post(
    "/{habit_id}/complete",
    response_model=ApiResponse[HabitLogResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Mark habit completed",
    description="Marks habit completed for a date (defaults to today). Prevents duplicate entries for the same date.",
)
def complete_habit_endpoint(
    habit_id: int,
    completion_in: HabitCompletionCreate = HabitCompletionCreate(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Marks a habit completed for a specific date."""
    log_entry = mark_habit_completed(
        db=db, current_user=current_user, habit_id=habit_id, completion_in=completion_in
    )
    return ApiResponse[HabitLogResponse](
        success=True,
        message="Habit marked as completed successfully.",
        data=log_entry,
    )


@router.delete(
    "/{habit_id}/complete/{log_id}",
    response_model=ApiResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Remove a completion record",
    description="Deletes a completion log record by log ID. Requires habit ownership.",
)
def remove_completion_endpoint(
    habit_id: int,
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Removes a habit completion record."""
    remove_habit_completion(
        db=db, current_user=current_user, habit_id=habit_id, log_id=log_id
    )
    return ApiResponse[dict](
        success=True,
        message=f"Habit completion log ID {log_id} removed successfully.",
        data={"removed_log_id": log_id, "habit_id": habit_id},
    )


@router.get(
    "/{habit_id}/history",
    response_model=ApiResponse[List[HabitLogResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get habit completion history",
    description="Retrieves all completion logs for a habit ordered by date (newest first). Requires habit ownership.",
)
def get_habit_history_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves completion history for a habit."""
    history = get_habit_completion_history(
        db=db, current_user=current_user, habit_id=habit_id
    )
    return ApiResponse[List[HabitLogResponse]](
        success=True,
        message="Habit completion history retrieved successfully.",
        data=history,
    )


@router.get(
    "/{habit_id}/stats",
    response_model=ApiResponse[HabitStatsResponse],
    status_code=status.HTTP_200_OK,
    summary="Get habit streak statistics",
    description="Calculates current streak, longest streak, total completed days, and last completed date. Requires habit ownership.",
)
def get_habit_stats_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Calculates streak statistics for a habit."""
    stats = get_habit_statistics(
        db=db, current_user=current_user, habit_id=habit_id
    )
    return ApiResponse[HabitStatsResponse](
        success=True,
        message="Habit statistics calculated successfully.",
        data=stats,
    )
