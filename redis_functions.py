from typing import List

from redis import asyncio as aioredis

global redis

async def init_redis():
    global redis
    redis = await aioredis.from_url("redis://localhost")

async def get_watched_profiles(_id: int) -> List[str]:
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    result = await redis.smembers(str(_id))
    return list(map(lambda x: x.decode('utf-8'), result))


async def add_watched_profiles(_id: int, watched_id: int) -> None:
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    await redis.sadd(str(_id), watched_id)


async def add_liked_profiles(_id: str, watched_id: int) -> None:
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    await redis.sadd(_id, watched_id)


async def get_liked_profiles(_id: str):
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    number = await redis.spop(_id)
    if number is None:
        return None
    return number.decode('utf-8')

async def add_anon_liked_profiles(_id: int, watched_id: int) -> None:
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    await redis.sadd(str(_id), watched_id)


async def get_anon_liked_profiles(_id: str, self_id: str):
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    number = await redis.smembers(_id)
    for i in number:
        a = i
        a = a.decode('utf-8')
        if a == self_id:
            return True
    return False


async def add_mes_liked_profiles(_id: str,watched_id: int, mes: str) -> None:
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    await redis.sadd(str(_id), str(watched_id) + '!iH!' + mes)


async def get_mes_liked_profiles(_id: str, self_id: str) -> str:
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://localhost")
    number = await redis.smembers(_id)
    for i in number:
        a = i
        a = a.decode('utf-8')
        if a.startswith(self_id + '!iH!'):
            await redis.srem(_id, i)
            return a[len(self_id) + 4:]
    return ''