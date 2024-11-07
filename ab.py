import asyncio
from redis import asyncio as aioredis

async def main():
    redis = await aioredis.from_url("redis://localhost")

    try:
        my_array = [1, 2, 3]

        # Добавляем значения в конец списка
        await redis.rpush('mylist', *my_array)

        # Получаем элементы из списка
        result = await redis.lrange('mylist', 0, -1)

        # Выводим результат
        print(result)
    finally:
        await redis.aclose()

asyncio.run(main())