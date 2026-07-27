from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

if settings.DATABASE_URL:
    DATABASE_URL = settings.DATABASE_URL
else:
    # Default to local SQLite dev database if explicit DATABASE_URL is not set
    DATABASE_URL = "sqlite:///./habit_tracker.db"

# Engine represents the core DB connection pool
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)

# SessionLocal is the factory for creating database sessions per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    FastAPI dependency that yields a database session per HTTP request.
    Ensures that the connection is automatically closed when request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
