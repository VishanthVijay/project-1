import logging
from app.database import Base, engine
# Importing models registers them with Base.metadata
import app.models  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db():
    """
    Creates all database tables registered under SQLAlchemy Base metadata.
    Does not drop existing tables; only creates missing ones.
    """
    logger.info("Creating database tables if they do not exist...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully!")


if __name__ == "__main__":
    init_db()
