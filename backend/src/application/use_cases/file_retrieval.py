from typing import List, Optional
from uuid import UUID
from ...domain.entities.file import File
from ..ports.file_repository import FileRepository

class FileRetrievalUseCase:
    """Use case для получения файлов"""

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def get_by_id(self, file_id: UUID) -> Optional[File]:
        """Получение файла по ID"""
        return await self.file_repository.get_by_id(file_id)

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[File]:
        """Получение всех файлов с пагинацией"""
        return await self.file_repository.get_all(limit, offset)