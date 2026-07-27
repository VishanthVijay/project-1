from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.schemas.habit_schemas import HabitCreate, HabitUpdate, HabitResponse
from app.schemas.response_schemas import ApiResponse
from app.services.habit_service import (
    create_user_habit,
    get_user_habits_list,
    get_user_habit_by_id,
    update_user_habit,
    delete_user_habit,
)

router = APIRouter(prefix="/habits", tags=["Habit Management"])


@router.post(
    "",
    response_model=ApiResponse[HabitResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create a new habit",
    description="Creates a new habit associated with the authenticated user. Returns standardized ApiResponse envelope.",
)
def create_habit_endpoint(
    habit_in: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Creates a new habit for current user."""
    habit = create_user_habit(db=db, current_user=current_user, habit_in=habit_in)
    return ApiResponse[HabitResponse](
        success=True,
        message="Habit created successfully.",
        data=habit,
    )


@router.get(
    "",
    response_model=ApiResponse[List[HabitResponse]],
    status_code=status.HTTP_200_OK,
    summary="Get all habits for current user",
    description="Retrieves all habits belonging to the authenticated user ordered by creation date. Does not return habits of other users.",
)
def get_habits_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves all habits belonging to current user."""
    habits = get_user_habits_list(db=db, current_user=current_user)
    return ApiResponse[List[HabitResponse]](
        success=True,
        message="User habits retrieved successfully.",
        data=habits,
    )


@router.get(
    "/{habit_id}",
    response_model=ApiResponse[HabitResponse],
    status_code=status.HTTP_200_OK,
    summary="Get a single habit by ID",
    description="Retrieves details for a specific habit belonging to the current user. Returns HTTP 404 if not found or unauthorized.",
)
def get_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves a single habit by ID if owned by current user."""
    habit = get_user_habit_by_id(db=db, current_user=current_user, habit_id=habit_id)
    return ApiResponse[HabitResponse](
        success=True,
        message="Habit details retrieved successfully.",
        data=habit,
    )


@router.put(
    "/{habit_id}",
    response_model=ApiResponse[HabitResponse],
    status_code=status.HTTP_200_OK,
    summary="Update a habit",
    description="Updates habit title, description, category, or frequency. Only the owner may update the habit.",
)
def update_habit_endpoint(
    habit_id: int,
    habit_in: HabitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Updates an existing habit belonging to current user."""
    updated = update_user_habit(
        db=db, current_user=current_user, habit_id=habit_id, habit_in=habit_in
    )
    return ApiResponse[HabitResponse](
        success=True,
        message="Habit updated successfully.",
        data=updated,
    )


@router.delete(
    "/{habit_id}",
    response_model=ApiResponse[dict],
    status_code=status.HTTP_200_OK,
    summary="Delete a habit",
    description="Deletes a habit. Cascade automatically removes all associated habit completion logs.",
)
def delete_habit_endpoint(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Deletes a habit belonging to current user."""
    delete_user_habit(db=db, current_user=current_user, habit_id=habit_id)
    return ApiResponse[dict](
        success=True,
        message=f"Habit with ID {habit_id} deleted successfully.",
        data={"deleted_habit_id": habit_id},
    )
