from pydantic import BaseModel
from typing import Literal


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
