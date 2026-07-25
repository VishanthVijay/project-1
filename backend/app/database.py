from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite database file. It will be created automatically when the app starts.
DATABASE_URL = "sqlite:///./habit_tracker.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required by SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class inherited by all database models."""


def get_db():
    """Provide a database session to FastAPI endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
