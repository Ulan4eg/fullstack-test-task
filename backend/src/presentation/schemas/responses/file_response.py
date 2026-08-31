from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from ....domain.entities.file import File

class FileResponse(BaseModel):
    """Ответ с информацией о файле"""
    id: UUID = Field(..., description="ID файла")
    title: str = Field(..., description="Название файла")
    original_name: str = Field(..., description="Оригинальное имя файла")
    mime_type: str = Field(..., description="MIME тип")
    size: int = Field(..., description="Размер в байтах")
    size_human: str = Field(..., description="Размер в человекочитаемом формате")
    processing_status: str = Field(..., description="Статус обработки")
    scan_status: Optional[str] = Field(None, description="Статус сканирования")
    scan_details: Optional[str] = Field(None, description="Детали сканирования")
    metadata_json: Optional[Dict[str, Any]] = Field(None, description="Метаданные")
    requires_attention: bool = Field(..., description="Требует внимания")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "Договор",
                "original_name": "contract.pdf",
                "mime_type": "application/pdf",
                "size": 1024000,
                "size_human": "1.0 MB",
                "processing_status": "processed",
                "scan_status": "clean",
                "scan_details": "no threats found",
                "metadata_json": {"page_count": 5},
                "requires_attention": False,
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:05:00"
            }
        }
    )

    @classmethod
    def from_domain(cls, file: File) -> 'FileResponse':
        """Создание ответа из доменной сущности"""
        return cls(
            id=file.id,
            title=file.title,
            original_name=file.original_name,
            mime_type=file.mime_type,
            size=file.size.bytes,
            size_human=str(file.size),
            processing_status=file.processing_status,
            scan_status=file.scan_status.value if file.scan_status else None,
            scan_details=file.scan_details,
            metadata_json=file.metadata_json,
            requires_attention=file.requires_attention,
            created_at=file.created_at,
            updated_at=file.updated_at,
        )