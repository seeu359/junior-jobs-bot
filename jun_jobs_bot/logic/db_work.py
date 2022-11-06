from datetime import date, timedelta
from jun_jobs_bot.logic.dataclasses import languages_id, region_id, languages
from requests.exceptions import RequestException, HTTPError, URLRequired, \
    TooManyRedirects, Timeout
from jun_jobs_bot.logic.exceptions import DataDownloadError
from jun_jobs_bot import models
from loguru import logger
import requests
import json


COEFFICIENT = 100
WEEK = 7
MONTH = 30
THREE_MONTH = 90
SIX_MONTH = 180
YEAR = 365


class DatabaseWorker:
    _days = {'perweek': WEEK,
             'permonth': MONTH,
             'per3month': THREE_MONTH,
             'per6month': SIX_MONTH,
             'peryear': YEAR,
             }

    def __init__(self):
        self.model = models.Statistics

    def get_today_stat(self, language_id: int) -> models.Statistics:
        with models.session() as s:
            return s.query(self.model).filter(
                   (self.model.date == date.today()) &
                   (self.model.language_id == language_id)).first()

    def get_data_by_comparison_type(
            self, compare_type: str, language_id: int) -> \
            tuple[models.Statistics, models.Statistics]:

        days_diff = date.today() - timedelta(days=6)
        with models.session() as s:

            past_time = s.query(self.model).filter(
                (self.model.date == days_diff) &
                (self.model.language_id == language_id)).first()

            today = s.query(self.model).filter(
                (self.model.date == date.today()) &
                (self.model.language_id == language_id)).first()
        return past_time, today

    def check_db_record(self) -> bool:
        with models.session() as s:
            check_db = s.query(self.model).filter(
                self.model.date == date.today()).first()
            if check_db is not None:
                return True
            return False

    def upload_to_db(self) -> None:
        with models.session() as s:
            data = _get_data()
            for key, value in data.items():
                record = self.model(language_id=languages_id[key],
                                    region_id=region_id['Russia'],
                                    vacancies=value,
                                    date=date.today())

                logger.debug('Record has been added in db!')
                s.add(record)
            s.commit()


def _get_data() -> dict[str, int]:
    data = dict()
    for language in languages:
        template = f'https://api.hh.ru/vacancies?text={language}+junior' \
                   f'&per_page=100&area=113'

        try:
            request = json.loads(requests.get(template).text)
        except (ConnectionError, RequestException, HTTPError,
                URLRequired, TooManyRedirects, Timeout) as e:
            logger.error(f'Request error: {e}')
            raise DataDownloadError(str(e))

        data[language]: int = request['found']
    return data
