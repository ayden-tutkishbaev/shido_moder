import asyncio
import logging
import sys
from dotenv import dotenv_values

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.core import create_users_table

from bot import handlers

config = dotenv_values(".env")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=config['BOT_TOKEN'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(
        handlers.rt
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        create_users_table()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("THE BOT IS OFF")