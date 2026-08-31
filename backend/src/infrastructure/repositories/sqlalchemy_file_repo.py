from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...application.ports.file_repository import FileRepository
from ...domain.entities.file import File
from ..models.file_model import FileModel

class SQLAlchemyFileRepository(FileRepository):
    """Реализация репозитория через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, file: File) -> File:
        model = FileModel.from_domain(file)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()

    async def get_by_id(self, file_id: UUID) -> Optional[File]:
        result = await self.session.execute(
            select(FileModel).where(FileModel.id == str(file_id))
        )
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[File]:
        result = await self.session.execute(
            select(FileModel)
            .order_by(FileModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return [model.to_domain() for model in result.scalars().all()]

    async def update(self, file: File) -> File:
        model = await self.session.get(FileModel, str(file.id))
        if model:
            model.update_from_domain(file)
            await self.session.commit()
            await self.session.refresh(model)
            return model.to_domain()
        raise ValueError(f"File with id {file.id} not found")

    async def delete(self, file_id: UUID) -> None:
        model = await self.session.get(FileModel, str(file_id))
        if model:
            await self.session.delete(model)
            await self.session.commit()