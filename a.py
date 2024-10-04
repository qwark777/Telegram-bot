import os
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from dotenv import load_dotenv, find_dotenv
from aiogram import F, Bot, Dispatcher, types  # внешние библиотеки
import asyncio
from aiogram.filters import CommandStart, StateFilter

from databases_functions import not_in_database  # вспомогательные файлы
from reply import start_keyboard

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


class USER(StatesGroup):
    registration = State()  # зарегестрирован или нет
    name = State()
    age = State()
    sex = State()
    university = State()
    image = State()


@dp.message(StateFilter(None),CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    if not_in_database(message.from_user.id):
        await message.answer("Привет, я вижу, что мы не знакомы. Хочешь зарегестрироваться?", reply_markup=start_keyboard)
    await state.set_state(USER.registration)

@dp.message(F.photo)
async def start_cmd(message: types.Message):
    document_id = message.photo[-1].file_id
    file_info = await bot.get_file(document_id)
    string = os.getenv("TRACE")
    tmp = string.format(id=message.from_user.id, number_of_media=file_info.file_id)
    await bot.download_file(file_info.file_path, tmp)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
