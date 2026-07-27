from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ApiResponse(BaseModel, Generic[DataT]):
    """
    Standardized Success API Response Envelope.

    Structure:
    {
        "success": true,
        "message": "Operation completed successfully",
        "data": { ... }
    }
    """
    success: bool = Field(default=True, description="Indicates if request succeeded")
    message: str = Field(..., description="Human-readable summary message")
    data: Optional[DataT] = Field(default=None, description="Response payload data")


class ApiErrorResponse(BaseModel):
    """
    Standardized Error API Response Envelope.

    Structure:
    {
        "success": false,
        "message": "Something went wrong",
        "errors": { ... }
    }
    """
    success: bool = Field(default=False, description="Indicates request failed")
    message: str = Field(..., description="Human-readable error description")
    errors: Optional[Any] = Field(default=None, description="Detailed field-level or system error details")
