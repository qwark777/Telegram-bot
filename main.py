from aiogram import Dispatcher
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_functions import get_connection_pool, bot
from clases import User, AlbumMiddleware, Constants
from sheduler import delete_inactive_users
from users_router import user_router

dp = Dispatcher()
dp.message.middleware(AlbumMiddleware())
dp.include_router(user_router)

async def sync_task():
    print("Выполнение синхронной задачи")



async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync_task, 'interval', seconds=1)  # Запуск задачи каждые 60 секунд
    scheduler.start()

    await dp.start_polling(bot)
    print(1)




if __name__ == "__main__":

    connection_pool = get_connection_pool()

    asyncio.run(main())

