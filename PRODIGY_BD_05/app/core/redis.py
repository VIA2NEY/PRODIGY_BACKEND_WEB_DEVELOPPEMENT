import redis
import json
from app.core.config import settings


class RedisClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True  # important pour string
            )
        return cls._instance


def get_redis():
    return RedisClient.get_instance()
