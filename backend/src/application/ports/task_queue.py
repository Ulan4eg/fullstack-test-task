from abc import ABC, abstractmethod
from uuid import UUID
from typing import Any, Dict

class TaskQueue(ABC):
    """Интерфейс очереди задач"""

    @abstractmethod
    async def enqueue_scan(self, file_id: UUID) -> str:
        """Добавить задачу сканирования"""
        pass

    @abstractmethod
    async def enqueue_metadata_extraction(self, file_id: UUID) -> str:
        """Добавить задачу извлечения метаданных"""
        pass

    @abstractmethod
    async def enqueue_alert(self, file_id: UUID) -> str:
        """Добавить задачу создания алерта"""
        pass

    @abstractmethod
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Получить статус задачи"""
        pass