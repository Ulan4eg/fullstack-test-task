from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID
from ...domain.entities.file import File

class FileRepository(ABC):
    """Интерфейс репозитория для работы с файлами"""

    @abstractmethod
    async def save(self, file: File) -> File:
        """Сохранить файл"""
        pass

    @abstractmethod
    async def get_by_id(self, file_id: UUID) -> Optional[File]:
        """Получить файл по ID"""
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[File]:
        """Получить все файлы с пагинацией"""
        pass

    @abstractmethod
    async def update(self, file: File) -> File:
        """Обновить файл"""
        pass

    @abstractmethod
    async def delete(self, file_id: UUID) -> None:
        """Удалить файл"""
        pass