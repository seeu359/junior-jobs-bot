from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from jun_jobs_bot.handlers.messages import MessageReply


class Condition(StatesGroup):
    language = State()
    compare_type = State()


async def choose_lang(message: types.Message):
    await message.reply(MessageReply.START)
    await Condition.language.set()


async def choose_format(message: types.Message, state: FSMContext):
    await state.update_data(language=message.text)
    await message.answer(MessageReply.COMPARE)
    await Condition.next()


async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(compare_type=message.text)
    data = await state.get_data()
    await message.answer(str(data))
    await state.finish()


def register_primary_handlers(dp: Dispatcher):
    dp.register_message_handler(choose_lang, commands=['start'], state=None)
    dp.register_message_handler(choose_format, state=Condition.language)
    dp.register_message_handler(get_result, state=Condition.compare_type)