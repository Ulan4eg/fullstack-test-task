from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from enum import Enum

class AlertLevel(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

@dataclass
class Alert:
    """Сущность алерта"""
    id: int
    file_id: UUID
    level: AlertLevel
    message: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        file_id: UUID,
        level: AlertLevel,
        message: str
    ) -> 'Alert':
        """Создание нового алерта"""
        return cls(
            id=0,  # ID будет назначен БД
            file_id=file_id,
            level=level,
            message=message,
            created_at=datetime.utcnow()
        )

    @classmethod
    def create_critical(cls, file_id: UUID, message: str) -> 'Alert':
        """Создание критического алерта"""
        return cls.create(file_id, AlertLevel.CRITICAL, message)

    @classmethod
    def create_warning(cls, file_id: UUID, message: str) -> 'Alert':
        """Создание предупреждения"""
        return cls.create(file_id, AlertLevel.WARNING, message)

    @classmethod
    def create_info(cls, file_id: UUID, message: str) -> 'Alert':
        """Создание информационного алерта"""
        return cls.create(file_id, AlertLevel.INFO, message)