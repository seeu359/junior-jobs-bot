from pydantic import ValidationError
from typing import Union, Dict
from jun_jobs_bot.logic import statistics as st
from jun_jobs_bot.logic.classes import RequestData
from jun_jobs_bot import text


def get_language(data: Dict[str, str]) -> Union[str, None]:
    """Abstraction for receive language from user input data"""
    return data.get('language', None)


def get_compare_type(data: Dict[str, str]) -> Union[str, None]:
    """Abstraction for receive compare type from user input data"""
    return data.get('compare_type', None)


def make_error_response(error: ValidationError) -> str:
    invalid_value = list()
    for error in error.errors():
        invalid_value.append(error['ctx']['given'])
    return f'Can\'t process this data: {", ".join(invalid_value)} :('


def make_params_from_request(data: Dict[str, str]) \
        -> Union[str, RequestData]:
    language = get_language(data)
    compare_type = get_compare_type(data)
    request_data = RequestData(
            language=_handle_params(language),
            compare_type=_handle_params(compare_type),
        )
    return request_data


def get_statistics(request_data: RequestData) -> str:
    _statistics = st.Statistics(request_data).stat
    response = _hande_statistics(request_data, _statistics)
    return response


def _handle_params(param: str) -> str:
    normalize_param = param.lower()
    mapper = {
        'right now': 'today',
        'per week': 'week',
        'per month': 'month',
    }
    compare_type = mapper.get(normalize_param)
    if not compare_type:
        return param.replace(' ', '')
    return compare_type.replace(' ', '')


def _hande_statistics(params: RequestData, stat) -> str:
    language = stat['language'].capitalize()
    if params.compare_type == 'today':
        all_vacs = stat['vacancies']
        no_exp_vac = stat['no_experience']
        return text.MessageReply.TODAY_STAT.substitute(
            language=language,
            all_vacancies=all_vacs,
            no_exp_vacancies=no_exp_vac,
        )
    else:
        comparison = stat['comparison']['in_percent']
        if comparison > 0:
            return text.MessageReply.VACS_INCREASED.substitute(
                language=language,
                result=abs(comparison),
            )
        elif comparison < 0:
            return text.MessageReply.VACS_DECREASED.substitute(
                language=language,
                result=abs(comparison),
            )
        else:
            return text.MessageReply.VACS_NO_CHANGE
