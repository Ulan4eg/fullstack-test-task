from typing import List, Optional
from uuid import UUID
from ...domain.entities.alert import Alert
from ..ports.alert_repository import AlertRepository

class AlertRetrievalUseCase:
    """Use case для получения алертов"""

    def __init__(self, alert_repository: AlertRepository):
        self.alert_repository = alert_repository

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Alert]:
        """Получение всех алертов"""
        return await self.alert_repository.get_all(limit, offset)

    async def get_by_file(
        self,
        file_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Alert]:
        """Получение алертов по файлу"""
        return await self.alert_repository.get_by_file(file_id, limit, offset)
