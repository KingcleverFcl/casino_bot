import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from db import create_db

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.environ["BOT_TOKEN"], parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await create_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())