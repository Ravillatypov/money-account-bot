from os import environ as env

from aiogram.utils import executor
from tortoise import Tortoise

from money_bot.bot import dp


async def on_startup(*args):
    await Tortoise.init(modules={'money_bot': ['money_bot.models']}, db_url=env.get('DB_URL'))
    await Tortoise.generate_schemas()


async def on_shutdown(*args):
    await Tortoise.close_connections()


if __name__ == '__main__':
    sentry_dsn = env.get('SENTRY_DSN', '')
    release = env.get('RELEASE', '')
    if sentry_dsn:
        try:
            import sentry_sdk
            from sentry_sdk.integrations.aiohttp import AioHttpIntegration

            sentry_sdk.init(sentry_dsn, release=release, integrations=[AioHttpIntegration()])
        except Exception:
            pass

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
