import asyncio
import aiohttp
from aiohttp import ClientSession
from loguru import logger
from datetime import date, timedelta
from jun_jobs_bot.logic.exceptions import URLUnavailableError
from jun_jobs_bot import models
from jun_jobs_bot import text
from jun_jobs_bot.dataclasses import LANGUAGES_ID, AVAILABLE_REGIONS, \
    AVAILABLE_LANGUAGES, CONSTANTS


class DatabaseWorker:

    def __init__(self):
        self.model = models.Statistics

    def get_today_stat(self, language_id: int) -> models.Statistics:
        with models.session() as s:
            return s.query(self.model).filter(
                   (self.model.date == date.today()) &
                   (self.model.language_id == language_id)).first()

    def get_data_by_comparison_type(
            self, compare_type: str, language_id: int
            ) -> models.Statistics:
        
        if compare_type not in ('perweek', 'permonth', 'rightnow'):
            compare_type = 'permonth'
        days_diff = date.today() - timedelta(days=CONSTANTS[compare_type])
        with models.session() as s:
            past_time = s.query(self.model).filter(
                (self.model.date == days_diff) &
                (self.model.language_id == language_id)).first()
            logger.info(f'Past time: ' f'Lang id: {past_time.language_id}, '
                        f'Vacancies: {past_time.vacancies}')
            return past_time

    def check_db_record(self) -> bool:
        with models.session() as s:
            check_db = s.query(self.model).filter(
                self.model.date == date.today()).first()
            if check_db is not None:
                return True
            return False

    def upload_to_db(self, data) -> None:
        with models.session() as s:
            for key, value in data.items():
                record = self.model(
                    language_id=LANGUAGES_ID[key],
                    region_id=AVAILABLE_REGIONS['Russia'],
                    vacancies=value[0],
                    date=date.today(),
                    no_experience=value[1]
                    )

                s.add(record)
            s.commit()


async def get_data() -> dict[str, list]:
    async with aiohttp.ClientSession() as session:

        requests_all_vacancies = [
            _get_vacancies(session, url, lang) for lang, url
            in list(_get_url_template().items())
        ]

        requests_no_exp_vacancies = [
            _get_vacancies(session, url, lang) for lang, url in
            list(_get_url_template(text.NO_EXP_TEMPLATE).items())
        ]
        all_vacs = await asyncio.gather(*requests_all_vacancies)
        no_exp = await asyncio.gather(*requests_no_exp_vacancies)

        return _get_merge_data([*all_vacs, *no_exp])


async def _get_vacancies(session: ClientSession, url: str, language):
    async with session.get(url) as result:
        if result.status != 200:
            logger.error(
                text.ExceptionMessage.CONNECTION_ERROR.substitute(
                    url=url,
                    status=result.status,
                )
            )
            raise URLUnavailableError(
                text.ExceptionMessage.CONNECTION_ERROR.substitute(
                    url=url,
                    status=result.status,
                )
            )
        response = await result.json()
        return {language: response['found']}


def _get_url_template(template=text.ALL_VACS_TEMPLATE):
    urls = dict()
    for language in AVAILABLE_LANGUAGES:
        url = template.substitute(
           language=language,
           area_id=AVAILABLE_REGIONS['Russia'],
        )
        urls[language] = url
    return urls


def _get_merge_data(data: list[dict]) -> dict[str, list]:
    merge_data = dict()
    for record in data:
        for k, v in record.items():
            if k in merge_data:
                merge_data[k].append(v)
            else:
                merge_data[k] = [v]

    return merge_data


async def func():
    async with aiohttp.ClientSession() as s:
        try:
            a = await _get_vacancies(s, 'https://site.com/404', 'some')
        except URLUnavailableError:
            print('Ошибка')

print(asyncio.run(func()))