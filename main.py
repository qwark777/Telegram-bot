import asyncio
import logging
import threading
from aiogram import Bot, Dispatcher, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv
router = Router()
bot = Bot(token="7061086759:AAF_s5oDahOFyjojIVMTGnyU-BEJjxEkgdA")
dp = Dispatcher(storage=MemoryStorage())

async def main():
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    await bot.delete_webhook(drop_pending_updates=True)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Сообщение приветствия, чел отправляет свое имя")


@router.message(Command())
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
