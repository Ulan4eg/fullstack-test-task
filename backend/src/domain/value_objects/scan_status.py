from enum import Enum

class ScanStatus(str, Enum):
    """Статус сканирования файла"""
    CLEAN = "clean"
    SUSPICIOUS = "suspicious"
    PENDING = "pending"
    FAILED = "failed"

    @classmethod
    def from_string(cls, value: str) -> 'ScanStatus':
        """Создание из строки"""
        try:
            return cls(value.lower())
        except ValueError:
            return cls.PENDING

    @property
    def is_clean(self) -> bool:
        return self == ScanStatus.CLEAN

    @property
    def is_suspicious(self) -> bool:
        return self == ScanStatus.SUSPICIOUS

    @property
    def is_pending(self) -> bool:
        return self == ScanStatus.PENDING

    @property
    def is_failed(self) -> bool:
        return self == ScanStatus.FAILED

    @property
    def requires_attention(self) -> bool:
        return self in (ScanStatus.SUSPICIOUS, ScanStatus.FAILED)