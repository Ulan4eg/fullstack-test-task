from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID
from ....domain.entities.alert import Alert, AlertLevel

class AlertResponse(BaseModel):
    """Ответ с информацией об алерте"""
    id: int = Field(..., description="ID алерта")
    file_id: UUID = Field(..., description="ID файла")
    level: str = Field(..., description="Уровень алерта")
    level_label: str = Field(..., description="Название уровня")
    message: str = Field(..., description="Сообщение")
    created_at: datetime = Field(..., description="Дата создания")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "file_id": "123e4567-e89b-12d3-a456-426614174000",
                "level": "warning",
                "level_label": "Предупреждение",
                "message": "File requires attention: suspicious extension .exe",
                "created_at": "2024-01-01T12:05:00"
            }
        }
    )

    @classmethod
    def from_domain(cls, alert: Alert) -> 'AlertResponse':
        """Создание ответа из доменной сущности"""
        level_labels = {
            AlertLevel.CRITICAL: "Критический",
            AlertLevel.WARNING: "Предупреждение",
            AlertLevel.INFO: "Информация",
        }
        return cls(
            id=alert.id,
            file_id=alert.file_id,
            level=alert.level.value,
            level_label=level_labels.get(alert.level, alert.level.value),
            message=alert.message,
            created_at=alert.created_at,
        )