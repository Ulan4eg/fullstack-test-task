from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from ...core.database import Base
from ...domain.entities.alert import Alert, AlertLevel

class AlertModel(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(36), ForeignKey("files.id"), nullable=False)
    level: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    def to_domain(self) -> Alert:
        """Конвертация из ORM модели в доменную сущность"""
        return Alert(
            id=self.id,
            file_id=UUID(self.file_id),
            level=AlertLevel(self.level),
            message=self.message,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, alert: Alert) -> 'AlertModel':
        """Конвертация из доменной сущности в ORM модель"""
        return cls(
            id=alert.id,
            file_id=str(alert.file_id),
            level=alert.level.value,
            message=alert.message,
            created_at=alert.created_at,
        )