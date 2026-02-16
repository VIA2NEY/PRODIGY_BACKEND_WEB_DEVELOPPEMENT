import json
from typing import Any, Optional
from app.core.redis import get_redis
from app.core.config import settings


class CacheService:
    def __init__(self):
        self.redis = get_redis()
        self.default_ttl = settings.REDIS_CACHE_EXPIRE

    def get(self, key: str) -> Optional[Any]:
        data = self.redis.get(key)
        if not data:
            return None
        return json.loads(data)

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expire_time = ttl if ttl else self.default_ttl
        self.redis.setex(
            key,
            expire_time,
            json.dumps(value, default=str)  # important UUID/date
        )

    def delete(self, key: str):
        self.redis.delete(key)

    def invalidate_pattern(self, pattern: str):
        """
        Supprime toutes les clés correspondant au pattern
        Ex: hotels:*
        """
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)
