import asyncio

from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_functions import get_connection_pool, bot
from clases import AlbumMiddleware
from sheduler import delete_inactive_users
from user_find import users_find
from users_reg_router import user_reg

dp = Dispatcher()
dp.message.middleware(AlbumMiddleware())
dp.include_router(user_reg)
dp.include_router(users_find)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    connection_pool = await get_connection_pool()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_inactive_users, args=[connection_pool], trigger='cron', hour=0, minute=0)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())