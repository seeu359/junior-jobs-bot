from pydantic import BaseModel
from typing import Literal, NamedTuple


class RequestData(BaseModel):
    language: Literal['python', 'ruby', 'php', 'javascript', 'java']
    compare_type: Literal[
        'rightnow',
        'perweek',
        'permonth',
        'per3month',
        'per6month',
        'peryear',
    ]


class RequestParams(NamedTuple):
    language: str
    compare_type: str
