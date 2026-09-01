from abc import ABC, abstractmethod
from typing import Optional, BinaryIO
from uuid import UUID
from pathlib import Path

class FileStorage(ABC):
    """Интерфейс хранилища файлов"""

    @abstractmethod
    async def save(self, file_id: UUID, stored_name: str, content: bytes) -> None:
        """Сохранить файл"""
        pass

    @abstractmethod
    async def get_content(self, file_id: UUID, stored_name: str) -> Optional[bytes]:
        """Получить содержимое файла"""
        pass

    @abstractmethod
    async def get_path(self, file_id: UUID, stored_name: str) -> Path:
        """Получить путь к файлу"""
        pass

    @abstractmethod
    async def delete(self, file_id: UUID, stored_name: str) -> None:
        """Удалить файл"""
        pass

    @abstractmethod
    async def exists(self, file_id: UUID, stored_name: str) -> bool:
        """Проверить существование файла"""
        pass