import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, any_state
from dotenv import load_dotenv, find_dotenv
from aiogram import F, Bot, Dispatcher, types  # внешние библиотеки
import asyncio
from aiogram.filters import StateFilter, Command
import mysql.connector
from aiogram.types import video_note
from mysql.connector import pooling, cursor

from databases_functions import not_in_database, insert_full_name, insert_sex, insert_age, insert_age_find, \
    insert_sex_find, select_name  # вспомогательные файлы
from reply import start_keyboard, del_keyboard, sex_keyboard

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
import sched
import time
import datetime

def my_function():
    pass

# создание объекта планировщика
scheduler = sched.scheduler(time.time, time.sleep)

# задание времени выполнения функции
event_time = datetime.datetime.now().replace(hour=10, minute=30, second=0, microsecond=0)

# добавление задания в планировщик
scheduler.enterabs(event_time.timestamp(), 1, my_function, ())

# запуск планировщика
scheduler.run()


@dp.message(StateFilter(None), F.content_type == types.ContentType.VIDEO_NOTE)
async def start(message: types.Message, state: FSMContext):
    await message.answer_video_note(message.video_note.file_id)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    dbconfig = {
        "user": "root",
        "password": "12345678",
        "host": "localhost",
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=20, **dbconfig)
    asyncio.run(main())

# document_id = message.photo[-1].file_id
#     file_info = await bot.get_file(document_id)
#     string = os.getenv("TRACE")
#     tmp = string.format(id=message.from_user.id, number_of_media=file_info.file_id)
#     await bot.download_file(file_info.file_path, tmp)