import os
from dotenv import load_dotenv, find_dotenv
from aiogram import F, Bot, Dispatcher, types
import asyncio
from aiogram.filters import CommandStart

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()


def not_in_database(id: int) -> bool:
    return True  # переделать


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    if not_in_database(message.from_user.id):
        await message.answer("Привет, я вижу, что мы не знакомы. Хочешь зарегестрироваться?")


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
