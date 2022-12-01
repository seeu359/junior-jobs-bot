from aiogram import types, Dispatcher
from jun_jobs_bot.text import MessageReply


async def get_info(message: types.Message):
    await message.answer(MessageReply.INFO)


async def get_help(message: types.Message):
    await message.answer(MessageReply.HELP)


def register_info_handlers(db: Dispatcher):
    db.register_message_handler(get_info, commands=['info'], state=None)
    db.register_message_handler(get_help, state=None)
