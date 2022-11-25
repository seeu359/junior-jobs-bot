from datetime import date, timedelta
from jun_jobs_bot.dataclasses import LANGUAGES_ID, AVAILABLE_REGIONS, \
    AVAILABLE_LANGUAGES, CONSTANTS
from requests.exceptions import RequestException, HTTPError, URLRequired, \
    TooManyRedirects, Timeout
from jun_jobs_bot.logic.exceptions import DataDownloadError
from jun_jobs_bot import models
from loguru import logger
from string import Template
import requests


ALL_VACANCIES_URL_TEMPLATE = Template(
        'https://api.hh.ru/vacancies?'
        'text=$language+junior&per_page=100&area=$area_id'
)

NO_EXPERIENCE_URL_TEMPLATE = Template(
        'https://api.hh.ru/vacancies?'
        'text=$language+junior&per_page=100&'
        'area=$area_id&experience=noExperience'
)


class DatabaseWorker:

    def __init__(self):
        self.model = models.Statistics

    def get_today_stat(self, language_id: int) -> models.Statistics:
        with models.session() as s:
            return s.query(self.model).filter(
                   (self.model.date == date.today()) &
                   (self.model.language_id == language_id)).first()

    def get_data_by_comparison_type(
            self, compare_type: str, language_id: int) -> models.Statistics:

        days_diff = date.today() - timedelta(days=CONSTANTS['perweek'])
        with models.session() as s:

            past_time = s.query(self.model).filter(
                (self.model.date == days_diff) &
                (self.model.language_id == language_id)).first()
            logger.info(f'Past time: '
                        f'Lang id: {past_time.language_id}, '
                        f'Vacancies: {past_time.vacancies}')
        return past_time

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
                record = self.model(
                    language_id=LANGUAGES_ID[key],
                    region_id=AVAILABLE_REGIONS['Russia'],
                    vacancies=value[0],
                    date=date.today(),
                    no_experience=value[1]
                    )

                logger.debug('Record has been added in db!')
                s.add(record)
            s.commit()


def _get_data() -> dict[str, tuple[int, int]]:
    data = dict()

    for language in AVAILABLE_LANGUAGES:
        all_vacancies_url, no_experience_url = _get_url_template(language)

        try:
            all_vacancies_query = requests.get(all_vacancies_url).json()
            logger.info('All - running')
            no_experience_query = requests.get(no_experience_url).json()
            logger.info('noexp - running')

        except (ConnectionError, RequestException, HTTPError,
                URLRequired, TooManyRedirects, Timeout) as e:
            logger.error(f'Request error: {e}')
            raise DataDownloadError(str(e))

        data[language]: tuple[int, int] = \
            all_vacancies_query['found'], no_experience_query['found']
    return data


def _get_url_template(language: str) -> tuple[str, str]:

    all_vacancies_url = ALL_VACANCIES_URL_TEMPLATE.substitute(
       language=language,
       area_id=AVAILABLE_REGIONS['Russia'],
    )

    no_experience_url = NO_EXPERIENCE_URL_TEMPLATE.substitute(
        language=language,
        area_id=AVAILABLE_REGIONS['Russia'],
    )
    return all_vacancies_url, no_experience_url
