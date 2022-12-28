import unittest
from aiogram_unittest import Requester
from aiogram_unittest.handler import MessageHandler
from aiogram_unittest.types.dataset import MESSAGE

from jun_jobs_bot import text
from jun_jobs_bot.handlers.info_handler import get_info, get_help
from jun_jobs_bot.handlers.primary_handler import (
    get_language,
    get_compare_type,
    Condition,
)


class TestBot(unittest.IsolatedAsyncioTestCase):
    async def test_help_handler(self):
        requester = Requester(request_handler=MessageHandler(get_help))
        message = MESSAGE.as_object(text='Hello')
        calls = await requester.query(message)
        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, text.MessageReply.HELP)

    async def test_info_handler(self):
        requester = Requester(
            request_handler=MessageHandler(get_info, commands=['info']))
        message = MESSAGE.as_object(text='/info')
        calls = await requester.query(message)
        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, text.MessageReply.INFO)

    async def test_get_lang_handler(self):
        requester = Requester(
            request_handler=MessageHandler(get_language, commands=["start"]))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, text.MessageReply.SELECT_LANG)

    async def test_get_compare_type_handler(self):
        requester = Requester(
            request_handler=MessageHandler(get_compare_type,
                                           state=Condition.language))

        message = MESSAGE.as_object(text='Python')
        calls = await requester.query(message)
        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, text.MessageReply.COMPARE)
