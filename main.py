import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import run_app
from aiohttp.web_app import Application

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
APP_BASE_URL = getenv("APP_BASE_URL")

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")


def main():
    dp["base_url"] = APP_BASE_URL
    dp.startup.register(on_startup)

    app = Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    ).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)

    logger.info("Starting bot")

    run_app(app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    main()