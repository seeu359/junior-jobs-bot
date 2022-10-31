from jun_jobs_bot.logic.exceptions import NotCorrectMessage
from jun_jobs_bot.logic.dataclasses import Languages, CompareType

languages = Languages(python='python', php='php', javascript='javascript',
                      ruby='ruby', java='java')

compare_type = CompareType(right_now='rightnow', per_week='perweek',
                           per_month='permonth', per_3_month='per3month',
                           per_6_month='per6month', per_year='peryear')


def process_request(request: dict[str, str]) -> str:
    _language_, _compare_type = _validate_data(request)
    return 'OK'


def _validate_data(data: dict[str, str]) -> tuple:
    _language, _compare_type = data['language'], data['compare_type']
    if _language.lower() not in languages:
        raise NotCorrectMessage('I can\'t process this kind of language')
    if _compare_type.lower().replace(' ', '') not in compare_type:
        raise NotCorrectMessage('I can\'t compare it to this type of')
    return _language, _compare_type
