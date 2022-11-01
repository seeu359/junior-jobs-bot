from jun_jobs_bot.logic.exceptions import NotCorrectMessage
from jun_jobs_bot.logic.dataclasses import languages, compare_type
from datetime import date, timedelta
from jun_jobs_bot.models import Requests, session
from jun_jobs_bot.logic.admin_requests import languages_id


COEFFICIENT = 100


def process_request(request: dict[str, str]) -> str:
    _language, _compare_type = request['language'], request['compare_type']
    ct_handling = _compare_type.lower().replace(' ', '')
    lang_id = languages_id[_language.lower()]
    stat = Statistics(_language, lang_id)
    handler = {'rightnow': stat.get_today_stat(),
               'perweek': stat.get_week_stat(),
               'permonth': stat.get_month_stat(),
               'per3month': stat.get_three_month_stat(),
               'per6month': stat.get_six_month_stat(),
               'peryear': stat.get_year_stat(),
               }
    data = handler[ct_handling]
    return data


class Statistics:

    def __init__(self, language: str, language_id: int):
        self.language = language
        self.language_id = language_id
        self.today = date.today()

    def get_today_stat(self) -> str:
        with session() as s:
            data = \
                s.query(Requests).filter((Requests.date == self.today) &
                                         (Requests.language_id
                                          == self.language_id)).first()
            return f'{self.language} vacancies at the moment: {data.vacancies}'

    def get_week_stat(self) -> str:
        week_ago = self.today - timedelta(days=7)
        with session() as s:
            data = s.query(
                Requests).filter((Requests.date > week_ago) &
                                 (Requests.date <= self.today) &
                                 (Requests.date == self.language_id)).all()
            result = self.count_week_stat(data)
            return result

    def get_month_stat(self):
        return f'Заглушка 30'

    def get_three_month_stat(self):
        return f'Заглушка 90'

    def get_six_month_stat(self):
        return f'Заглушка 180'

    def get_year_stat(self):
        return f'Заглушка 365'

    def count_week_stat(self, data: list[Requests]) -> str:
        data.sort(key=lambda x: x.date)
        week_ago, now = data[0], data[1]
        result = round(now.vacancies / week_ago.vacancies *
                       COEFFICIENT - COEFFICIENT)
        if result < 0:
            return f'The number of {self.language} jobs decreased by ' \
                   f'{abs(result)}%'
        elif result > 0:
            return f'The number of {self.language} vacancies has ' \
                   f'increased by {result}%'
        else:
            return f'The number of vacancies has not changed'


def validate_data(data: dict[str, str]) -> None:
    _language, _compare_type = data['language'], data['compare_type']
    if _language.lower() not in languages:
        raise NotCorrectMessage('I can\'t process this kind of language')
    if _compare_type.lower().replace(' ', '') not in compare_type:
        raise NotCorrectMessage('I can\'t compare it to this type of')
