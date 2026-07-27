from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import Base, engine
from app.routes.auth_routes import router as auth_router
from app.routes.habit_routes import router as habit_router
from app.routes.habit_log_routes import router as habit_log_router
from app.utils.logger import logger
from app.utils.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    global_exception_handler,
)
from app.schemas.response_schemas import ApiResponse
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Logs startup and ensures database tables exist on server launch.
    """
    logger.info(f"Starting {settings.APP_NAME}...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified successfully.")
    except Exception as e:
        logger.warning(f"Database initialization warning on startup: {e}")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-ready Habit Tracker Backend API built with FastAPI, SQLAlchemy, MySQL, and JWT Authentication.",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Global Exception Handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Register Routers
app.include_router(auth_router)
app.include_router(habit_router)
app.include_router(habit_log_router)


@app.get("/", tags=["Health"], response_model=ApiResponse[dict])
def health_check():
    """Health check endpoint to verify server status."""
    return ApiResponse[dict](
        success=True,
        message="Habit Tracker API is operational.",
        data={"status": "ok", "app_name": settings.APP_NAME, "version": "1.0.0"},
    )
