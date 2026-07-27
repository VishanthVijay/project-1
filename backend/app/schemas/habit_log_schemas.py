from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class HabitCompletionCreate(BaseModel):
    """Schema for completing a habit on a specific date."""
    completed_date: Optional[date] = Field(
        default=None,
        description="Calendar date (YYYY-MM-DD) when habit was completed. Defaults to today's date if omitted.",
        examples=["2026-07-27"]
    )


class HabitLogResponse(BaseModel):
    """Public habit completion log record response model."""
    id: int = Field(..., description="Unique habit log record identifier.")
    habit_id: int = Field(..., description="Parent habit identifier.")
    completed_date: date = Field(..., description="Completion date.")
    completed: bool = Field(default=True, description="Completion status flag.")

    class Config:
        from_attributes = True


class HabitStatsResponse(BaseModel):
    """Analytics and streak statistics response for a habit."""
    habit_id: int = Field(..., description="Parent habit identifier.")
    current_streak: int = Field(..., description="Current active consecutive day streak.")
    longest_streak: int = Field(..., description="Longest historical consecutive day streak.")
    total_completed_days: int = Field(..., description="Total number of completion days logged.")
    last_completed_date: Optional[date] = Field(default=None, description="Most recent completion date.")
