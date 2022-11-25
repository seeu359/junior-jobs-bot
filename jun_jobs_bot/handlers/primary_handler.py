from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from jun_jobs_bot.messages import MessageReply
from jun_jobs_bot.handlers import buttons
from jun_jobs_bot.logic import statistics, exceptions
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup


class Condition(StatesGroup):
    language = State()
    compare_type = State()


async def get_language(message: types.Message):
    kb_client = buttons.get_lang_buttons()
    await message.reply(MessageReply.SELECT_LANG, reply_markup=kb_client)
    await Condition.language.set()


async def get_compare_type(message: types.Message, state: FSMContext):
    kb_client = buttons.get_stats_buttons()
    await state.update_data(language=message.text)
    await message.answer(MessageReply.COMPARE, reply_markup=kb_client)
    await Condition.next()


async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(compare_type=message.text)
    data = await state.get_data()
    try:
        statistics.validate_data(data)
    except exceptions.NotCorrectData as e:
        await message.answer(str(e), reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        language, processed_compare_type = \
            statistics.process_request_data(data)
        answer = statistics.get_statistics(
            language,
            processed_compare_type,
        )
        await message.answer(answer, reply_markup=ReplyKeyboardRemove())
        await state.finish()


def register_primary_handlers(dp: Dispatcher):
    dp.register_message_handler(get_language, commands=['start'], state=None)
    dp.register_message_handler(get_compare_type, state=Condition.language)
    dp.register_message_handler(get_result, state=Condition.compare_type)
