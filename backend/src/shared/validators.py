from typing import Optional, List
from pathlib import Path
from ..core.config import settings

class FileValidator:
    """Валидатор файлов"""

    @staticmethod
    def validate_title(title: str) -> bool:
        """Проверка названия файла"""
        if not title or not title.strip():
            return False
        if len(title) > 255:
            return False
        # Запрещенные символы в названии
        forbidden = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        return not any(char in title for char in forbidden)

    @staticmethod
    def validate_extension(filename: str) -> bool:
        """Проверка расширения файла"""
        ext = Path(filename).suffix.lower()
        return ext in settings.ALLOWED_EXTENSIONS

    @staticmethod
    def validate_size(size: int) -> bool:
        """Проверка размера файла"""
        return 0 < size <= settings.MAX_FILE_SIZE

    @staticmethod
    def validate_content_type(content_type: Optional[str]) -> bool:
        """Проверка MIME типа"""
        if not content_type:
            return False
        # Базовые разрешенные MIME типы
        allowed = [
            'application/pdf',
            'text/plain',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/png',
            'application/zip',
        ]
        return content_type in allowed

    @classmethod
    def validate_all(cls, filename: str, size: int, content_type: Optional[str] = None) -> List[str]:
        """Полная валидация файла"""
        errors = []

        if not cls.validate_extension(filename):
            errors.append(f"Extension not allowed. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}")

        if not cls.validate_size(size):
            max_mb = settings.MAX_FILE_SIZE // (1024 * 1024)
            errors.append(f"File too large. Max size: {max_mb} MB")

        if content_type and not cls.validate_content_type(content_type):
            errors.append(f"Content type '{content_type}' not supported")

        return errors