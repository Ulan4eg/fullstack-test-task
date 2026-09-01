import logging
import sys
from pathlib import Path
from .config import settings

def setup_logging():
    """Настройка логгирования"""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    # Handler для файла
    handlers = [console_handler]

    if settings.LOG_FILE:
        log_file = Path(settings.LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        handlers.append(file_handler)

    # Настройка корневого логгера
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )

    # Настройка логгеров для библиотек
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("celery").setLevel(logging.INFO)

    return logging.getLogger(__name__)

# Создание логгера
logger = setup_logging()