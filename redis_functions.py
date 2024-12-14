from typing import List

from redis import asyncio as aioredis


async def get_watched_profiles(_id: int) -> List[str]:
    redis = await aioredis.from_url("redis://localhost")
    try:
        result = await redis.smembers(str(_id))
    finally:
        await redis.aclose()
    return list(map(lambda x: x.decode('utf-8'), result))

async def add_watched_profiles(_id: int, watched_id: int) -> None:
    redis = await aioredis.from_url("redis://localhost")
    try:
        await redis.sadd(str(_id), watched_id)
    finally:
        await redis.aclose()


async def add_liked_profiles(_id: str, watched_id: int) -> None:
    redis = await aioredis.from_url("redis://localhost")
    try:
        await redis.sadd(_id, watched_id)
    finally:
        await redis.aclose()

async def get_liked_profiles(_id: str):
    redis = await aioredis.from_url("redis://localhost")
    try:
        number = await redis.srandmember(_id)
        return number.decode('utf-8')
    finally:
        await redis.aclose()