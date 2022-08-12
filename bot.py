import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.start import register_start_handlers
from tgbot.handlers.yacht import register_yacht_handlers
from tgbot.middlewares.db import DbMiddleware
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.handlers.admin import register_admin
from tgbot.handlers.cars import register_cars_handlers
from tgbot.integrations.telegraph.service import TelegraphService
from tgbot.middlewares.integration import IntegrationMiddleware

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, file_uploader):
    dp.setup_middleware(DbMiddleware())
    dp.middleware.setup(IntegrationMiddleware(file_uploader))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    # register_admin(dp)
    # register_user(dp)
    register_start_handlers(dp)
    register_cars_handlers(dp)
    register_yacht_handlers(dp)
    # register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    file_uploader = TelegraphService()
    
    bot['config'] = config
    bot["file_uploader"] = file_uploader
    
    register_all_middlewares(dp, file_uploader)
    register_all_filters(dp)
    register_all_handlers(dp)


    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
