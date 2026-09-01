import logging
from typing import Optional
from ..core.logging import logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Получение логгера с именем"""
    if name:
        return logger.getChild(name)
    return logger

def log_function_call(func):
    """Декоратор для логирования вызовов функций"""
    async def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = await func(*args, **kwargs)
            logger.debug(f"Function {func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {func.__name__} failed: {str(e)}")
            raise
    return wrapper