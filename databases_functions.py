import os

import aiomysql
from aiogram import types, Bot
from dotenv import load_dotenv, find_dotenv

from clases import Constants

load_dotenv(find_dotenv())


async def not_in_database(id_: int, pool: aiomysql.pool.Pool) -> bool:
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            string = os.getenv("SELECT_ID")
            string = string.format(ID=id_)
            await cursor.execute(string)
            result_set = await cursor.fetchall()
            await conn.commit()
    return len(result_set) == 0


async def insert_full_name(id_: int, full_name: str, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_NAME")
                string = string.format(ID=id_, NAME=full_name)
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_sex(id_: int, sex: int, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_DATA_NUMBER")
                string = string.format(ID=id_, DATA=sex, COLUMN="sex")
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_age(id_: int, age: int,
                     pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_DATA_NUMBER")
                string = string.format(ID=id_, DATA=age, COLUMN="age")
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_age_find(id_: int, age_min: int, age_max: int, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_DATA_NUMBER")
                string = string.format(ID=id_, DATA=age_min, COLUMN="age_min")
                await cursor.execute(string)
                string = os.getenv("INSERT_DATA_NUMBER")
                string = string.format(ID=id_, DATA=age_max, COLUMN="age_max")
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_sex_find(id_: int, sex: int, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_DATA_NUMBER")
                string = string.format(ID=id_, DATA=sex, COLUMN="sex_find")
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def select_name(id_: int, pool: aiomysql.pool.Pool) -> str:
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            string = os.getenv("SELECT_NAME")
            string = string.format(ID=id_)
            await cursor.execute(string)
            result_set = await cursor.fetchall()
            await conn.commit()
    return str(result_set[0][0])


async def insert_media(id_: int, id_media: str, counter: int, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_MEDIA")
                string = string.format(ID=id_, COUNTER=counter, DATA=id_media)
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def get_count_of_media(id_: int, pool: aiomysql.pool.Pool) -> int:
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            string = os.getenv("SELECT_COUNT")
            string = string.format(ID=id_)
            await cursor.execute(string)
            result_set = await cursor.fetchall()
            await conn.commit()
    return int(result_set[0][0])


async def insert_description(id_: int, desc: str, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_STR")
                string = string.format(ID=id_, DATA=desc, COLUMN="description")
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_type(id_: int, type_: int, counter: int, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_TYPE")
                string = string.format(ID=id_, COUNTER=counter, DATA=type_)
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def print_registration_profile(id_: int, pool: aiomysql.pool.Pool, bot: Bot) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                text = str(os.getenv("FORM_PATTERN"))
                await bot.send_message(id_, 'Отлично! Вот твоя анкета:')
                media = []
                string = os.getenv("SELECT_DATA")
                name = string.format(ID=id_, COLUMN='name')
                await cursor.execute(name)
                result_name = await cursor.fetchall()
                age = string.format(ID=id_, COLUMN='age')
                await cursor.execute(age)
                result_age = await cursor.fetchall()
                desc = string.format(ID=id_, COLUMN='description')
                await cursor.execute(desc)
                result_desc = await cursor.fetchall()
                if result_desc == "":
                    text = os.getenv("FORM_PATTERN_WITHOUT_DESC")
                text = text.format(NAME=result_name[0][0], AGE=result_age[0][0], DESC=result_desc[0][0])
                string = os.getenv("SELECT_MEDIA")
                a = string.format(ID=id_, COUNTER=1)
                await cursor.execute(a)
                result_set = await cursor.fetchall()
                if int(result_set[0][0]) == Constants.video:
                    media.append(types.InputMediaVideo(media=result_set[0][1], caption=text))
                else:
                    media.append(types.InputMediaPhoto(media=result_set[0][1], caption=text))
                i = await get_count_of_media(id_, pool)
                for i in range(2, i + 1):
                    a = string.format(ID=id_, COUNTER=i)
                    await cursor.execute(a)
                    result_set = await cursor.fetchall()
                    if int(result_set[0][0]) == Constants.video:
                        media.append(types.InputMediaVideo(media=result_set[0][1]))
                    else:
                        media.append(types.InputMediaPhoto(media=result_set[0][1]))

                await bot.send_media_group(-4513837603, media=media)
                await bot.send_media_group(id_, media=media)
                await bot.send_message(id_, text="Все верно?")
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_uni(id_: int, uni: int, pool: aiomysql.pool.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                string = os.getenv("INSERT_DATA_NUMBER")
                string = string.format(ID=id_, DATA=uni, COLUMN='university')
                await cursor.execute(string)
                await conn.commit()
        return False
    except Exception as e:
        print(e)
        return True