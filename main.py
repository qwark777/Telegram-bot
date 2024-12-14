import asyncio

import aiomysql
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_functions import bot, dp
from clases import AlbumMiddleware
from sheduler import delete_inactive_users
from user_find import users_find, create_user_find_router
from users_reg_router import user_reg, create_user_router

dp.message.middleware(AlbumMiddleware())
dp.include_router(user_reg)
dp.include_router(users_find)

async def main():
    connection_pool = await aiomysql.create_pool(host='localhost', port=3306, user='root', password='12345678', db='msutndr', minsize=1, maxsize=100)
    await create_user_router(connection_pool)
    await create_user_find_router(connection_pool)
    await bot.delete_webhook(drop_pending_updates=True)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(delete_inactive_users, args=[connection_pool], trigger='cron', hour=0, minute=0)
    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())