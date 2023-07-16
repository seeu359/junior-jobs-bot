from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup

from jun_jobs_bot.text import MessageReply
from jun_jobs_bot.handlers import buttons
from jun_jobs_bot import services

from loguru import logger
from pydantic import ValidationError


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
        params = services.make_params_from_request(data)
        statistics = services.get_statistics(params)
        await message.answer(statistics, reply_markup=ReplyKeyboardRemove())
        await state.finish()

    except ValidationError as e:
        logger.info(e)
        error = services.make_error_response(e)
        await message.answer(error, reply_markup=ReplyKeyboardRemove())
        await state.finish()


def register_primary_handlers(dp: Dispatcher):
    dp.register_message_handler(get_language, commands=['start'], state=None)
    dp.register_message_handler(get_compare_type, state=Condition.language)
    dp.register_message_handler(get_result, state=Condition.compare_type)
