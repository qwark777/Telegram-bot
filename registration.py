from getpass import getpass
import asyncio
from mysql.connector import connect, Error
import mysql.connector.pooling


try:
    with connect(
        host="localhost",
        user="root",
        password="12345678",
    ) as connection:
        show_db_query = "SHOW DATABASES"
        with connection.cursor() as cursor:
            cursor.execute(show_db_query)
            for db in cursor:
                print(db)
except Error as e:
    print(e)

class User_info:
    user_id = 0
    age = 0
    first_name = ""
    second_name = ""

async def insert_database(row, data):
    pass