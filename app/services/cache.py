from redis.asyncio import Redis
from typing import Any
import json

class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> Any | None:
        data = await self.redis.get(key)
        if not data:
            return None
        return json.loads(data)

    async def set(self, key: str, value: Any, ttl: int) -> None:
        await self.redis.set(key, json.dumps(value, default=str), ex=ttl)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)