from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from clases import User

users_find = Router()


@users_find.message(User.find)
async def print_profile(message: types.Message, state: FSMContext):
    pass
