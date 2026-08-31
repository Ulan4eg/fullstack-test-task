from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.logging import logger
from src.presentation.api.v1.router import router as api_router
from src.presentation.middlewares.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from src.presentation.middlewares.logging_middleware import LoggingMiddleware
from src.core.exceptions import AppException
from fastapi.exceptions import RequestValidationError

# Создание приложения
app = FastAPI(
    title="File Manager API",
    description="API для управления файлами с асинхронной обработкой",
    version="1.0.0",
    debug=settings.DEBUG,
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list if not settings.is_development else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Добавление middleware для логирования
app.add_middleware(LoggingMiddleware)

# Регистрация обработчиков исключений
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Регистрация роутеров
app.include_router(api_router)

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "name": "File Manager API",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )