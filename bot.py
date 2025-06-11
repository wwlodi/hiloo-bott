import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import settings
from handlers import start, order, utils, cleanup
from utils.logger import setup_logger


async def main():
    setup_logger()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(
        start.router,
        order.router,
        utils.router,
        cleanup.router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
