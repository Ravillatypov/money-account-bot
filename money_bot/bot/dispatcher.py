from os import environ as env

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from money_bot.bot.middleware import AuthMiddleware

PROXY_URL = env.get('PROXY_URL')
if PROXY_URL:
    bot = Bot(token=env.get('API_TOKEN', ''), proxy=PROXY_URL)
else:
    bot = Bot(token=env.get('API_TOKEN', ''))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(AuthMiddleware())
