import logging

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from money_bot.models import User


class AuthMiddleware(BaseMiddleware):
    @staticmethod
    async def on_process_message(message: types.Message, *args):
        logging.info(args)
        tg_user = message.from_user
        await User.get_or_create(
            {
                'username': tg_user.username,
                'full_name': tg_user.full_name,
                'locale': tg_user.language_code,
            },
            id=tg_user.id
        )
