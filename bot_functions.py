import os
from typing import List

import aiomysql
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv("TOKEN"))


async def get_connection_pool() -> aiomysql.pool.Pool:
    return await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='msutndr', minsize=1, maxsize=100)


async def get_any_profile(pool: aiomysql.pool.Pool) -> None:
    pass


async def create_inline_keyboard(button_texts: List[str]) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=text, callback_data=f'btn_{i + 1}')] for i, text in enumerate(button_texts)]
    buttons.append([InlineKeyboardButton(text="Принять 👍", callback_data=f'btn_{100}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def back_in_reg():
    pass