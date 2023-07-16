from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_lang_buttons() -> ReplyKeyboardMarkup:
    python = KeyboardButton("Python")
    java = KeyboardButton("Java")
    ruby = KeyboardButton("Ruby")
    js = KeyboardButton("JavaScript")
    php = KeyboardButton("Php")
    client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    client.add(python).add(java).add(ruby).add(js).add(php)
    return client


def get_stats_buttons() -> ReplyKeyboardMarkup:
    now = KeyboardButton("Right now")
    per_week = KeyboardButton("Per week")
    per_month = KeyboardButton("Per month")
    per_3_month = KeyboardButton("Per 3 month")
    per_6_month = KeyboardButton("Per 6 month")
    per_year = KeyboardButton("Per year")
    client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    client.add(now).add(per_week).add(per_month).add(per_3_month).add(per_6_month).add(
        per_year
    )
    return client


def get_admin_buttons() -> ReplyKeyboardMarkup:
    yes = KeyboardButton("Yes")
    no = KeyboardButton("No")
    client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    client.row(yes, no)
    return client
