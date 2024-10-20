import os
import mysql.connector
import mysql.connector.pooling
from mysql.connector.pooling import MySQLConnectionPool
import asyncio
from dotenv import load_dotenv, find_dotenv

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


async def insert_media(id_: int, id_media: int, connection_pool: MySQLConnectionPool) -> str:
    connector = connection_pool.get_connection()
    with connector.cursor() as cursor:
        cursor.execute(os.getenv("USE_DATABASE"))
        string = os.getenv("INSERT_DATA_NUMBER")
        string = string.format(ID=id_)
        cursor.execute(string)
        result_set = cursor.fetchall()
        connector.commit()
        connector.close()
        return str(result_set[0][0])