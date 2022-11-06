import unittest

import pytest
import requests_mock
from jun_jobs_bot import messages
from aiogram_unittest import Requester
from jun_jobs_bot.logic import exceptions
from jun_jobs_bot.logic.db_work import _get_data
from aiogram_unittest.handler import MessageHandler
from aiogram_unittest.types.dataset import MESSAGE
from jun_jobs_bot.logic.statistics import validate_data
from aiogram_unittest.handler import CallbackQueryHandler
from aiogram_unittest.types.dataset import CALLBACK_QUERY
from jun_jobs_bot.handlers.info_handler import get_info, get_help
from jun_jobs_bot.handlers.primary_handler import get_language, \
    get_compare_type, Condition


@pytest.mark.parametrize('data',
                         [({'language': 'Wrong Python',
                           'compare_type': 'Per Week'}),
                          ({'language': 'Java',
                            'compare_type': 'Wrong Type'})
                          ])
def test_validate_data1(data):
    with pytest.raises(exceptions.NotCorrectMessage):
        validate_data(data)


def test_get_data():
    with requests_mock.Mocker() as mock:
        test_key = 'test'
        test_data = '{"found": "%s"}' % test_key
        mock.get(f'https://api.hh.ru/vacancies?text=python+junior'
                 f'&per_page=100&area=113', text=test_data)
        mock.get(f'https://api.hh.ru/vacancies?text=php+junior'
                 f'&per_page=100&area=113', text=test_data)
        mock.get(f'https://api.hh.ru/vacancies?text=javascript+junior'
                 f'&per_page=100&area=113', text=test_data)
        mock.get(f'https://api.hh.ru/vacancies?text=ruby+junior'
                 f'&per_page=100&area=113', text=test_data)
        mock.get(f'https://api.hh.ru/vacancies?text=java+junior'
                 f'&per_page=100&area=113', text=test_data)
        tested_func = _get_data()
        assert len(tested_func) == 5
        assert tested_func['python'] == test_key
        assert tested_func['ruby'] == test_key


class TestBot(unittest.IsolatedAsyncioTestCase):
    async def test_help_handler(self):
        requester = Requester(request_handler=MessageHandler(get_help))
        message = MESSAGE.as_object(text='Hello')
        calls = await requester.query(message)
        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, messages.MessageReply.HELP)

    async def test_info_handler(self):
        requester = Requester(
            request_handler=MessageHandler(get_info, commands=['info']))
        message = MESSAGE.as_object(text='/info')
        calls = await requester.query(message)
        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, messages.MessageReply.INFO)

    async def test_get_lang_handler(self):
        requester = Requester(
            request_handler=MessageHandler(get_language, commands=["start"]))

        message = MESSAGE.as_object(text="/start")
        calls = await requester.query(message)

        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, messages.MessageReply.SELECT_LANG)

    async def test_get_compare_type_handler(self):
        requester = Requester(
            request_handler=MessageHandler(get_compare_type,
                                           state=Condition.language))

        message = MESSAGE.as_object(text='Python')
        calls = await requester.query(message)
        answer_message = calls.send_message.fetchone().text
        self.assertEqual(answer_message, messages.MessageReply.COMPARE)
