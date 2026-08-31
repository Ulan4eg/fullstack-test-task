from typing import Optional, List
from uuid import UUID
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from ...application.ports.alert_repository import AlertRepository
from ...domain.entities.alert import Alert
from ..models.alert_model import AlertModel

class SQLAlchemyAlertRepository(AlertRepository):
    """Реализация репозитория алертов через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, alert: Alert) -> Alert:
        """Сохранить алерт"""
        model = AlertModel.from_domain(alert)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()

    async def get_by_id(self, alert_id: int) -> Optional[Alert]:
        """Получить алерт по ID"""
        model = await self.session.get(AlertModel, alert_id)
        return model.to_domain() if model else None

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[Alert]:
        """Получить все алерты с пагинацией"""
        result = await self.session.execute(
            select(AlertModel)
            .order_by(desc(AlertModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [model.to_domain() for model in result.scalars().all()]

    async def get_by_file(
        self,
        file_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Alert]:
        """Получить алерты по файлу"""
        result = await self.session.execute(
            select(AlertModel)
            .where(AlertModel.file_id == str(file_id))
            .order_by(desc(AlertModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        return [model.to_domain() for model in result.scalars().all()]