from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class FileCreateRequest(BaseModel):
    """Запрос на создание файла"""
    title: str = Field(..., min_length=1, max_length=255, description="Название файла")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Договор с подрядчиком"
            }
        }
    )

class FileUpdateRequest(BaseModel):
    """Запрос на обновление файла"""
    title: str = Field(..., min_length=1, max_length=255, description="Новое название файла")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Обновленный договор"
            }
        }
    )

class FileFilterRequest(BaseModel):
    """Фильтр для списка файлов"""
    status: Optional[str] = Field(None, description="Статус обработки")
    requires_attention: Optional[bool] = Field(None, description="Требует внимания")
    search: Optional[str] = Field(None, description="Поиск по названию")