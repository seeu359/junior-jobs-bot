from jun_jobs_bot.logic.exceptions import NotCorrectData
from jun_jobs_bot.logic.dataclasses import COMPARE_TYPE, LANGUAGES_ID, \
    AVAILABLE_LANGUAGES, CONSTANTS
from jun_jobs_bot import messages as msg
from jun_jobs_bot.models import Statistics
from loguru import logger
from jun_jobs_bot.logic.db_work import DatabaseWorker


def process_request(data: dict[str, str]) -> str:
    _language, _compare_type = data['language'], data['compare_type']
    ct_handling = _compare_type.lower().replace(' ', '')
    language_id = LANGUAGES_ID[_language.lower()]
    stat = _Statistics(_language, language_id)
    if ct_handling == COMPARE_TYPE.right_now:
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
        vacancies = self.db_worker.get_today_stat(self.language_id)

        if vacancies is None:
            return msg.MessageReply.HAVE_NO_DATE
        logger.info(f'Data: {self.language}, {vacancies.vacancies}, '
                    f'{vacancies.date}')

        return msg.TODAY_STAT.substitute(
            language=self.language,
            all_vacancies=vacancies.vacancies,
            no_exp_vacancies=vacancies.no_experience
        )

    def get_stats_by_comparison_type(self, _compare_type: str) -> str:
        past_time, now = self.db_worker.get_data_by_comparison_type(
            _compare_type, self.language_id)
        result = self.compute_stats(past_time, now)
        return result

    def compute_stats(self, past_time: Statistics, now: Statistics) -> str:
        result = round(now.vacancies / past_time.vacancies *
                       CONSTANTS['Coefficient'] - CONSTANTS['Coefficient'])
        if result < 0:
            return msg.VACS_DECREASED.substitute(
                language=self.language,
                result=result,
            )
        elif result > 0:
            return msg.VACS_INCREASED.substitute(
                language=self.language,
                result=result,
            )
        else:
            return msg.VACS_NO_CHANGE


def validate_data(data: dict[str, str]) -> None:
    _language, _compare_type = data['language'], data['compare_type']
    if _language.lower() not in AVAILABLE_LANGUAGES:
        logger.error(f'Not correct data. Language: {_language.lower()}')
        raise NotCorrectData(msg.NOT_CORRECT_LANG)
    if _compare_type.lower().replace(' ', '') not in COMPARE_TYPE:
        logger.error(f'Not correct data. Compare type: '
                     f'{_compare_type.lower()}')
        raise NotCorrectData(msg.NOT_CORRECT_COMPARE_TYPE)
