import os
from aiogram import types, Bot
import mysql.connector
import mysql.connector.pooling
from mysql.connector.pooling import MySQLConnectionPool
import asyncio
from dotenv import load_dotenv, find_dotenv
from clases import Constants

load_dotenv(find_dotenv())


async def not_in_database(id_: int, connection_pool: MySQLConnectionPool) -> bool:
    connector = connection_pool.get_connection()
    with connector.cursor() as cursor:
        cursor.execute(os.getenv("USE_DATABASE"))
        string = os.getenv("SELECT_ID")
        string = string.format(ID=id_)
        cursor.execute(string)
        result_set = cursor.fetchall()
        connector.commit()
        connector.close()
        return len(result_set) == 0


async def insert_full_name(id_: int, full_name: str,
                           connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_NAME")
            string = string.format(ID=id_, NAME=full_name)
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_sex(id_: int, sex: int,
                     connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_DATA_NUMBER")
            string = string.format(ID=id_, DATA=sex, COLUMN="sex")
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_age(id_: int, age: int,
                     connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_DATA_NUMBER")
            string = string.format(ID=id_, DATA=age, COLUMN="age")
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_age_find(id_: int, age_min: int, age_max: int,
                          connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_DATA_NUMBER")
            string = string.format(ID=id_, DATA=age_min, COLUMN="age_min")
            cursor.execute(string)
            string = os.getenv("INSERT_DATA_NUMBER")
            string = string.format(ID=id_, DATA=age_max, COLUMN="age_max")
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_sex_find(id_: int, sex: int,
                          connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_DATA_NUMBER")
            string = string.format(ID=id_, DATA=sex, COLUMN="sex_find")
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def select_name(id_: int, connection_pool: MySQLConnectionPool) -> str:
    connector = connection_pool.get_connection()
    with connector.cursor() as cursor:
        cursor.execute(os.getenv("USE_DATABASE"))
        string = os.getenv("SELECT_NAME")
        string = string.format(ID=id_)
        cursor.execute(string)
        result_set = cursor.fetchall()
        connector.commit()
        connector.close()
        return str(result_set[0][0])


async def insert_media(id_: int, id_media: str, counter: int, connection_pool: MySQLConnectionPool) -> bool:
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_MEDIA")
            string = string.format(ID=id_, COUNTER=counter, DATA=id_media)
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def get_count_of_media(id_: int, connection_pool: MySQLConnectionPool) -> int:
    connector = connection_pool.get_connection()
    with connector.cursor() as cursor:
        cursor.execute(os.getenv("USE_DATABASE"))
        string = os.getenv("SELECT_COUNT")
        string = string.format(ID=id_)
        cursor.execute(string)
        result_set = cursor.fetchall()
        connector.commit()
        connector.close()
        return int(result_set[0][0])


async def insert_description(id_: int, desc: str, connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_STR")
            string = string.format(ID=id_, DATA=desc, COLUMN="description")
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def insert_type(id_: int, type_: int, counter: int, connection_pool: MySQLConnectionPool) -> bool:  # возвращает True если произошла ошибка
    try:
        connector = connection_pool.get_connection()
        with connector.cursor() as cursor:
            cursor.execute(os.getenv("USE_DATABASE"))
            string = os.getenv("INSERT_TYPE")
            string = string.format(ID=id_, COUNTER=counter, DATA=type_)
            cursor.execute(string)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True


async def print_profile(id_: int, connection_pool: MySQLConnectionPool, bot: Bot) -> bool:
    try:
        text = str(os.getenv("FORM_PATTERN"))
        connector = connection_pool.get_connection()

        with connector.cursor() as cursor:
            await bot.send_message(id_, 'Отлично! Вот твоя анкета:')
            cursor.execute(os.getenv("USE_DATABASE"))
            media = []
            string = os.getenv("SELECT_DATA")
            name = string.format(ID=id_, COLUMN='name')
            cursor.execute(name)
            result_name = cursor.fetchall()
            age = string.format(ID=id_, COLUMN='age')
            cursor.execute(age)
            result_age = cursor.fetchall()
            desc = string.format(ID=id_, COLUMN='description')
            cursor.execute(desc)
            result_desc = cursor.fetchall()
            text = text.format(NAME = result_name[0][0], AGE = result_age[0][0], DESC = result_desc[0][0])

            string = os.getenv("SELECT_MEDIA")

            a = string.format(ID=id_, COUNTER=1)
            cursor.execute(a)
            result_set = cursor.fetchall()
            if int(result_set[0][0]) == Constants.video:
                media.append(types.InputMediaVideo(media=result_set[0][1], caption=text))
            else:
                media.append(types.InputMediaPhoto(media=result_set[0][1], caption=text))


            for i in range(2, await get_count_of_media(id_, connection_pool) + 1):
                a = string.format(ID=id_, COUNTER=i)
                cursor.execute(a)
                result_set = cursor.fetchall()
                if int(result_set[0][0]) == Constants.video:
                    media.append(types.InputMediaVideo(media = result_set[0][1]))
                else:
                    media.append(types.InputMediaPhoto(media=result_set[0][1]))

            await bot.send_media_group(-4513837603, media=media)
            await bot.send_media_group(id_, media=media)
            connector.commit()
            connector.close()
        return False
    except Exception as e:
        print(e)
        return True
