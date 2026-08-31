from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Union
from ...core.exceptions import AppException

async def app_exception_handler(request: Request, exc: AppException):
    """Обработчик кастомных исключений приложения"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details,
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработчик ошибок валидации Pydantic"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": {
                "errors": errors
            }
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Обработчик всех остальных исключений"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "details": {
                "message": str(exc) if __debug__ else "An unexpected error occurred"
            }
        }
    )