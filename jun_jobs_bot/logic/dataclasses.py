from typing import NamedTuple, TypedDict


class LanguagesId(TypedDict):
    python: int
    java: int
    php: int
    javascript: int
    ruby: int


class RegionId(TypedDict):
    Russia: int


class Languages(NamedTuple):
    python: str
    php: str
    javascript: str
    ruby: str
    java: str


class CompareType(NamedTuple):
    right_now: str
    per_week: str
    per_month: str
    per_3_month: str
    per_6_month: str
    per_year: str


languages_id = LanguagesId(python=1, php=2, javascript=3, ruby=4, java=5)

region_id = RegionId(Russia=113)

languages = Languages(python='python', php='php', javascript='javascript',
                      ruby='ruby', java='java')

compare_type = CompareType(right_now='rightnow', per_week='perweek',
                           per_month='permonth', per_3_month='per3month',
                           per_6_month='per6month', per_year='peryear')
