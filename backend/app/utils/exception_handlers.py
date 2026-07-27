from fastapi import Request, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.response_schemas import ApiErrorResponse
from app.utils.logger import logger


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handles HTTPExceptions raised anywhere in the application.
    Returns standardized ApiErrorResponse envelope.
    """
    logger.warning(
        f"HTTPException [{exc.status_code}] on {request.method} {request.url.path}: {exc.detail}"
    )
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=exc.status_code,
        content=ApiErrorResponse(
            success=False,
            message=str(exc.detail),
            errors=None,
        ).model_dump(),
        headers=headers,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handles request body validation failures (Pydantic schema errors).
    Returns standardized ApiErrorResponse envelope with field-level details.
    """
    logger.warning(
        f"ValidationError on {request.method} {request.url.path}: {exc.errors()}"
    )
    formatted_errors = [
        {"field": " -> ".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiErrorResponse(
            success=False,
            message="Input validation failed. Please check your request parameters.",
            errors=formatted_errors,
        ).model_dump(),
    )


async def sqlalchemy_exception_handler(
    request: Request, exc: SQLAlchemyError
) -> JSONResponse:
    """
    Handles database operations failures (e.g., connection lost, integrity error).
    """
    logger.error(
        f"Database Error on {request.method} {request.url.path}: {exc}", exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiErrorResponse(
            success=False,
            message="A database operation error occurred. Please try again later.",
            errors=str(exc) if exc else None,
        ).model_dump(),
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all exception handler for unexpected server errors.
    Prevents raw tracebacks from exposing internal details to clients.
    """
    logger.error(
        f"Unhandled Server Error on {request.method} {request.url.path}: {exc}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiErrorResponse(
            success=False,
            message="An unexpected internal server error occurred.",
            errors=str(exc),
        ).model_dump(),
    )
