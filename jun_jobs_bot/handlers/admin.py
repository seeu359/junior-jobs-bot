from aiogram import Dispatcher, types
from jun_jobs_bot.settings import ADMIN_ID
from aiogram.dispatcher.filters.state import State, StatesGroup
from jun_jobs_bot.handlers.messages import MessageReply
from jun_jobs_bot.handlers.buttons import get_admin_buttons
from aiogram.dispatcher import FSMContext
from jun_jobs_bot.logic.admin_requests import Requester


class Request(StatesGroup):
    all = State()


async def choose_lang(message: types.Message):
    if str(message.from_user.id) == ADMIN_ID:
        kb_client = get_admin_buttons()
        await message.answer(MessageReply.ADMIN_START, reply_markup=kb_client)
        await Request.all.set()


async def get_result(message: types.Message, state: FSMContext):
    await state.update_data(all=message.text)
    if message.text == 'No':
        await message.answer('Ok')
        await state.finish()
    else:
        m = Requester().upload_to_db()
        await message.answer(m)
        await state.finish()


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(choose_lang, commands=['admin'], state=None)
    dp.register_message_handler(get_result, state=Request.all)
