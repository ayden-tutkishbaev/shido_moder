import asyncio
import logging
import sys
from dotenv import dotenv_values

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.core import *

from middlewares import *

from bot.utils import *

from bot import admins
from bot import handlers

config = dotenv_values(".env")


async def main() -> None:
    dp = Dispatcher()
    bot = Bot(token=config['BOT_TOKEN'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # dp.message.middleware(ThrottlingMiddleware())
    dp.include_routers(
        admins.rt,
        handlers.rt
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # stories_table()
    # create_languages_table()
    # eng_stories_table()
    # rus_stories_table()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("THE BOT IS OFF")