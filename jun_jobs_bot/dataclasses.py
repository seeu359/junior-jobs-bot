from enum import Enum
from typing import NamedTuple, TypedDict


class ExperienceType(Enum):
    pass


class Employed(Enum):
    pass


class LanguagesId(TypedDict):
    python: int
    php: int
    javascript: int
    ruby: int
    java: int


LANGUAGES_ID = LanguagesId(
    python=1,
    php=2,
    javascript=3,
    ruby=4,
    java=5
)


class AvailableRegions(TypedDict):
    """Available regions for sampling jobs.
    Structure:
    Region = Region ID in hh api region-dictionary. The ID also matches the ID
    in the database"""
    Russia: int


AVAILABLE_REGIONS = AvailableRegions(
    Russia=113,
)


class AvailableLanguages(NamedTuple):
    python: str
    php: str
    javascript: str
    ruby: str
    java: str


AVAILABLE_LANGUAGES = AvailableLanguages(
    python='python',
    php='php',
    javascript='javascript',
    ruby='ruby',
    java='java'
)


class CompareType(NamedTuple):
    right_now: str
    per_week: str
    per_month: str
    per_3_month: str
    per_6_month: str
    per_year: str


COMPARE_TYPE = CompareType(
    right_now='rightnow',
    per_week='perweek',
    per_month='permonth',
    per_3_month='per3month',
    per_6_month='per6month',
    per_year='peryear'
)


class Constants(TypedDict):
    Coefficient: int
    perweek: int
    permonth: int
    per3month: int
    per6month: int
    peryear: int


CONSTANTS = Constants(
    Coefficient=100,
    perweek=7,
    permonth=30,
    per3month=90,
    per6month=180,
    peryear=365
)
