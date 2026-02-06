import json
from typing import Any, Optional
from app.cache.redis_client import redis_client

class CacheService:

    @staticmethod
    def get(key: str) -> Optional[Any]:
        value = redis_client.get(key)
        return json.loads(value) if value else None

    @staticmethod
    def set(key: str, value: Any, ttl: int):
        redis_client.setex(key, ttl, json.dumps(value))

    @staticmethod
    def delete(key: str):
        redis_client.delete(key)
