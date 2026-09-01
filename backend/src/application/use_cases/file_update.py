from uuid import UUID
from ...domain.entities.file import File
from ..ports.file_repository import FileRepository
from ...core.exceptions import FileNotFoundError, FileValidationError

class FileUpdateUseCase:
    """Use case для обновления файла"""

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def execute(self, file_id: UUID, new_title: str) -> File:
        """Обновление названия файла"""

        # Валидация
        if not new_title or not new_title.strip():
            raise FileValidationError("Title cannot be empty")

        if len(new_title) > 255:
            raise FileValidationError("Title too long (max 255 characters)")

        # Получение файла
        file = await self.file_repository.get_by_id(file_id)
        if not file:
            raise FileNotFoundError(str(file_id))

        # Обновление
        file.update_title(new_title)

        # Сохранение
        return await self.file_repository.update(file)