from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.user_crud import (
    get_user_by_email,
    get_user_by_username,
    create_user,
)
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from app.schemas.auth_schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.models.user import User


def register_new_user(db: Session, user_data: UserRegister) -> UserResponse:
    """
    Business logic for user registration:
    1. Check for duplicate email
    2. Check for duplicate username
    3. Hash user password
    4. Persist user in database
    """
    # 1. Check duplicate email
    if get_user_by_email(db, email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists.",
        )

    # 2. Check duplicate username
    if get_user_by_username(db, username=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken. Please choose another.",
        )

    # 3. Hash password
    hashed_pwd = hash_password(user_data.password)

    # 4. Save user
    new_user = create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_pwd,
    )

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account.",
        )

    return UserResponse.model_validate(new_user)


def authenticate_user(db: Session, credentials: UserLogin) -> TokenResponse:
    """
    Business logic for user authentication:
    1. Retrieve user by email
    2. Verify hashed password
    3. Generate and return JWT access token
    """
    user = get_user_by_email(db, email=credentials.email)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")
