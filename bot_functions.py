import os
import mysql
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv
from mysql.connector.pooling import MySQLConnectionPool
from clases import AlbumMiddleware


load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))

def get_connection_pool() -> MySQLConnectionPool:
    return mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=32, user="root", password="12345678", host="localhost")