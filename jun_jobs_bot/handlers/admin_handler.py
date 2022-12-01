from aiogram import Dispatcher, types
from jun_jobs_bot.logic.exceptions import URLUnavailableError
from jun_jobs_bot.logic.db_work import DatabaseWorker, get_data
from jun_jobs_bot.settings import ADMIN_ID
from jun_jobs_bot.text import MessageReply
from jun_jobs_bot.handlers.buttons import get_admin_buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove


class Request(StatesGroup):
    all = State()


async def select_lang(message: types.Message):
    if str(message.from_user.id) == ADMIN_ID:
        kb_client = get_admin_buttons()
        await message.answer(MessageReply.ADMIN_START, reply_markup=kb_client)
        await Request.all.set()


async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(all=message.text)
    if message.text == 'No':
        await message.answer('Ok', reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif message.text == 'Yes':
        db_worker = DatabaseWorker()
        if db_worker.check_db_record():
            await message.answer(MessageReply.REQUEST_MADE,
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            try:
                data = await get_data()
                db_worker.upload_to_db(data)
            except URLUnavailableError as e:
                await message.answer(
                    str(e), reply_markup=ReplyKeyboardRemove()
                )
                await state.finish()
            await message.answer(MessageReply.DATA_DOWNLOADED_SUCCESS,
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(select_lang, commands=['admin'], state=None)
    dp.register_message_handler(get_result, state=Request.all)
