from typing import BinaryIO
from uuid import UUID
from ...domain.entities.file import File
from ...domain.services.file_scanner import FileScanner
from ...domain.value_objects.scan_status import ScanStatus
from ..ports.file_repository import FileRepository
from ..ports.file_storage import FileStorage
from ..ports.task_queue import TaskQueue
from ...core.exceptions import FileValidationError

class FileUploadUseCase:
    """Use case для загрузки файла"""

    def __init__(
        self,
        file_repository: FileRepository,
        file_storage: FileStorage,
        task_queue: TaskQueue
    ):
        self.file_repository = file_repository
        self.file_storage = file_storage
        self.task_queue = task_queue

    async def execute(
        self,
        title: str,
        original_name: str,
        content: bytes,
        mime_type: str
    ) -> File:
        """Загружает файл и запускает асинхронную обработку"""

        # Валидация
        if not title or not title.strip():
            raise FileValidationError("Title cannot be empty")

        if not content:
            raise FileValidationError("File content is empty")

        # Создание сущности
        stored_name = f"{uuid4()}{Path(original_name).suffix}"
        file = File.create(
            title=title,
            original_name=original_name,
            stored_name=stored_name,
            mime_type=mime_type,
            size=len(content)
        )

        # Сохранение файла
        await self.file_storage.save(file.id, stored_name, content)

        # Сохранение в БД
        saved_file = await self.file_repository.save(file)

        # Запуск асинхронной обработки
        await self.task_queue.enqueue_scan(saved_file.id)

        return saved_file