from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    Every model class (e.g. User, Habit) will inherit from this class.
    It maintains the metadata catalog of table definitions.
    """
    pass
