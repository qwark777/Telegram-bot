from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot_functions import get_connection_pool, bot
from clases import User

users_find = Router()


@users_find.message(User.find)
async def print_profile(message: types.Message, state: FSMContext):
    connection_pool = await get_connection_pool()
