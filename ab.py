import asyncio
from redis import asyncio as aioredis

async def main():
    redis = aioredis.from_url("redis://localhost")

    try:
        await redis.set("my-key", "value", ex=604800)
        value = await redis.get("my-key")
        print(value.decode('utf-8'))
    finally:
        await redis.aclose()

asyncio.run(main())