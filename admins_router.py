import aiomysql
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from bot_functions import bot, ban
from clases import Admin


admin_router = Router()
global connection_pool


async def create_admin_router(con_pool: aiomysql.pool.Pool):
    global connection_pool
    connection_pool = con_pool


@admin_router.callback_query(lambda c: c.data and c.data.startswith('btn_99_'))
async def wait_like_from(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.message.chat.id == Admin.admin_chat:
        index = int(callback_query.data.split("_")[-1])
        if index == 1:
            await ban()
        elif index == 2:
            pass
    await bot.answer_callback_query(callback_query.id)