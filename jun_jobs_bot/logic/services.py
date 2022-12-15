from pydantic import ValidationError
from typing import Optional
from jun_jobs_bot.logic import statistics as st
from jun_jobs_bot.logic.classes import RequestParams, RequestData
from jun_jobs_bot import text


def get_language(data: dict[str, str]) -> Optional[str, None]:
    return data.get('language', None)


def get_compare_type(data: dict[str, str]) -> Optional[str, None]:
    return data.get('compare_type', None)


def get_request_params(request_data: RequestData) -> RequestParams:
    mapper = {
        'rightnow': 'today',
        'perweek': 'week',
        'permonth': 'month',
    }
    language = request_data.language
    compare_type = request_data.compare_type
    return RequestParams(
        language=language,
        compare_type=mapper[compare_type]
    )


def make_error_response(error: ValidationError) -> str:
    invalid_value = list()
    for error in error.errors():
        invalid_value.append(error['ctx']['given'])
    return f'Can\'t process this data: {", ".join(invalid_value)}'


def make_params_from_request(data: dict[str, str]) \
        -> Optional[str, RequestData]:
    language = get_language(data)
    compare_type = get_compare_type(data)
    request_data = RequestData(
            language=_handle_params(language),
            compare_type=_handle_params(compare_type),
        )
    return request_data


def get_statistics(request_data: RequestData) -> str:
    request_params = get_request_params(request_data)
    _statistics = st.Statistics(request_params).stat
    response = _hande_statistics(request_params, _statistics)
    return response


def _handle_params(param: str) -> str:
    return param.replace(' ', '').lower()


def _hande_statistics(params: RequestParams, stat) -> str:
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
