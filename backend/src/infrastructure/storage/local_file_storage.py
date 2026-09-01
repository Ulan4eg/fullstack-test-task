from pathlib import Path
from typing import Optional
from uuid import UUID
from ...application.ports.file_storage import FileStorage
from ...core.config import settings
from ...core.exceptions import FileStorageError

class LocalFileStorage(FileStorage):
    """Реализация файлового хранилища на локальной файловой системе"""

    def __init__(self, storage_dir: Path = settings.STORAGE_DIR):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _get_file_path(self, file_id: UUID, stored_name: str) -> Path:
        """Получить путь к файлу"""
        # Создаем поддиректорию по первым двум символам ID
        file_id_str = str(file_id)
        sub_dir = file_id_str[:2]
        file_dir = self.storage_dir / sub_dir
        file_dir.mkdir(parents=True, exist_ok=True)
        return file_dir / stored_name

    async def save(self, file_id: UUID, stored_name: str, content: bytes) -> None:
        """Сохранить файл"""
        try:
            file_path = self._get_file_path(file_id, stored_name)
            file_path.write_bytes(content)
        except Exception as e:
            raise FileStorageError(f"Failed to save file: {str(e)}")

    async def get_content(self, file_id: UUID, stored_name: str) -> Optional[bytes]:
        """Получить содержимое файла"""
        try:
            file_path = self._get_file_path(file_id, stored_name)
            if not file_path.exists():
                return None
            return file_path.read_bytes()
        except Exception as e:
            raise FileStorageError(f"Failed to read file: {str(e)}")

    async def get_path(self, file_id: UUID, stored_name: str) -> Path:
        """Получить путь к файлу"""
        file_path = self._get_file_path(file_id, stored_name)
        if not file_path.exists():
            raise FileStorageError(f"File not found: {file_path}")
        return file_path

    async def delete(self, file_id: UUID, stored_name: str) -> None:
        """Удалить файл"""
        try:
            file_path = self._get_file_path(file_id, stored_name)
            if file_path.exists():
                file_path.unlink()
        except Exception as e:
            raise FileStorageError(f"Failed to delete file: {str(e)}")

    async def exists