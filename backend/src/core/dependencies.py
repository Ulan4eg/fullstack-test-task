from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from ..infrastructure.repositories.sqlalchemy_file_repo import SQLAlchemyFileRepository
from ..infrastructure.repositories.sqlalchemy_alert_repo import SQLAlchemyAlertRepository
from ..infrastructure.storage.local_file_storage import LocalFileStorage
from ..infrastructure.task_queue.celery_app import CeleryTaskQueue
from ..application.ports.file_repository import FileRepository
from ..application.ports.alert_repository import AlertRepository
from ..application.ports.file_storage import FileStorage
from ..application.ports.task_queue import TaskQueue
from .database import get_db
from .config import settings

async def get_file_repository(
    session: AsyncSession = Depends(get_db)
) -> FileRepository:
    """Получение репозитория файлов"""
    return SQLAlchemyFileRepository(session)

async def get_alert_repository(
    session: AsyncSession = Depends(get_db)
) -> AlertRepository:
    """Получение репозитория алертов"""
    return SQLAlchemyAlertRepository(session)

async def get_file_storage() -> FileStorage:
    """Получение хранилища файлов"""
    return LocalFileStorage(settings.STORAGE_DIR)

async def get_task_queue() -> TaskQueue:
    """Получение очереди задач"""
    return CeleryTaskQueue()

# Для обратной совместимости с FastAPI Depends
from fastapi import Depends