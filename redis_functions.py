import time
from typing import List

from redis import asyncio as aioredis

global redis

async def init_redis():
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")

async def get_watched_profiles(_id: int) -> List[str]:
    await init_redis()
    result = await redis.smembers(str(_id))
    return list(map(lambda x: x.decode('utf-8'), result))


async def add_watched_profiles(_id: int, watched_id: int) -> None:
    await init_redis()
    await redis.sadd(str(_id), watched_id)


async def add_liked_profiles(_id: str, watched_id: int) -> None:
    await init_redis()
    await redis.sadd(_id, watched_id)


async def get_liked_profiles(_id: str):
    await init_redis()
    number = await redis.spop(_id)
    if number is None:
        return None
    return number.decode('utf-8')

async def add_anon_liked_profiles(_id: int, watched_id: int) -> None:
    await init_redis()
    await redis.sadd(str(_id), watched_id)


async def get_anon_liked_profiles(_id: str):
    await init_redis()
    number = await redis.spop(_id)
    if number is None:
        return None
    return number.decode('utf-8')
