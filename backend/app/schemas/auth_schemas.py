from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration request payload."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Unique username containing letters, numbers, underscores, or hyphens.",
        examples=["johndoe"]
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address used for login and notifications.",
        examples=["john@example.com"]
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Password (minimum 6 characters).",
        examples=["secret123"]
    )


class UserLogin(BaseModel):
    """Schema for user login request payload."""
    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["john@example.com"]
    )
    password: str = Field(
        ...,
        min_length=1,
        description="User password.",
        examples=["secret123"]
    )


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str = Field(..., description="JWT bearer access token string.")
    token_type: str = Field(default="bearer", description="Token scheme type.")


class UserResponse(BaseModel):
    """Public user profile model (omits sensitive password hash)."""
    id: int = Field(..., description="Unique user identifier.")
    username: str = Field(..., description="User's unique username.")
    email: EmailStr = Field(..., description="User's email address.")
    created_at: datetime = Field(..., description="Timestamp of user account creation.")

    class Config:
        from_attributes = True
