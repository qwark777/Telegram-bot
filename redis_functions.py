import asyncio
from typing import List

from redis import asyncio as aioredis


async def get_watched_profiles(_id: int) -> List[str]:
    redis = await aioredis.from_url("redis://localhost")
    try:
        result = await redis.lrange(str(_id), 0, -1)
    finally:
        await redis.aclose()
    return list(map(lambda x: x.decode('utf-8'), result))