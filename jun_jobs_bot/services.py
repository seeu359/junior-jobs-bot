from pydantic import ValidationError
from typing import Union, Dict, Literal

import requests
from furl import furl
from dataclasses import dataclass
from pydantic import BaseModel

from jun_jobs_bot import text


class RequestData(BaseModel):
    language: Literal['python', 'ruby', 'php', 'javascript', 'java']
    compare_type: Literal[
        'today',
        'week',
        'month',
        'per3month',
        'per6month',
        'peryear',
    ]


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


def get_statistics(request_params: RequestData) -> str:

    _statistics = _Statistics(request_params).stat
    response = _handle_statistics(request_params, _statistics)

    return response


def _handle_params(param: str) -> str:

    normalize_param = param.lower()

    mapper = {
        'right now': 'today',
        'per week': 'week',
        'per month': 'month',
        'per 3 month': 'month',
        'per 6 month': 'month',
        'per year': 'month',
    }

    compare_type = mapper.get(normalize_param)

    if not compare_type:
        return normalize_param.replace(' ', '')
    return compare_type.replace(' ', '')


def _handle_statistics(params: RequestData, stat) -> str:

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


@dataclass
class URLParts:
    """
    URL parts for build url in Statistics class. Netloc - its body of api url.
    Other params - parts of url, which represent models from database.
    """
    netloc = 'https://jun-jobs-api.online/'
    stat_path = '/stat'


class _Statistics:

    def __init__(self, request_data: RequestData):

        self.request_data = request_data
        self.url = \
            furl(URLParts.netloc) / URLParts.stat_path / \
            self.request_data.language / self.request_data.compare_type
        self.stat = self._get_stat()

    def _get_stat(self) -> Dict:
        return requests.get(self.url).json()
