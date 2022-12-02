from loguru import logger
from jun_jobs_bot import CONSTANTS
from jun_jobs_bot.models import Statistics
from jun_jobs_bot.text import MessageReply
from jun_jobs_bot.logic.db_work import DatabaseWorker


class Stats:

    db_worker = DatabaseWorker()

    def __init__(self, language: str, language_id: int):
        self.language = language
        self.language_id = language_id

    def get_today_stat(self) -> str | tuple[int, int]:
        vacancies = self.db_worker.get_today_stat(self.language_id)

        if vacancies is None:
            logger.info(f'vacancies is {str(vacancies)}')
            return MessageReply.HAVE_NO_DATE
        logger.info(f'{vacancies}')
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
        """Returns the final string with today's statistics"""
        if isinstance(vacancies, str):
            return vacancies
        return MessageReply.TODAY_STAT.substitute(
            language=self.language,
            all_vacancies=vacancies[0],
            no_exp_vacancies=vacancies[1],
        )

    def return_stat_by_comp_type(self, vacancies: int) -> str:
        """return the final string depending on the type of comparison"""
        if vacancies < 0:
            return MessageReply.VACS_DECREASED.substitute(
                language=self.language,
                result=vacancies,
            )
        elif vacancies > 0:
            return MessageReply.VACS_INCREASED.substitute(
                language=self.language,
                result=vacancies,
            )
        else:
            return MessageReply.VACS_NO_CHANGE
