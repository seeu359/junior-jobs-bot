from loguru import logger
from jun_jobs_bot import text
from jun_jobs_bot import LANGUAGES_ID, COMPARE_TYPE, AVAILABLE_LANGUAGES
from jun_jobs_bot.logic.statistics import Stats
from jun_jobs_bot.logic.exceptions import NotCorrectData


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


def validate_data(data: dict[str, str]) -> None:
    language, compare_type = data['language'], data['compare_type']

    if language.lower() not in AVAILABLE_LANGUAGES:
        logger.error(f'Not correct data. Language: {language.lower()}')
        raise NotCorrectData(text.MessageReply.NOT_CORRECT_LANG)

    if compare_type.lower().replace(' ', '') not in COMPARE_TYPE:

        logger.error(f'Not correct data. Compare type: '
                     f'{compare_type.lower()}')

        raise NotCorrectData(text.MessageReply.NOT_CORRECT_COMPARE_TYPE)
