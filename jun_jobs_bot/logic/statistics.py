from jun_jobs_bot.logic.exceptions import NotCorrectData
from jun_jobs_bot.dataclasses import COMPARE_TYPE, LANGUAGES_ID, \
    AVAILABLE_LANGUAGES, CONSTANTS
from jun_jobs_bot import messages as msg
from jun_jobs_bot.models import Statistics
from loguru import logger
from jun_jobs_bot.logic.db_work import DatabaseWorker


def process_request_data(data: dict[str, str]) -> tuple[str, str]:
    language, compare_type = data['language'], data['compare_type']
    processed_compare_type = compare_type.lower().replace(' ', '')
    return language, processed_compare_type


def get_statistics(language: str, compare_type: str) -> str:
    language_id = LANGUAGES_ID[language.lower()]
    stat = Stats(language, language_id)
    if compare_type == COMPARE_TYPE.right_now:
        today_data = stat.get_today_stat()
        return stat.return_today_stats(today_data)
    now, past_time = stat.get_stats_by_comparison_type(compare_type)
    compute_state = stat.compute_stats(now.vacancies, past_time.vacancies)
    return stat.return_stat_by_comp_type(compute_state)


class Stats:

    db_worker = DatabaseWorker()

    def __init__(self, language: str, language_id: int):
        self.language = language
        self.language_id = language_id

    def get_today_stat(self) -> str | tuple[int, int]:
        vacancies = self.db_worker.get_today_stat(self.language_id)

        logger.info(f'Data: {self.language}, {vacancies.vacancies}, '
                    f'{vacancies.date}')

        if vacancies is None:
            return msg.MessageReply.HAVE_NO_DATE
        return vacancies.vacancies, vacancies.no_experience

    def get_stats_by_comparison_type(
            self, _compare_type: str) -> tuple[Statistics, Statistics]:
        now = self.db_worker.get_today_stat(self.language_id)
        past_time = self.db_worker.get_data_by_comparison_type(
            _compare_type, self.language_id)
        return now, past_time

    @staticmethod
    def compute_stats(now: int, past_time: int) -> int:
        return round(now / past_time *
                     CONSTANTS['Coefficient'] - CONSTANTS['Coefficient'])

    def return_today_stats(self, vacancies: tuple[int, int]) -> str:
        """Returns the final line with today's statistics"""
        if isinstance(vacancies, str):
            return vacancies
        return msg.TODAY_STAT.substitute(
            language=self.language,
            all_vacancies=vacancies[0],
            no_exp_vacancies=vacancies[1],
        )

    def return_stat_by_comp_type(self, vacancies: int) -> str:
        """Returns the final line with statistics """
        if vacancies < 0:
            return msg.VACS_DECREASED.substitute(
                language=self.language,
                result=vacancies,
            )
        elif vacancies > 0:
            return msg.VACS_INCREASED.substitute(
                language=self.language,
                result=vacancies,
            )
        else:
            return msg.VACS_NO_CHANGE


def validate_data(data: dict[str, str]) -> None:
    language, compare_type = data['language'], data['compare_type']
    if language.lower() not in AVAILABLE_LANGUAGES:
        logger.error(f'Not correct data. Language: {language.lower()}')
        raise NotCorrectData(msg.NOT_CORRECT_LANG)
    if compare_type.lower().replace(' ', '') not in COMPARE_TYPE:
        logger.error(f'Not correct data. Compare type: '
                     f'{compare_type.lower()}')
        raise NotCorrectData(msg.NOT_CORRECT_COMPARE_TYPE)
