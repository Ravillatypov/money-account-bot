import logging
import re
from typing import Tuple

from aiogram.types import inline_keyboard as kb, Message

from money_bot.bot.dispatcher import bot, dp
from money_bot.models import User, AccountOperation, OperationType

f_regexp = re.compile(r'(\d+?\s?\d+)([,.0-9]?)(\d{2})?')


def get_amount_and_description(s: str) -> Tuple[float, str]:
    m = f_regexp.match(s)
    if m:
        matched = ''.join((i for i in m.groups() if isinstance(i, str)))
        desc = s.replace(matched, '')
        matched = matched.replace(' ', '').replace(',', '.')
    else:
        matched = s if s.isdigit() else '0'
        desc = ''

    try:
        return float(matched), desc
    except Exception:
        return 0, desc


@dp.message_handler(commands=['start'])
async def start(message: Message):
    markup = kb.InlineKeyboardMarkup()

    markup.add(kb.InlineKeyboardButton('Метки', callback_data='tags_list'))
    markup.add(kb.InlineKeyboardButton('Расход', callback_data='operation_add_expenditure'))
    markup.add(kb.InlineKeyboardButton('Доход', callback_data='operation_add_revenue'))

    await bot.send_message(
        message.chat.id,
        f'{message.from_user.full_name}, привет! Я бот который поможет тебе ввести учет расходов и доходов',
        reply_markup=markup,
    )


@dp.message_handler(commands=['add_tags'])
async def add_tags(message: Message):
    markup = kb.InlineKeyboardMarkup()
    for i in (OperationType.expenditure, OperationType.revenue, OperationType.any):
        markup.add(kb.InlineKeyboardButton(i.ru_name(), callback_data=f'tag_add_{i.value}'))

    for tag_name in [i.strip().lower() for i in message.text.replace('/add_tags', '').split(',')]:
        await bot.send_message(message.chat.id, tag_name, reply_markup=markup)


@dp.message_handler()
async def add_operation(message: Message):
    logging.info(message)
    user = await User.get(id=message.from_user.id)
    amount, desc = get_amount_and_description(message.text)
    if not amount:
        return await bot.send_message(message.chat.id, 'help')
    op = await AccountOperation.create(user=user, amount=amount, description=desc)
    markup = kb.InlineKeyboardMarkup()
    for i in OperationType.allowed():
        markup.add(kb.InlineKeyboardButton(i.ru_name(), callback_data=f'op_type_{i.value}_{op.id}'))

    await message.reply('Выберите тип операции', reply_markup=markup)
