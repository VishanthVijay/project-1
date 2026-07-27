from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User


def create_user(
    db: Session, username: str, email: str, password_hash: str
) -> Optional[User]:
    """
    Creates and persists a new User record.

    SQL Equivalent:
    INSERT INTO users (username, email, password_hash) VALUES (...);
    """
    user = User(username=username, email=email, password_hash=password_hash)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()  # Undo pending transaction on error
        print(f"[Error creating user]: {e}")
        return None


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Retrieves a user by primary key ID.

    SQL Equivalent:
    SELECT * FROM users WHERE id = user_id LIMIT 1;
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieves a user by email address.

    SQL Equivalent:
    SELECT * FROM users WHERE email = email LIMIT 1;
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Retrieves a user by username.

    SQL Equivalent:
    SELECT * FROM users WHERE username = username LIMIT 1;
    """
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session) -> List[User]:
    """
    Lists all registered users.

    SQL Equivalent:
    SELECT * FROM users;
    """
    return db.query(User).all()


def update_username(db: Session, user_id: int, new_username: str) -> Optional[User]:
    """
    Updates the username of a specific user.

    SQL Equivalent:
    UPDATE users SET username = new_username WHERE id = user_id;
    """
    user = get_user_by_id(db, user_id)
    if not user:
        print(f"[Update Failed]: User ID {user_id} not found.")
        return None
    try:
        user.username = new_username
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[Error updating username]: {e}")
        return None


def delete_user(db: Session, user_id: int) -> bool:
    """
    Deletes a user by ID. Cascades automatically delete associated habits and logs.

    SQL Equivalent:
    DELETE FROM users WHERE id = user_id;
    """
    user = get_user_by_id(db, user_id)
    if not user:
        print(f"[Delete Failed]: User ID {user_id} not found.")
        return False
    try:
        db.delete(user)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[Error deleting user]: {e}")
        return False
