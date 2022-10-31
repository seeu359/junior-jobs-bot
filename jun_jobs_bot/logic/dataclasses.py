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
