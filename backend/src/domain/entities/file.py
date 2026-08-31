from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from ..value_objects.file_extension import FileExtension
from ..value_objects.file_size import FileSize
from ..value_objects.scan_status import ScanStatus

@dataclass
class File:
    id: UUID
    title: str
    original_name: str
    stored_name: str
    mime_type: str
    size: FileSize
    processing_status: str
    scan_status: Optional[ScanStatus]
    scan_details: Optional[str]
    metadata_json: Optional[Dict[str, Any]]
    requires_attention: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        title: str,
        original_name: str,
        stored_name: str,
        mime_type: str,
        size: int
    ) -> 'File':
        now = datetime.utcnow()
        return cls(
            id=uuid4(),
            title=title,
            original_name=original_name,
            stored_name=stored_name,
            mime_type=mime_type,
            size=FileSize(size),
            processing_status="uploaded",
            scan_status=None,
            scan_details=None,
            metadata_json=None,
            requires_attention=False,
            created_at=now,
            updated_at=now
        )

    def update_title(self, new_title: str) -> None:
        self.title = new_title
        self.updated_at = datetime.utcnow()

    def mark_as_processing(self) -> None:
        self.processing_status = "processing"
        self.updated_at = datetime.utcnow()

    def mark_as_processed(self, metadata: Dict[str, Any]) -> None:
        self.processing_status = "processed"
        self.metadata_json = metadata
        self.updated_at = datetime.utcnow()

    def mark_as_failed(self, reason: str) -> None:
        self.processing_status = "failed"
        self.scan_status = ScanStatus.FAILED
        self.scan_details = reason
        self.requires_attention = True
        self.updated_at = datetime.utcnow()

    def update_scan_result(
        self,
        status: ScanStatus,
        details: str,
        requires_attention: bool
    ) -> None:
        self.scan_status = status
        self.scan_details = details
        self.requires_attention = requires_attention
        self.updated_at = datetime.utcnow()