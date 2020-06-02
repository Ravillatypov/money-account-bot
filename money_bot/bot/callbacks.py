from aiogram.types import inline_keyboard as kb, CallbackQuery

from money_bot.bot.dispatcher import bot, dp
from money_bot.models import User, Tag, AccountOperation, OperationType


@dp.callback_query_handler(lambda x: x.data == 'tags_list')
async def tag_list(callback_query: CallbackQuery, **kwargs):
    tag_names = []
    async for tag in Tag.filter(user__id=callback_query.from_user.id):
        tag_names.append(f'{tag.name} ({tag.type.ru_name().lower()})')
    text = '\n'.join(tag_names) if tag_names else 'У вас нет меток'
    await bot.send_message(callback_query.message.chat.id, text)


@dp.callback_query_handler(lambda x: x.data.startswith('op_type_'))
async def set_operation_type(callback_query: CallbackQuery, **kwargs):
    val, op_id = callback_query.data.replace('op_type_', '').split('_')
    op_type = OperationType(val)
    await AccountOperation.filter(id=int(op_id)).update(type=op_type)

    await callback_query.answer(f'Тип {op_type.ru_name().lower()}')

    markup = kb.InlineKeyboardMarkup(row_width=2)
    async for i in Tag.filter(user_id=callback_query.from_user.id, type__in=[op_type, OperationType.any]):
        markup.add(kb.InlineKeyboardButton(i.name, callback_data=f'op_tag_{i.id}_{op_id}'))
    if markup.inline_keyboard:
        markup.inline_keyboard.append([kb.InlineKeyboardButton('Готово', callback_data='delete_message')])
        await callback_query.message.edit_text('Добавьте метки', reply_markup=markup)
    else:
        await callback_query.message.delete()


@dp.callback_query_handler(lambda x: x.data.startswith('op_tag_'))
async def add_tag_to_operation(callback_query: CallbackQuery, **kwargs):
    tag_id, op_id = callback_query.data.replace('op_tag_', '').split('_')
    op = await AccountOperation.get(id=int(op_id))
    tag = await Tag.get(id=int(tag_id))
    await op.tags.add(tag)
    await callback_query.answer('Метка добавлена')


@dp.callback_query_handler(lambda x: x.data == 'delete_message')
async def delete(callback_query: CallbackQuery, **kwargs):
    await callback_query.message.delete()


@dp.callback_query_handler(lambda x: x.data.startswith('tag_add_'))
async def add_tag(callback_query: CallbackQuery, **kwargs):
    tag_type = OperationType(callback_query.data.replace('tag_add_', ''))
    tag_name = callback_query.message.text
    user = await User.get(id=callback_query.from_user.id)
    await Tag.get_or_create(defaults={'type': tag_type}, name=tag_name, user=user)
    await callback_query.answer('Метка добавлена')
    await callback_query.message.delete()
