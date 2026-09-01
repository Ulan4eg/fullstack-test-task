from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from ...core.database import Base
from ...domain.entities.file import File
from ...domain.value_objects.file_size import FileSize
from ...domain.value_objects.scan_status import ScanStatus

class FileModel(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)
    stored_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    mime_type: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    processing_status: Mapped[str] = mapped_column(String(50), nullable=False, default="uploaded")
    scan_status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    scan_details: Mapped[str | None] = mapped_column(String(500), nullable=True)
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    requires_attention: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_domain(self) -> File:
        """Конвертация из ORM модели в доменную сущность"""
        return File(
            id=UUID(self.id),
            title=self.title,
            original_name=self.original_name,
            stored_name=self.stored_name,
            mime_type=self.mime_type,
            size=FileSize(self.size),
            processing_status=self.processing_status,
            scan_status=ScanStatus.from_string(self.scan_status) if self.scan_status else None,
            scan_details=self.scan_details,
            metadata_json=self.metadata_json,
            requires_attention=self.requires_attention,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, file: File) -> 'FileModel':
        """Конвертация из доменной сущности в ORM модель"""
        return cls(
            id=str(file.id),
            title=file.title,
            original_name=file.original_name,
            stored_name=file.stored_name,
            mime_type=file.mime_type,
            size=file.size.bytes,
            processing_status=file.processing_status,
            scan_status=file.scan_status.value if file.scan_status else None,
            scan_details=file.scan_details,
            metadata_json=file.metadata_json,
            requires_attention=file.requires_attention,
            created_at=file.created_at,
            updated_at=file.updated_at,
        )

    def update_from_domain(self, file: File) -> None:
        """Обновление модели из доменной сущности"""
        self.title = file.title
        self.processing_status = file.processing_status
        self.scan_status = file.scan_status.value if file.scan_status else None
        self.scan_details = file.scan_details
        self.metadata_json = file.metadata_json
        self.requires_attention = file.requires_attention
        self.updated_at = file.updated_at