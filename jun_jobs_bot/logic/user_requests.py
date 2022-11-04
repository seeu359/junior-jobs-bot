from jun_jobs_bot.logic.exceptions import NotCorrectMessage
from jun_jobs_bot.logic.dataclasses import languages, compare_type, \
    languages_id
from datetime import date, timedelta
from jun_jobs_bot.models import Requests, session
from loguru import logger

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
    stat = Statistics(_language, lang_id)
    if ct_handling == compare_type.right_now:
        data = stat.get_today_stat()
    else:
        data = stat.get_stats(ct_handling)
    return data


class Statistics:

    _days = {'perweek': WEEK,
             'permonth': MONTH,
             'per3month': THREE_MONTH,
             'per6month': SIX_MONTH,
             'peryear': YEAR,
             }

    def __init__(self, language: str, language_id: int):
        self.language = language
        self.language_id = language_id

    def get_today_stat(self) -> str:
        with session() as s:
            data = \
                s.query(Requests).filter((Requests.date == date.today()) &
                                         (Requests.language_id
                                          == self.language_id)).first()
            if data is None:
                return 'Today\'s data has not yet been uploaded'
            logger.info(f'Data: {self.language}, {data.vacancies}, '
                        f'{data.date}')
            return f'{self.language} vacancies at the moment: {data.vacancies}'

    def get_stats(self, _compare_type: str) -> str:
        days = self._days[_compare_type]
        days_diff = date.today() - timedelta(days=4)
        with session() as s:
            past_time = s.query(Requests).filter((Requests.date == days_diff) &
                                                 (Requests.language_id ==
                                                 self.language_id)).first()
            now = s.query(Requests).filter((Requests.date == date.today()) &
                                           (Requests.language_id ==
                                            self.language_id)).first()
            logger.info(f'Data: {self.language}, {past_time.vacancies}, '
                        f'{past_time.date}, {now.vacancies}, {now.date}')
            result = self.compute_data(past_time, now)
            return result

    def compute_data(self, past_time: Requests, now: Requests) -> str:
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
