from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables (.env).
    Pydantic handles type validation and defaults.
    """
    APP_NAME: str = "Habit Tracker API"
    DEBUG: bool = True

    # Database
    DATABASE_URL: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "habit_tracker"

    # JWT Authentication
    SECRET_KEY: str = "change_this_to_a_long_random_secret_string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Shared global instance used across the app
settings = Settings()
