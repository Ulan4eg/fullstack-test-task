from pathlib import Path
from typing import Dict, Any
from ..entities.file import File

class MetadataExtractor:
    """Доменный сервис для извлечения метаданных"""

    @classmethod
    def extract(cls, file: File, file_path: Path) -> Dict[str, Any]:
        """Извлечение метаданных из файла"""
        metadata = {
            "extension": Path(file.original_name).suffix.lower(),
            "size_bytes": file.size.bytes,
            "mime_type": file.mime_type,
            "size_human": str(file.size),
        }

        # Извлечение специфичных метаданных в зависимости от типа
        if file.mime_type.startswith("text/"):
            metadata.update(cls._extract_text_metadata(file_path))
        elif file.mime_type == "application/pdf":
            metadata.update(cls._extract_pdf_metadata(file_path))
        elif file.mime_type.startswith("image/"):
            metadata.update(cls._extract_image_metadata(file_path))

        return metadata

    @classmethod
    def _extract_text_metadata(cls, file_path: Path) -> Dict[str, Any]:
        """Извлечение метаданных из текстовых файлов"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()

            return {
                "line_count": len(lines),
                "char_count": len(content),
                "word_count": len(content.split()),
                "encoding": "utf-8",
            }
        except Exception:
            return {
                "line_count": 0,
                "char_count": 0,
                "word_count": 0,
                "encoding": "unknown",
            }

    @classmethod
    def _extract_pdf_metadata(cls, file_path: Path) -> Dict[str, Any]:
        """Извлечение метаданных из PDF файлов"""
        try:
            content = file_path.read_bytes()
            page_count = max(content.count(b"/Type /Page"), 1)

            return {
                "approx_page_count": page_count,
                "file_size_bytes": len(content),
            }
        except Exception:
            return {
                "approx_page_count": 1,
                "file_size_bytes": 0,
            }

    @classmethod
    def _extract_image_metadata(cls, file_path: Path) -> Dict[str, Any]:
        """Извлечение метаданных из изображений"""
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                return {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "mode": img.mode,
                }
        except ImportError:
            return {
                "width": 0,
                "height": 0,
                "format": "unknown",
                "mode": "unknown",
            }
        except Exception:
            return {
                "width": 0,
                "height": 0,
                "format": "unknown",
                "mode": "unknown",
            }