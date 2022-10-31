from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from jun_jobs_bot.handlers.messages import MessageReply
from jun_jobs_bot.handlers import buttons
from jun_jobs_bot.logic import user_requests, exceptions

class Condition(StatesGroup):
    language = State()
    compare_type = State()


async def choose_lang(message: types.Message):
    kb_client = buttons.get_lang_buttons()
    await message.reply(MessageReply.START, reply_markup=kb_client)
    await Condition.language.set()


async def choose_format(message: types.Message, state: FSMContext):
    kb_client = buttons.get_stats_buttons()
    await state.update_data(language=message.text)
    await message.answer(MessageReply.COMPARE, reply_markup=kb_client)
    await Condition.next()


async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(compare_type=message.text)
    data = await state.get_data()
    try:
        check = user_requests.process_request(data)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        await state.finish()
    else:
        await message.answer(str(check))
        await state.finish()


def register_primary_handlers(dp: Dispatcher):
    dp.register_message_handler(choose_lang, commands=['start'], state=None)
    dp.register_message_handler(choose_format, state=Condition.language)
    dp.register_message_handler(get_result, state=Condition.compare_type)
