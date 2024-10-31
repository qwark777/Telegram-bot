import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, any_state
from dotenv import load_dotenv, find_dotenv
from aiogram import F, Bot, Dispatcher, types  # внешние библиотеки
import asyncio
from aiogram.filters import StateFilter, Command
import mysql.connector
from aiogram.types import video_note, InputMediaPhoto, InputMedia, InputMediaVideo
from mysql.connector import pooling, cursor
import time

from bot_functions import get_connection_pool, bot
from databases_functions import not_in_database, insert_full_name, insert_sex, insert_age, insert_age_find, \
    insert_sex_find, select_name, get_count_of_media, print_registration_profile, insert_media, \
    insert_description, insert_type  # вспомогательные файлы
from reply import start_keyboard, del_keyboard, sex_keyboard, find_sex_keyboard
from clases import User, AlbumMiddleware, Constants
from users_router import user_router

dp = Dispatcher()
dp.message.middleware(AlbumMiddleware())
dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    connection_pool = get_connection_pool()
    asyncio.run(main())
