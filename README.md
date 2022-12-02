[![code-check](https://github.com/seeu359/junior-jobs-bot/actions/workflows/test_linter_check.yaml/badge.svg)](https://github.com/seeu359/junior-jobs-bot/actions/workflows/test_linter_check.yaml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/40e70737d55a80dbd3cf/test_coverage)](https://codeclimate.com/github/seeu359/junior-jobs-bot/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/40e70737d55a80dbd3cf/maintainability)](https://codeclimate.com/github/seeu359/junior-jobs-bot/maintainability)

---
### Bot name

>@JunJobsBot

---
### Description
The bot parses junior vacancies by the main programming languages, referring to the selected recruiting platform, and displays the statistics in a convenient form for the selected language. 
You can output the number of jobs right now, or choose the *type of comparison,  and understand the dynamics of job growth and the general idea of what is happening with the IT industry.

---

### Installation

1. Clone repo: ``$ git clone https://github.com/seeu359/junior-jobs-bot.git``
2. Go to the directory with code: ``$ cd junior-jobs-bot``
3. Set the dependencies:
   1. If you're using poetry, run command: ``$ make p_install``
   2. Else: ``$ make install``

---

### Dependencies

| Library | Version | Description                                 |
|---------|---------|---------------------------------------------|
| python  | 3.10    |                                             |  
| aiogram | 2.22.2    | Asynchronous framework for Telegram Bot API |
 | sqlalchemy | 1.4.42 | ORM for working with database |
 | psycopg2 | 2.9.5 | PostgreSQL database adapter |
 | aiohttp | 3.8.3 | Asynchronous HTTP requests to HH API |
 | alembic | 1.8.1 | Migration tools for SQLAlchemy ORM | 

---

#### Available language:
1. Python
2. Java
3. JavaScript
4. Ruby
5. PHP

#### Available types of comparisons:

1. Right now - displays the number of vacancies right now
2. Per week - Comparison with the number of vacancies a week ago
3. Per month - Comparison with the number of vacancies a month ago
4. Per 3 month - Comparison with the number of vacancies a 3 month ago
5. Per 6 month - Comparison with the number of vacancies a 6 month ago
6. Per 3 month - Comparison with the number of vacancies a year ago

---

*since the bot is little more than a month old, the actual comparison is only available for a month. If you select a longer period, the comparison for a month will be shown