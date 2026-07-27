from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class HabitCreate(BaseModel):
    """Schema for creating a new habit."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the habit.",
        examples=["Morning Workout"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional description or details about the habit.",
        examples=["30 minutes of cardio and stretching"]
    )
    category: str = Field(
        default="General",
        min_length=1,
        max_length=50,
        description="Category tag for organizing habits.",
        examples=["Fitness"]
    )
    frequency: str = Field(
        default="daily",
        description="Habit recurrence frequency ('daily', 'weekly', 'monthly').",
        examples=["daily"]
    )

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, value: str) -> str:
        allowed = {"daily", "weekly", "monthly"}
        clean_val = value.lower().strip()
        if clean_val not in allowed:
            raise ValueError(f"Frequency must be one of: {', '.join(allowed)}")
        return clean_val


class HabitUpdate(BaseModel):
    """Schema for updating an existing habit (allows partial updates)."""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated name of the habit.",
        examples=["Morning HIIT Workout"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Updated habit description.",
        examples=["45 minutes high intensity interval training"]
    )
    category: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Updated category tag.",
        examples=["Fitness"]
    )
    frequency: Optional[str] = Field(
        default=None,
        description="Updated recurrence frequency ('daily', 'weekly', 'monthly').",
        examples=["daily"]
    )

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        allowed = {"daily", "weekly", "monthly"}
        clean_val = value.lower().strip()
        if clean_val not in allowed:
            raise ValueError(f"Frequency must be one of: {', '.join(allowed)}")
        return clean_val


class HabitResponse(BaseModel):
    """Public habit response model."""
    id: int = Field(..., description="Unique habit primary key identifier.")
    title: str = Field(..., description="Name of the habit.")
    description: Optional[str] = Field(default=None, description="Detailed habit description.")
    category: str = Field(..., description="Habit category tag.")
    frequency: str = Field(..., description="Recurrence frequency ('daily', 'weekly', 'monthly').")
    created_at: datetime = Field(..., description="Timestamp when habit was created.")

    class Config:
        from_attributes = True
