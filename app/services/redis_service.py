from datetime import timedelta
from typing import Optional

from app.core.config import settings

from pydantic import BaseModel
from redis import Redis


redis_client = Redis(host=settings.REDIS_HOST, port=6379)


class RedisData(BaseModel):
    key: str
    value: str | bytes
    ttl: Optional[int | timedelta] = None


class SyncRedis:
    @classmethod
    def set_redis_key(
        cls, redis_data: RedisData, *, is_transaction: bool = False
    ) -> None:
        with redis_client.pipeline(transaction=is_transaction) as pipe:
            pipe.set(redis_data.key, redis_data.value)
            if redis_data.ttl:
                pipe.expire(redis_data.key, redis_data.ttl)

            pipe.execute()

    @classmethod
    def get_by_key(cls, key: str):
        return redis_client.get(key)

    @classmethod
    def delete_by_key(cls, key: str) -> None:
        return redis_client.delete(key)

    @classmethod
    def lpush_by_key(cls, key: str, value) -> None:
        return redis_client.lpush(key, value)

    @classmethod
    def lrange_by_key(cls, key: str) -> list[str]:
        return redis_client.lrange(key, 0, -1)

    @classmethod
    def lrem_by_key(cls, key: str, value) -> int:
        return redis_client.lrem(key, 0, value)
