from aiogram import executor
from jun_jobs_bot.bot import dp
import logging
from jun_jobs_bot import models
from jun_jobs_bot.handlers.info import register_handlers
from jun_jobs_bot.handlers.primary import register_primary_handlers

"""Entry point"""


logging.basicConfig(level=logging.INFO)


def main():
    models.Base.metadata.create_all(models.engine)
    register_primary_handlers(dp)
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
