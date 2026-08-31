from typing import Optional, Any, Dict, Tuple
from datetime import datetime, timedelta
import hashlib
import json
import asyncio
from functools import lru_cache

class InMemoryCache:
    """Простой in-memory кэш с TTL"""

    def __init__(self, default_ttl: int = 300):
        self._cache: Dict[str, Tuple[datetime, Any]] = {}
        self.default_ttl = default_ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Получить значение из кэша"""
        if key in self._cache:
            timestamp, value = self._cache[key]
            if datetime.utcnow() - timestamp < timedelta(seconds=self.default_ttl):
                return value
            async with self._lock:
                if key in self._cache:
                    del self._cache[key]
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Сохранить значение в кэш"""
        ttl = ttl or self.default_ttl
        async with self._lock:
            self._cache[key] = (datetime.utcnow() + timedelta(seconds=ttl), value)

    async def delete(self, key: str) -> None:
        """Удалить значение из кэша"""
        async with self._lock:
            if key in self._cache:
                del self._cache[key]

    async def clear(self) -> None:
        """Очистить весь кэш"""
        async with self._lock:
            self._cache.clear()

    async def get_or_set(self, key: str, factory, ttl: Optional[int] = None) -> Any:
        """Получить из кэша или создать новое значение"""
        value = await self.get(key)
        if value is not None:
            return value

        value = await factory()
        await self.set(key, value, ttl)
        return value

    @staticmethod
    def generate_key(*args, **kwargs) -> str:
        """Генерация ключа из аргументов"""
        data = {
            "args": args,
            "kwargs": kwargs
        }
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()

# Глобальный экземпляр кэша
cache = InMemoryCache(default_ttl=300)