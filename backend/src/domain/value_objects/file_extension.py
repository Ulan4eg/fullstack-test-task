from dataclasses import dataclass
from pathlib import Path
from typing import Set, Optional

@dataclass(frozen=True)
class FileExtension:
    """Value Object для расширения файла"""
    value: str

    def __post_init__(self):
        if not self.value or not self.value.startswith('.'):
            raise ValueError("Extension must start with '.'")

    @classmethod
    def from_filename(cls, filename: str) -> Optional['FileExtension']:
        """Создание из имени файла"""
        path = Path(filename)
        if path.suffix:
            return cls(path.suffix.lower())
        return None

    @property
    def without_dot(self) -> str:
        """Расширение без точки"""
        return self.value[1:]

    def in_set(self, extensions: Set[str]) -> bool:
        """Проверка, входит ли расширение в набор"""
        return self.value in extensions

    def __str__(self) -> str:
        return self.value