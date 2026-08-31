from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from ...domain.entities.alert import Alert

class AlertRepository(ABC):
    """Интерфейс репозитория алертов"""

    @abstractmethod
    async def save(self, alert: Alert) -> Alert:
        """Сохранить алерт"""
        pass

    @abstractmethod
    async def get_by_id(self, alert_id: int) -> Optional[Alert]:
        """Получить алерт по ID"""
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Alert]:
        """Получить все алерты"""
        pass

    @abstractmethod
    async def get_by_file(
        self,
        file_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Alert]:
        """Получить алерты по файлу"""
        pass