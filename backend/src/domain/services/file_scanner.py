from pathlib import Path
from typing import List, Tuple
from ..entities.file import File
from ..value_objects.scan_status import ScanStatus
from ...core.config import settings

class FileScanner:
    """Доменный сервис для сканирования файлов"""

    SUSPICIOUS_EXTENSIONS = {'.exe', '.bat', '.cmd', '.sh', '.js'}
    MAX_FILE_SIZE = settings.MAX_FILE_SIZE

    @classmethod
    def scan(cls, file: File, file_path: Path) -> Tuple[ScanStatus, str, bool]:
        """Сканирует файл и возвращает статус, детали и флаг внимания"""
        reasons: List[str] = []

        # Проверка расширения
        extension = Path(file.original_name).suffix.lower()
        if extension in cls.SUSPICIOUS_EXTENSIONS:
            reasons.append(f"suspicious extension {extension}")

        # Проверка размера
        if file.size.bytes > cls.MAX_FILE_SIZE:
            reasons.append(f"file exceeds {cls.MAX_FILE_SIZE // (1024*1024)} MB limit")

        # Проверка MIME типа для PDF
        if extension == '.pdf' and file.mime_type not in {
            'application/pdf', 'application/octet-stream'
        }:
            reasons.append("pdf extension does not match mime type")

        # Проверка на вредоносные паттерны (пример)
        if extension == '.txt' and file_path.exists():
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            if any(pattern in content.lower() for pattern in ['eval(', 'exec(', 'system(']):
                reasons.append("contains potentially dangerous code patterns")

        if reasons:
            return ScanStatus.SUSPICIOUS, ", ".join(reasons), True

        return ScanStatus.CLEAN, "no threats found", False