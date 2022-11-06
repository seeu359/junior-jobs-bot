from jun_jobs_bot.logic.exceptions import NotCorrectMessage
from jun_jobs_bot.logic.dataclasses import languages, compare_type, \
    languages_id
from jun_jobs_bot.messages import MessageReply
from jun_jobs_bot.models import Statistics
from loguru import logger
from jun_jobs_bot.logic.db_work import DatabaseWorker

COEFFICIENT = 100
WEEK = 7
MONTH = 30
THREE_MONTH = 90
SIX_MONTH = 180
YEAR = 365


def process_request(request: dict[str, str]) -> str:
    _language, _compare_type = request['language'], request['compare_type']
    ct_handling = _compare_type.lower().replace(' ', '')
    lang_id = languages_id[_language.lower()]
    stat = _Statistics(_language, lang_id)
    if ct_handling == compare_type.right_now:
        data = stat.get_today_stat()
    else:
        data = stat.get_stats_by_comparison_type(ct_handling)
    return data


class _Statistics:
    db_worker = DatabaseWorker()

    def __init__(self, language: str, language_id: int):
        self.language = language
        self.language_id = language_id

    def get_today_stat(self) -> str:
        data = self.db_worker.get_today_stat(self.language_id)
        if data is None:
            return MessageReply.HAVE_NO_DATE
        logger.info(f'Data: {self.language}, {data.vacancies}, '
                    f'{data.date}')
        return f'{self.language} vacancies at the moment: {data.vacancies}'

    def get_stats_by_comparison_type(self, _compare_type: str) -> str:
        past_time, now = self.db_worker.get_data_by_comparison_type(
            _compare_type, self.language_id)
        result = self.compute_stats(past_time, now)
        return result

    def compute_stats(self, past_time: Statistics, now: Statistics) -> str:
        result = round(now.vacancies / past_time.vacancies *
                       COEFFICIENT - COEFFICIENT)
        if result < 0:
            return f'The number of {self.language} jobs decreased by ' \
                   f'{abs(result)}%'
        elif result > 0:
            return f'The number of {self.language} vacancies has ' \
                   f'increased by {result}%'
        else:
            return 'The number of vacancies has not changed'


def validate_data(data: dict[str, str]) -> None:
    _language, _compare_type = data['language'], data['compare_type']
    if _language.lower() not in languages:
        logger.error(f'Not correct data. Language: {_language.lower()}')
        raise NotCorrectMessage('I can\'t process this kind of language')
    if _compare_type.lower().replace(' ', '') not in compare_type:
        logger.error(f'Not correct data. Compare type: '
                     f'{_compare_type.lower()}')
        raise NotCorrectMessage('I can\'t compare it to this type of')
