from dataclasses import dataclass

@dataclass(frozen=True)
class FileSize:
    """Value Object для размера файла"""
    bytes: int

    def __post_init__(self):
        if self.bytes < 0:
            raise ValueError("File size cannot be negative")

    @property
    def kilobytes(self) -> float:
        return self.bytes / 1024

    @property
    def megabytes(self) -> float:
        return self.bytes / (1024 * 1024)

    @property
    def gigabytes(self) -> float:
        return self.bytes / (1024 * 1024 * 1024)

    def __str__(self) -> str:
        if self.bytes < 1024:
            return f"{self.bytes} B"
        elif self.bytes < 1024 * 1024:
            return f"{self.kilobytes:.1f} KB"
        elif self.bytes < 1024 * 1024 * 1024:
            return f"{self.megabytes:.1f} MB"
        else:
            return f"{self.gigabytes:.1f} GB"

    def __lt__(self, other: 'FileSize') -> bool:
        return self.bytes < other.bytes

    def __le__(self, other: 'FileSize') -> bool:
        return self.bytes <= other.bytes

    def __gt__(self, other: 'FileSize') -> bool:
        return self.bytes > other.bytes

    def __ge__(self, other: 'FileSize') -> bool:
        return self.bytes >= other.bytes