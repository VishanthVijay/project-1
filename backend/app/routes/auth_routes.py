from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth_schemas import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserResponse,
)
from app.schemas.response_schemas import ApiResponse
from app.auth.auth_service import register_new_user, authenticate_user
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    description="Registers a new user with a unique username, valid email, and password. Returns standardized ApiResponse envelope.",
)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Registers a new user account.
    """
    logger.info(f"Registration request for email: '{user_data.email}'")
    user_response = register_new_user(db, user_data)
    return ApiResponse[UserResponse](
        success=True,
        message="User account registered successfully.",
        data=user_response,
    )


@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and obtain JWT access token",
    description="Authenticates user credentials (email & password) and returns a signed JWT access token in standardized envelope.",
)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates user and returns JWT token.
    """
    logger.info(f"Login request for email: '{credentials.email}'")
    token_response = authenticate_user(db, credentials)
    return ApiResponse[TokenResponse](
        success=True,
        message="Authentication successful.",
        data=token_response,
    )


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user profile",
    description="Protected endpoint requiring valid JWT Bearer token. Returns authenticated user profile details in standardized envelope.",
)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Returns profile information of the current logged-in user.
    """
    logger.info(f"Profile requested by authenticated User ID: {current_user.id}")
    user_response = UserResponse.model_validate(current_user)
    return ApiResponse[UserResponse](
        success=True,
        message="User profile retrieved successfully.",
        data=user_response,
    )
