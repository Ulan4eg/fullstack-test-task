import asyncio
from uuid import UUID
from pathlib import Path
from celery import Task
from typing import Optional
from ...core.config import settings
from ...core.database import get_engine
from ...domain.services.file_scanner import FileScanner
from ...domain.services.metadata_extractor import MetadataExtractor
from ...domain.entities.alert import Alert, AlertLevel
from ...infrastructure.repositories.sqlalchemy_file_repo import SQLAlchemyFileRepository
from ...infrastructure.repositories.sqlalchemy_alert_repo import SQLAlchemyAlertRepository
from ...infrastructure.storage.local_file_storage import LocalFileStorage
from .celery_app import celery_app
from sqlalchemy.ext.asyncio import async_sessionmaker

class TaskContext:
    """Контекст для выполнения асинхронных задач в Celery"""
    _engine = None
    _session_maker = None

    @classmethod
    def get_session_maker(cls):
        if not cls._engine:
            cls._engine = get_engine()
            cls._session_maker = async_sessionmaker(
                cls._engine,
                expire_on_commit=False,
            )
        return cls._session_maker

    @classmethod
    async def get_session(cls):
        maker = cls.get_session_maker()
        async with maker() as session:
            yield session

def run_async(coroutine):
    """Запуск асинхронной корутины в синхронном контексте Celery"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def scan_file(self: Task, file_id: str) -> None:
    """Задача сканирования файла с повторными попытками"""
    try:
        run_async(_scan_file_async(file_id))
    except Exception as e:
        self.retry(exc=e)

async def _scan_file_async(file_id: str) -> None:
    """Асинхронное сканирование файла"""
    async for session in TaskContext.get_session():
        file_repo = SQLAlchemyFileRepository(session)
        alert_repo = SQLAlchemyAlertRepository(session)
        storage = LocalFileStorage(settings.STORAGE_DIR)

        # Получение файла
        file = await file_repo.get_by_id(UUID(file_id))
        if not file:
            return

        # Обновление статуса
        file.mark_as_processing()
        await file_repo.update(file)

        try:
            # Получение пути к файлу
            file_path = await storage.get_path(file.id, file.stored_name)

            # Сканирование на угрозы
            scan_status, details, requires_attention = FileScanner.scan(
                file, file_path
            )

            # Обновление результатов сканирования
            file.update_scan_result(scan_status, details, requires_attention)
            await file_repo.update(file)

            # Извлечение метаданных
            metadata = MetadataExtractor.extract(file, file_path)
            file.mark_as_processed(metadata)
            await file_repo.update(file)

            # Создание алерта
            if requires_attention:
                alert = Alert.create_warning(
                    file.id,
                    f"File requires attention: {details}"
                )
            else:
                alert = Alert.create_info(
                    file.id,
                    "File processed successfully"
                )
            await alert_repo.save(alert)

        except Exception as e:
            # Обработка ошибки
            file.mark_as_failed(str(e))
            await file_repo.update(file)

            alert = Alert.create_critical(
                file.id,
                f"File processing failed: {str(e)}"
            )
            await alert_repo.save(alert)
            raise

@celery_app.task(bind=True, max_retries=2)
def extract_file_metadata(self: Task, file_id: str) -> None:
    """Задача извлечения метаданных"""
    try:
        run_async(_extract_metadata_async(file_id))
    except Exception as e:
        self.retry(exc=e)

async def _extract_metadata_async(file_id: str) -> None:
    """Асинхронное извлечение метаданных"""
    async for session in TaskContext.get_session():
        file_repo = SQLAlchemyFileRepository(session)
        storage = LocalFileStorage(settings.STORAGE_DIR)

        file = await file_repo.get_by_id(UUID(file_id))
        if not file:
            return

        try:
            file_path = await storage.get_path(file.id, file.stored_name)
            metadata = MetadataExtractor.extract(file, file_path)

            file.metadata_json = metadata
            file.processing_status = "processed"
            await file_repo.update(file)

        except Exception as e:
            file.mark_as_failed(f"Metadata extraction failed: {str(e)}")
            await file_repo.update(file)
            raise

@celery_app.task
def send_file_alert(file_id: str) -> None:
    """Задача отправки алерта"""
    run_async(_send_alert_async(file_id))

async def _send_alert_async(file_id: str) -> None:
    """Асинхронная отправка алерта"""
    async for session in TaskContext.get_session():
        file_repo = SQLAlchemyFileRepository(session)
        alert_repo = SQLAlchemyAlertRepository(session)

        file = await file_repo.get_by_id(UUID(file_id))
        if not file:
            return

        if file.processing_status == "failed":
            alert = Alert.create_critical(
                file.id,
                "File processing failed"
            )
        elif file.requires_attention:
            alert = Alert.create_warning(
                file.id,
                f"File requires attention: {file.scan_details}"
            )
        else:
            alert = Alert.create_info(
                file.id,
                "File processed successfully"
            )

        await alert_repo.save(alert)